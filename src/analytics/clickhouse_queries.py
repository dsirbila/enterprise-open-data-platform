"""lecture 23: ClickHouse query-ების აგება და შედეგის ფორმატირება —
testable, clickhouse_connect-ისგან დამოუკიდებელი."""

VALID_AGGS = {"avg", "min", "max", "sum", "count"}


class QueryBuildError(Exception):
    """query-ის აგებისას წარმოქმნილი ვალიდაციის შეცდომა."""


def build_daily_aggregation_query(
    table: str, date_col: str, value_col: str, agg_func: str = "avg"
) -> str:
    if agg_func not in VALID_AGGS:
        raise QueryBuildError(
            f"უცნობი aggregation function: '{agg_func}' (დაშვებულია: {VALID_AGGS})"
        )

    return (
        f"SELECT toDate({date_col}) AS day, {agg_func}({value_col}) AS result "
        f"FROM {table} "
        f"GROUP BY day "
        f"ORDER BY day"
    )


def format_query_result(rows: list, columns: list) -> str:
    """query შედეგებს (row tuples-ს) ფორმატირებულ ცხრილად აქცევს, ტერმინალში საჩვენებლად."""
    if not rows:
        return "(ცარიელი შედეგი)"

    widths = [
        max(len(str(col)), max(len(str(row[i])) for row in rows))
        for i, col in enumerate(columns)
    ]
    header = " | ".join(str(col).ljust(w) for col, w in zip(columns, widths))
    separator = "-+-".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        lines.append(" | ".join(str(val).ljust(w) for val, w in zip(row, widths)))
    return "\n".join(lines)
