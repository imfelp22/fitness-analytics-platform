select
    attendance_id,
    member_id,
    studio_id,
    attendance_date,
    class_type
from {{ ref('stg_attendance') }}