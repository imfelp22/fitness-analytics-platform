select
    studio_id,
    studio_name,
    city,
    state,
    region,
    opening_date
from {{ ref('stg_studios') }}