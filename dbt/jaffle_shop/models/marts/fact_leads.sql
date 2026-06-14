select
    lead_id,
    studio_id,
    lead_date,
    lead_source,
    converted,
    lead_score
from {{ ref('stg_leads') }}