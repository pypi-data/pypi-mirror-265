from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any
from typing import Iterable
from typing import Literal
from typing import Sequence

from narwhals.dtypes import to_narwhals_dtype
from narwhals.pandas_like.dataframe import PandasDataFrame
from narwhals.translate import get_cudf
from narwhals.translate import get_modin
from narwhals.translate import get_pandas
from narwhals.translate import get_polars

if TYPE_CHECKING:
    from typing_extensions import Self

    from narwhals.dtypes import DType
    from narwhals.group_by import GroupBy
    from narwhals.series import Series
    from narwhals.typing import IntoExpr


class BaseFrame:
    _dataframe: Any
    _implementation: str

    def _from_dataframe(self, df: Any) -> Self:
        # construct, preserving properties
        return self.__class__(  # type: ignore[call-arg]
            df,
            implementation=self._implementation,
        )

    def _flatten_and_extract(self, *args: Any, **kwargs: Any) -> Any:
        from narwhals.utils import flatten

        args = [self._extract_native(v) for v in flatten(args)]  # type: ignore[assignment]
        kwargs = {k: self._extract_native(v) for k, v in kwargs.items()}
        return args, kwargs

    def _extract_native(self, arg: Any) -> Any:
        from narwhals.expression import Expr
        from narwhals.pandas_like.namespace import PandasNamespace
        from narwhals.series import Series

        if isinstance(arg, BaseFrame):
            return arg._dataframe
        if isinstance(arg, Series):
            return arg._series
        if isinstance(arg, Expr):
            if self._implementation == "polars":
                import polars as pl

                return arg._call(pl)
            plx = PandasNamespace(implementation=self._implementation)
            return arg._call(plx)
        return arg

    def __repr__(self) -> str:  # pragma: no cover
        header = " Narwhals DataFrame                              "
        length = len(header)
        return (
            "┌"
            + "─" * length
            + "┐\n"
            + f"|{header}|\n"
            + "| Use `narwhals.to_native()` to see native output |\n"
            + "└"
            + "─" * length
            + "┘"
        )

    @property
    def schema(self) -> dict[str, DType]:
        return {
            k: to_narwhals_dtype(v, self._implementation)
            for k, v in self._dataframe.schema.items()
        }

    @property
    def columns(self) -> list[str]:
        return self._dataframe.columns  # type: ignore[no-any-return]

    def with_columns(
        self, *exprs: IntoExpr | Iterable[IntoExpr], **named_exprs: IntoExpr
    ) -> Self:
        exprs, named_exprs = self._flatten_and_extract(*exprs, **named_exprs)
        return self._from_dataframe(
            self._dataframe.with_columns(*exprs, **named_exprs),
        )

    def select(
        self,
        *exprs: IntoExpr | Iterable[IntoExpr],
        **named_exprs: IntoExpr,
    ) -> Self:
        exprs, named_exprs = self._flatten_and_extract(*exprs, **named_exprs)
        return self._from_dataframe(
            self._dataframe.select(*exprs, **named_exprs),
        )

    def rename(self, mapping: dict[str, str]) -> Self:
        return self._from_dataframe(self._dataframe.rename(mapping))

    def head(self, n: int) -> Self:
        return self._from_dataframe(self._dataframe.head(n))

    def drop(self, *columns: str | Iterable[str]) -> Self:
        return self._from_dataframe(self._dataframe.drop(*columns))

    def unique(self, subset: str | list[str]) -> Self:
        return self._from_dataframe(self._dataframe.unique(subset=subset))

    def filter(self, *predicates: IntoExpr | Iterable[IntoExpr]) -> Self:
        predicates, _ = self._flatten_and_extract(*predicates)
        return self._from_dataframe(
            self._dataframe.filter(*predicates),
        )

    def group_by(self, *keys: str | Iterable[str]) -> GroupBy:
        from narwhals.group_by import GroupBy

        # todo: groupby and lazygroupby
        return GroupBy(self, *keys)  # type: ignore[arg-type]

    def sort(
        self,
        by: str | Iterable[str],
        *more_by: str,
        descending: bool | Sequence[bool] = False,
    ) -> Self:
        return self._from_dataframe(
            self._dataframe.sort(by, *more_by, descending=descending)
        )

    def join(
        self,
        other: Self,
        *,
        how: Literal["inner"] = "inner",
        left_on: str | list[str],
        right_on: str | list[str],
    ) -> Self:
        return self._from_dataframe(
            self._dataframe.join(
                self._extract_native(other),
                how=how,
                left_on=left_on,
                right_on=right_on,
            )
        )


