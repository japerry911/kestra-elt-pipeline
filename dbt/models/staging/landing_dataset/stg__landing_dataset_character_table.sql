with dedupped as (
    select *
    from {{ source("landing_dataset", "character_table") }}
    {{ qualify_partition_by(partitions="id", order_by="run_datetime") }}
)

select *
from dedupped
