{#
    Generates a QUALIFY clause with ROW_NUMBER() for deduplication of records.

    This macro creates a SQL statement that keeps only the first row within each partition
    when records are sorted by the specified order column.

    Args:
        partitions: Comma-separated list of columns to partition the data by
        order_by: Column name to sort records within each partition (in descending order)
#}
{% macro qualify_partition_by(partitions, order_by) %}
qualify row_number() over (partition by {{ partitions }} order by {{ order_by }} desc) = 1
{% endmacro %}