class DataFrame(BaseFrame):
    def __init__(
        self,
        df: Any,
        *,
        implementation: str | None = None,
    ) -> None:
        if implementation is not None:
            self._dataframe: Any = df
            self._implementation = implementation
            return
        if (pl := get_polars()) is not None and isinstance(df, pl.DataFrame):
            self._dataframe = df
            self._implementation = "polars"
        elif (pl := get_polars()) is not None and isinstance(df, pl.LazyFrame):
            raise TypeError(
                "Can't instantiate DataFrame from Polars LazyFrame. Call `collect()` first, or use `narwhals.LazyFrame` if you don't specifically require eager execution."
            )
        elif (pd := get_pandas()) is not None and isinstance(df, pd.DataFrame):
            self._dataframe = PandasDataFrame(df, implementation="pandas")
            self._implementation = "pandas"
        elif (mpd := get_modin()) is not None and isinstance(
            df, mpd.DataFrame
        ):  # pragma: no cover
            self._dataframe = PandasDataFrame(df, implementation="modin")
            self._implementation = "modin"
        elif (cudf := get_cudf()) is not None and isinstance(
            df, cudf.DataFrame
        ):  # pragma: no cover
            self._dataframe = PandasDataFrame(df, implementation="cudf")
            self._implementation = "cudf"
        elif hasattr(df, "__narwhals_dataframe__"):  # pragma: no cover
            self._dataframe = df.__narwhals_dataframe__()
            self._implementation = "custom"
        else:
            msg = f"Expected pandas-like dataframe, Polars dataframe, or Polars lazyframe, got: {type(df)}"
            raise TypeError(msg)

    def to_pandas(self) -> Any:
        return self._dataframe.to_pandas()

    def to_numpy(self) -> Any:
        return self._dataframe.to_numpy()

    @property
    def shape(self) -> tuple[int, int]:
        return self._dataframe.shape  # type: ignore[no-any-return]

    def __getitem__(self, col_name: str) -> Series:
        from narwhals.series import Series

        return Series(self._dataframe[col_name], implementation=self._implementation)

    def to_dict(self, *, as_series: bool = True) -> dict[str, Any]:
        return self._dataframe.to_dict(as_series=as_series)  # type: ignore[no-any-return]

    # inherited
    @property
    def schema(self) -> dict[str, DType]:
        r"""
        Get a dict[column name, DataType].

        Examples:
            >>> import polars as pl
            >>> import narwhals as nw
            >>> df_pl = pl.DataFrame(
            ...     {
            ...         "foo": [1, 2, 3],
            ...         "bar": [6.0, 7.0, 8.0],
            ...         "ham": ["a", "b", "c"],
            ...     }
            ... )
            >>> df = nw.DataFrame(df_pl)
            >>> df.schema  # doctest: +SKIP
            OrderedDict({'foo': Int64, 'bar': Float64, 'ham': String})
            ```
        """
        return super().schema

    @property
    def columns(self) -> list[str]:
        r"""
        Get column names.

        Examples:
            Get column names.

            >>> import polars as pl
            >>> import narwhals as nw
            >>> df_pl = pl.DataFrame(
            ...     {
            ...         "foo": [1, 2, 3],
            ...         "bar": [6, 7, 8],
            ...         "ham": ["a", "b", "c"],
            ...     }
            ... )
            >>> df = nw.DataFrame(df_pl)
            >>> df.columns
            ['foo', 'bar', 'ham']
        """
        return super().columns

    def with_columns(
        self, *exprs: IntoExpr | Iterable[IntoExpr], **named_exprs: IntoExpr
    ) -> Self:
        r"""
        Add columns to this DataFrame.

        Added columns will replace existing columns with the same name.

        Arguments:
            *exprs: Column(s) to add, specified as positional arguments.
                     Accepts expression input. Strings are parsed as column names, other
                     non-expression inputs are parsed as literals.

            **named_exprs: Additional columns to add, specified as keyword arguments.
                            The columns will be renamed to the keyword used.

        Returns:
            DataFrame: A new DataFrame with the columns added.

        Note:
            Creating a new DataFrame using this method does not create a new copy of
            existing data.

        Examples:
            Pass an expression to add it as a new column.

            >>> import polars as pl
            >>> import narwhals as nw
            >>> df_pl = pl.DataFrame(
            ...     {
            ...         "a": [1, 2, 3, 4],
            ...         "b": [0.5, 4, 10, 13],
            ...         "c": [True, True, False, True],
            ...     }
            ... )
            >>> df = nw.DataFrame(df_pl)
            >>> dframe = df.with_columns((nw.col("a") * 2).alias("a*2"))
            >>> dframe
            ┌─────────────────────────────────────────────────┐
            | Narwhals DataFrame                              |
            | Use `narwhals.to_native()` to see native output |
            └─────────────────────────────────────────────────┘

            >>> nw.to_native(dframe)
            shape: (4, 4)
            ┌─────┬──────┬───────┬─────┐
            │ a   ┆ b    ┆ c     ┆ a*2 │
            │ --- ┆ ---  ┆ ---   ┆ --- │
            │ i64 ┆ f64  ┆ bool  ┆ i64 │
            ╞═════╪══════╪═══════╪═════╡
            │ 1   ┆ 0.5  ┆ true  ┆ 2   │
            │ 2   ┆ 4.0  ┆ true  ┆ 4   │
            │ 3   ┆ 10.0 ┆ false ┆ 6   │
            │ 4   ┆ 13.0 ┆ true  ┆ 8   │
            └─────┴──────┴───────┴─────┘
        """
        return super().with_columns(*exprs, **named_exprs)

    def select(
        self,
        *exprs: IntoExpr | Iterable[IntoExpr],
        **named_exprs: IntoExpr,
    ) -> Self:
        r"""
        Select columns from this DataFrame.

        Arguments:
            *exprs: Column(s) to select, specified as positional arguments.
                     Accepts expression input. Strings are parsed as column names,
                     other non-expression inputs are parsed as literals.

            **named_exprs: Additional columns to select, specified as keyword arguments.
                            The columns will be renamed to the keyword used.

        Examples:
            Pass the name of a column to select that column.

            >>> import polars as pl
            >>> import narwhals as nw
            >>> df_pl = pl.DataFrame(
            ...     {
            ...         "foo": [1, 2, 3],
            ...         "bar": [6, 7, 8],
            ...         "ham": ["a", "b", "c"],
            ...     }
            ... )
            >>> df = nw.DataFrame(df_pl)
            >>> dframe = df.select("foo")
            >>> dframe
            ┌─────────────────────────────────────────────────┐
            | Narwhals DataFrame                              |
            | Use `narwhals.to_native()` to see native output |
            └─────────────────────────────────────────────────┘
            >>> nw.to_native(dframe)
            shape: (3, 1)
            ┌─────┐
            │ foo │
            │ --- │
            │ i64 │
            ╞═════╡
            │ 1   │
            │ 2   │
            │ 3   │
            └─────┘

            Multiple columns can be selected by passing a list of column names.

            >>> dframe = df.select(["foo", "bar"])
            >>> dframe
            ┌─────────────────────────────────────────────────┐
            | Narwhals DataFrame                              |
            | Use `narwhals.to_native()` to see native output |
            └─────────────────────────────────────────────────┘
            >>> nw.to_native(dframe)
            shape: (3, 2)
            ┌─────┬─────┐
            │ foo ┆ bar │
            │ --- ┆ --- │
            │ i64 ┆ i64 │
            ╞═════╪═════╡
            │ 1   ┆ 6   │
            │ 2   ┆ 7   │
            │ 3   ┆ 8   │
            └─────┴─────┘

            Multiple columns can also be selected using positional arguments instead of a
            list. Expressions are also accepted.

            >>> dframe = df.select(nw.col("foo"), nw.col("bar") + 1)
            >>> dframe
            ┌─────────────────────────────────────────────────┐
            | Narwhals DataFrame                              |
            | Use `narwhals.to_native()` to see native output |
            └─────────────────────────────────────────────────┘
            >>> nw.to_native(dframe)
            shape: (3, 2)
            ┌─────┬─────┐
            │ foo ┆ bar │
            │ --- ┆ --- │
            │ i64 ┆ i64 │
            ╞═════╪═════╡
            │ 1   ┆ 7   │
            │ 2   ┆ 8   │
            │ 3   ┆ 9   │
            └─────┴─────┘

            Use keyword arguments to easily name your expression inputs.

            >>> dframe = df.select(threshold=nw.col('foo')*2)
            >>> dframe
            ┌─────────────────────────────────────────────────┐
            | Narwhals DataFrame                              |
            | Use `narwhals.to_native()` to see native output |
            └─────────────────────────────────────────────────┘
            >>> nw.to_native(dframe)
            shape: (3, 1)
            ┌───────────┐
            │ threshold │
            │ ---       │
            │ i64       │
            ╞═══════════╡
            │ 2         │
            │ 4         │
            │ 6         │
            └───────────┘
        """
        return super().select(*exprs, **named_exprs)

    def rename(self, mapping: dict[str, str]) -> Self:
        r"""
        Rename column names.

        Arguments:
            mapping: Key value pairs that map from old name to new name, or a function
                      that takes the old name as input and returns the new name.

        Examples:
            >>> import polars as pl
            >>> import narwhals as nw
            >>> df_pl = pl.DataFrame(
            ...     {"foo": [1, 2, 3], "bar": [6, 7, 8], "ham": ["a", "b", "c"]}
            ... )
            >>> df = nw.DataFrame(df_pl)
            >>> dframe = df.rename({"foo": "apple"})
            >>> dframe
            ┌─────────────────────────────────────────────────┐
            | Narwhals DataFrame                              |
            | Use `narwhals.to_native()` to see native output |
            └─────────────────────────────────────────────────┘

            >>> nw.to_native(dframe)
            shape: (3, 3)
            ┌───────┬─────┬─────┐
            │ apple ┆ bar ┆ ham │
            │ ---   ┆ --- ┆ --- │
            │ i64   ┆ i64 ┆ str │
            ╞═══════╪═════╪═════╡
            │ 1     ┆ 6   ┆ a   │
            │ 2     ┆ 7   ┆ b   │
            │ 3     ┆ 8   ┆ c   │
            └───────┴─────┴─────┘
            >>> dframe = df.rename(lambda column_name: "f" + column_name[1:])
            >>> dframe
            ┌─────────────────────────────────────────────────┐
            | Narwhals DataFrame                              |
            | Use `narwhals.to_native()` to see native output |
            └─────────────────────────────────────────────────┘
            >>> nw.to_native(dframe)
            shape: (3, 3)
            ┌─────┬─────┬─────┐
            │ foo ┆ far ┆ fam │
            │ --- ┆ --- ┆ --- │
            │ i64 ┆ i64 ┆ str │
            ╞═════╪═════╪═════╡
            │ 1   ┆ 6   ┆ a   │
            │ 2   ┆ 7   ┆ b   │
            │ 3   ┆ 8   ┆ c   │
            └─────┴─────┴─────┘
        """
        return super().rename(mapping)

    def head(self, n: int) -> Self:
        return super().head(n)

    def drop(self, *columns: str | Iterable[str]) -> Self:
        return super().drop(*columns)

    def unique(self, subset: str | list[str]) -> Self:
        return super().unique(subset)

    def filter(self, *predicates: IntoExpr | Iterable[IntoExpr]) -> Self:
        return super().filter(*predicates)

    def group_by(self, *keys: str | Iterable[str]) -> GroupBy:
        from narwhals.group_by import GroupBy

        # todo: groupby and lazygroupby
        return GroupBy(self, *keys)

    def sort(
        self,
        by: str | Iterable[str],
        *more_by: str,
        descending: bool | Sequence[bool] = False,
    ) -> Self:
        return super().sort(by, *more_by, descending=descending)

    def join(
        self,
        other: Self,
        *,
        how: Literal["inner"] = "inner",
        left_on: str | list[str],
        right_on: str | list[str],
    ) -> Self:
        return self._from_dataframe(
            self._dataframe.join(
                self._extract_native(other),
                how=how,
                left_on=left_on,
                right_on=right_on,
            )
        )


