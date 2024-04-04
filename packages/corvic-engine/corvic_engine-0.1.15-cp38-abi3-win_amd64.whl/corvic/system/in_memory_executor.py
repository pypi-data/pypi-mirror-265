"""Staging-agnostic in-memory executor."""

from typing import cast

import polars as pl
import pyarrow as pa
import pyarrow.parquet as pq

from corvic import embed, op_graph, sql
from corvic.result import InternalError
from corvic.system.op_graph_executor import ExecutionContext
from corvic.system.staging import StagingDB
from corvic.system.storage import StorageManager
from corvic_generated.orm.v1 import table_pb2


def _as_df(batch_reader: pa.RecordBatchReader | pa.RecordBatch):
    return cast(pl.DataFrame, pl.from_arrow(batch_reader, rechunk=False))


def _as_batch_reader(dataframe: pl.DataFrame):
    table = dataframe.to_arrow()
    return pa.RecordBatchReader.from_batches(table.schema, table.to_batches())


class InMemoryExecutionResult:
    """A container for in-memory results.

    This container is optimized to avoid writes to disk, i.e., `to_batch_reader` will
    be fast `to_urls` will be slow.
    """

    def __init__(
        self,
        storage_manager: StorageManager,
        schema: pa.Schema,
        batches: list[pa.RecordBatch],
        context: ExecutionContext,
    ):
        self._storage_manager = storage_manager
        self._schema = schema
        self._batches = batches
        self._context = context

    def to_batch_reader(self) -> pa.RecordBatchReader:
        return pa.RecordBatchReader.from_batches(self._schema, self._batches)

    def to_urls(self) -> list[str]:
        # one file for now; we may produce more in the future
        file_idx = 0
        file_name = f"{self._context.output_url_prefix}.{file_idx:>06}"
        with (
            self._storage_manager.blob_from_url(file_name).open("wb") as stream,
            pq.ParquetWriter(stream, self._schema) as writer,
        ):
            for batch in self._batches:
                writer.write_batch(batch)

        return [file_name]


class InMemoryExecutor:
    """Executes op_graphs in memory (after staging queries)."""

    def __init__(self, staging_db: StagingDB, storage_manager: StorageManager):
        self._staging_db = staging_db
        self._storage_manager = storage_manager

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
            _as_df(self._execute(op.source)).rename(dict(op.old_name_to_new))
        )

    def _execute_select_columns(self, op: op_graph.op.SelectColumns):
        return _as_batch_reader(_as_df(self._execute(op.source)).select(op.columns))

    def _execute_limit_rows(self, op: op_graph.op.LimitRows):
        return _as_batch_reader(_as_df(self._execute(op.source)).limit(op.num_rows))

    def _execute_filter_rows(self, op: op_graph.op.FilterRows) -> pa.RecordBatchReader:
        raise NotImplementedError("filter rows outside of sql not implemented")

    def _execute_distinct_rows(
        self, op: op_graph.op.DistinctRows
    ) -> pa.RecordBatchReader:
        return _as_batch_reader(_as_df(self._execute(op.source)).unique())

    def _execute_join(self, op: op_graph.op.Join) -> pa.RecordBatchReader:
        left_df = _as_df(self._execute(op.left_source))
        right_df = _as_df(self._execute(op.right_source))

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
                for batch in self._execute(edge_list.table):
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

    def _execute(self, op: op_graph.Op) -> pa.RecordBatchReader:  # noqa: PLR0911
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
                return self._execute(op.source)
            case op_graph.op.RollupByAggregation() as op:
                return self._execute_rollup_by_aggregation(op)
            case op_graph.op.Empty():
                return self._execute_empty(op)
            case op_graph.op.EmbedNode2vecFromEdgeLists():
                return self._execute_embed_node2vec_from_edge_lists(op)

    def execute(self, context: ExecutionContext) -> InMemoryExecutionResult:
        reader = self._execute(context.table_to_compute)
        return InMemoryExecutionResult(
            self._storage_manager, reader.schema, list(reader), context
        )
