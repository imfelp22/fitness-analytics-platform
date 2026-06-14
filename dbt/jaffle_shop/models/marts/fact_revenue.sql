select
    transaction_id,
    member_id,
    studio_id,
    transaction_date,
    revenue_type,
    amount
from {{ ref('stg_revenue') }}