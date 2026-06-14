select
    member_id,
    studio_id,
    gender,
    age,
    membership_tier,
    monthly_rate,
    join_date,
    cancel_date,
    is_churned
from {{ ref('stg_members') }}