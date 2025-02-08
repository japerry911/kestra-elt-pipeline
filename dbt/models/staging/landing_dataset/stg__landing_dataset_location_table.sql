with dedupped as (
    select *
    from {{ source("landing_dataset", "location_table") }}
    {{ qualify_partition_by(partitions="id", order_by="run_datetime") }}
)

select *
from dedupped
