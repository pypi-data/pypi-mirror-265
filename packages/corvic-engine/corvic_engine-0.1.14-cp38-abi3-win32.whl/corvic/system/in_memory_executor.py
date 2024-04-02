"""Staging-agnostic in-memory executor."""

from typing import cast

import polars as pl
import pyarrow as pa

from corvic import embed, op_graph, sql
from corvic.result import InternalError
from corvic.system.staging import StagingDB
from corvic_generated.orm.v1 import table_pb2


def _as_df(batch_reader: pa.RecordBatchReader | pa.RecordBatch):
    return cast(pl.DataFrame, pl.from_arrow(batch_reader, rechunk=False))


def _as_batch_reader(dataframe: pl.DataFrame):
    table = dataframe.to_arrow()
    return pa.RecordBatchReader.from_batches(table.schema, table.to_batches())


class InMemoryExecutor:
    """Executes op_graphs in memory (after staging queries)."""

    def __init__(self, staging_db: StagingDB):
        self._staging_db = staging_db

    def _staging_query_generator(self, blob_names: list[str], column_names: list[str]):
        return self._staging_db.query_for_blobs(blob_names, column_names)

    @classmethod
    def _is_sql_compatible(cls, op: op_graph.Op) -> bool:
        return isinstance(op, sql.SqlComputableOp) and all(
            cls._is_sql_compatible(sub_op) for sub_op in op.sources()
        )

    def _execute_rollup_by_aggregation(
        self, op: op_graph.op.RollupByAggregation
    ) -> pa.RecordBatchReader:
        raise NotImplementedError(
            "rollup by aggregation outside of sql not implemented"
        )

    def _execute_rename_columns(
        self, op: op_graph.op.RenameColumns
    ) -> pa.RecordBatchReader:
        return _as_batch_reader(
            _as_df(self.execute(op.source)).rename(dict(op.old_name_to_new))
        )

    def _execute_select_columns(self, op: op_graph.op.SelectColumns):
        return _as_batch_reader(_as_df(self.execute(op.source)).select(op.columns))

    def _execute_limit_rows(self, op: op_graph.op.LimitRows):
        return _as_batch_reader(_as_df(self.execute(op.source)).limit(op.num_rows))

    def _execute_filter_rows(self, op: op_graph.op.FilterRows) -> pa.RecordBatchReader:
        raise NotImplementedError("filter rows outside of sql not implemented")

    def _execute_distinct_rows(
        self, op: op_graph.op.DistinctRows
    ) -> pa.RecordBatchReader:
        return _as_batch_reader(_as_df(self.execute(op.source)).unique())

    def _execute_join(self, op: op_graph.op.Join) -> pa.RecordBatchReader:
        left_df = _as_df(self.execute(op.left_source))
        right_df = _as_df(self.execute(op.right_source))

        match op.how:
            case table_pb2.JOIN_TYPE_INNER:
                join_type = "inner"
            case table_pb2.JOIN_TYPE_LEFT_OUTER:
                join_type = "left"
            case _:
                join_type = "inner"

        # in our join semantics we drop columns from the right source on conflict
        right_df = right_df.select(
            [
                col
                for col in right_df.columns
                if col in op.right_join_columns or col not in left_df.columns
            ]
        )

        return _as_batch_reader(
            left_df.join(
                right_df,
                left_on=op.left_join_columns,
                right_on=op.right_join_columns,
                how=join_type,
            )
        )

    def _execute_empty(self, op: op_graph.op.Empty):
        empty_table = pa.schema([]).empty_table()
        return pa.RecordBatchReader.from_batches(
            empty_table.schema, empty_table.to_batches()
        )

    def _execute_embed_node2vec_from_edge_lists(
        self, op: op_graph.op.EmbedNode2vecFromEdgeLists
    ):
        def edge_generator():
            for edge_list in op.edge_list_tables:
                for batch in self.execute(edge_list.table):
                    yield (
                        _as_df(batch)
                        .with_columns(
                            pl.col(edge_list.start_column_name).alias("start_id"),
                            pl.lit(edge_list.start_entity_name).alias("start_source"),
                            pl.col(edge_list.end_column_name).alias("end_id"),
                            pl.lit(edge_list.end_entity_name).alias("end_source"),
                        )
                        .select("start_id", "start_source", "end_id", "end_source")
                    )

        n2v_space = embed.Space(
            pl.concat((edge_list for edge_list in edge_generator()), rechunk=False),
            start_id_column_names=("start_id", "start_source"),
            end_id_column_names=("end_id", "end_source"),
            directed=True,
        )
        n2v_runner = embed.Node2Vec(
            space=n2v_space,
            dim=op.ndim,
            walk_length=op.walk_length,
            window=op.window,
            p=op.p,
            q=op.q,
            alpha=op.alpha,
            min_alpha=op.min_alpha,
            negative=op.negative,
        )
        n2v_runner.train(epochs=op.epochs)
        return _as_batch_reader(
            pl.from_numpy(
                n2v_runner.wv.vectors,
                orient="row",
                schema=[f"dim_{i}" for i in range(op.ndim)],
            ).with_columns(
                pl.Series(name="identifier", values=n2v_runner.wv.index_to_key)
            )
        )

    def execute(self, op: op_graph.Op) -> pa.RecordBatchReader:  # noqa: PLR0911
        if self._is_sql_compatible(op):
            query = sql.parse_op_graph(op, self._staging_query_generator)
            return self._staging_db.run_select_query(query)

        match op:
            case op_graph.op.SelectFromStaging():
                raise InternalError("SelectFromStaging should always be lowered to sql")
            case op_graph.op.RenameColumns():
                return self._execute_rename_columns(op)
            case op_graph.op.Join():
                return self._execute_join(op)
            case op_graph.op.SelectColumns():
                return self._execute_select_columns(op)
            case op_graph.op.LimitRows():
                return self._execute_limit_rows(op)
            case op_graph.op.FilterRows():
                return self._execute_filter_rows(op)
            case op_graph.op.DistinctRows():
                return self._execute_distinct_rows(op)
            case (
                op_graph.op.SetMetadata()
                | op_graph.op.UpdateMetadata()
                | op_graph.op.RemoveFromMetadata()
                | op_graph.op.UpdateFeatureTypes()
            ):
                return self.execute(op.source)
            case op_graph.op.RollupByAggregation() as op:
                return self._execute_rollup_by_aggregation(op)
            case op_graph.op.Empty():
                return self._execute_empty(op)
            case op_graph.op.EmbedNode2vecFromEdgeLists():
                return self._execute_embed_node2vec_from_edge_lists(op)