class LazyFrame(BaseFrame):
    def __init__(
        self,
        df: Any,
        *,
        implementation: str | None = None,
    ) -> None:
        if implementation is not None:
            self._dataframe: Any = df
            self._implementation = implementation
            return
        if (pl := get_polars()) is not None and isinstance(
            df, (pl.DataFrame, pl.LazyFrame)
        ):
            self._dataframe = df.lazy()
            self._implementation = "polars"
        elif (pd := get_pandas()) is not None and isinstance(df, pd.DataFrame):
            self._dataframe = PandasDataFrame(df, implementation="pandas")
            self._implementation = "pandas"
        elif (mpd := get_modin()) is not None and isinstance(
            df, mpd.DataFrame
        ):  # pragma: no cover
            self._dataframe = PandasDataFrame(df, implementation="modin")
            self._implementation = "modin"
        elif (cudf := get_cudf()) is not None and isinstance(
            df, cudf.DataFrame
        ):  # pragma: no cover
            self._dataframe = PandasDataFrame(df, implementation="cudf")
            self._implementation = "cudf"
        else:
            msg = f"Expected pandas-like dataframe, Polars dataframe, or Polars lazyframe, got: {type(df)}"
            raise TypeError(msg)

    def collect(self) -> DataFrame:
        return DataFrame(
            self._dataframe.collect(),
            implementation=self._implementation,
        )

    # inherited
    @property
    def schema(self) -> dict[str, DType]:
        return super().schema

    @property
    def columns(self) -> list[str]:
        return super().columns

    def with_columns(
        self, *exprs: IntoExpr | Iterable[IntoExpr], **named_exprs: IntoExpr
    ) -> Self:
        return super().with_columns(*exprs, **named_exprs)

    def select(
        self,
        *exprs: IntoExpr | Iterable[IntoExpr],
        **named_exprs: IntoExpr,
    ) -> Self:
        return super().select(*exprs, **named_exprs)

    def rename(self, mapping: dict[str, str]) -> Self:
        return super().rename(mapping)

    def head(self, n: int) -> Self:
        return super().head(n)

    def drop(self, *columns: str | Iterable[str]) -> Self:
        return super().drop(*columns)

    def unique(self, subset: str | list[str]) -> Self:
        return super().unique(subset)

    def filter(self, *predicates: IntoExpr | Iterable[IntoExpr]) -> Self:
        return super().filter(*predicates)

    def group_by(self, *keys: str | Iterable[str]) -> GroupBy:
        from narwhals.group_by import GroupBy

        # todo: groupby and lazygroupby
        return GroupBy(self, *keys)

    def sort(
        self,
        by: str | Iterable[str],
        *more_by: str,
        descending: bool | Sequence[bool] = False,
    ) -> Self:
        return super().sort(by, *more_by, descending=descending)

    def join(
        self,
        other: Self,
        *,
        how: Literal["inner"] = "inner",
        left_on: str | list[str],
        right_on: str | list[str],
    ) -> Self:
        return self._from_dataframe(
            self._dataframe.join(
                self._extract_native(other),
                how=how,
                left_on=left_on,
                right_on=right_on,
            )
        )
