import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

np.random.seed(42)

# ==========================================================
# CONFIG
# ==========================================================

NUM_STUDIOS = 100
NUM_MEMBERS = 50000
NUM_LEADS = 20000
NUM_ATTENDANCE = 500000
NUM_REVENUE = 200000

START_DATE = datetime.today() - timedelta(days=730)
END_DATE = datetime.today()

# ==========================================================
# STUDIO DATA
# ==========================================================

cities = [
    ("Miami", "FL"),
    ("Orlando", "FL"),
    ("Tampa", "FL"),
    ("Atlanta", "GA"),
    ("Charlotte", "NC"),
    ("Nashville", "TN"),
    ("Dallas", "TX"),
    ("Austin", "TX"),
    ("Houston", "TX"),
    ("Phoenix", "AZ"),
    ("Denver", "CO"),
    ("Chicago", "IL"),
    ("Boston", "MA"),
    ("Seattle", "WA"),
    ("San Diego", "CA"),
    ("Los Angeles", "CA"),
    ("San Francisco", "CA"),
    ("Las Vegas", "NV"),
    ("New York", "NY"),
    ("Philadelphia", "PA")
]

studios = []

for studio_id in range(1, NUM_STUDIOS + 1):
    city, state = cities[np.random.randint(len(cities))]

    studios.append({
        "studio_id": studio_id,
        "studio_name": f"FitLife Studio {studio_id}",
        "city": city,
        "state": state,
        "region": np.random.choice(
            ["Northeast", "South", "Midwest", "West"],
            p=[0.25, 0.35, 0.20, 0.20]
        ),
        "opening_date": fake.date_between(
            start_date="-10y",
            end_date="-1y"
        )
    })

studios_df = pd.DataFrame(studios)

# ==========================================================
# MEMBERS
# ==========================================================

membership_tiers = {
    "Basic": 49,
    "Premium": 89,
    "Elite": 139
}

tier_probs = [0.50, 0.35, 0.15]

members = []

for member_id in range(1, NUM_MEMBERS + 1):

    join_date = fake.date_between(
        start_date=START_DATE,
        end_date=END_DATE
    )

    tier = np.random.choice(
        list(membership_tiers.keys()),
        p=tier_probs
    )

    churned = np.random.choice(
        [0, 1],
        p=[0.72, 0.28]
    )

    cancel_date = None

    if churned:
        cancel_date = fake.date_between(
            start_date=join_date,
            end_date=END_DATE
        )

    members.append({
        "member_id": member_id,
        "studio_id": np.random.randint(1, NUM_STUDIOS + 1),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "gender": np.random.choice(
            ["Male", "Female", "Other"],
            p=[0.47, 0.50, 0.03]
        ),
        "age": np.random.randint(18, 70),
        "membership_tier": tier,
        "monthly_rate": membership_tiers[tier],
        "join_date": join_date,
        "cancel_date": cancel_date,
        "is_churned": churned
    })

members_df = pd.DataFrame(members)

# ==========================================================
# LEADS
# ==========================================================

lead_sources = [
    "Google Ads",
    "Facebook",
    "Instagram",
    "Referral",
    "Walk-In",
    "Email Campaign",
    "TikTok",
    "Corporate Partnership"
]

source_probs = [
    0.25,
    0.20,
    0.15,
    0.15,
    0.10,
    0.05,
    0.05,
    0.05
]

leads = []

for lead_id in range(1, NUM_LEADS + 1):

    lead_date = fake.date_between(
        start_date=START_DATE,
        end_date=END_DATE
    )

    converted = np.random.choice(
        [0, 1],
        p=[0.65, 0.35]
    )

    leads.append({
        "lead_id": lead_id,
        "studio_id": np.random.randint(1, NUM_STUDIOS + 1),
        "lead_date": lead_date,
        "lead_source": np.random.choice(
            lead_sources,
            p=source_probs
        ),
        "converted": converted,
        "lead_score": np.random.randint(20, 100)
    })

leads_df = pd.DataFrame(leads)

# ==========================================================
# ATTENDANCE
# ==========================================================

attendance = []

member_ids = members_df["member_id"].values

for attendance_id in range(1, NUM_ATTENDANCE + 1):

    member = members_df.sample(1).iloc[0]

    attendance.append({
        "attendance_id": attendance_id,
        "member_id": member.member_id,
        "studio_id": member.studio_id,
        "attendance_date": fake.date_between(
            start_date=max(
                member.join_date,
                START_DATE.date()
            ),
            end_date=END_DATE
        ),
        "class_type": np.random.choice([
            "HIIT",
            "Strength",
            "Yoga",
            "Cardio",
            "Cycle",
            "Bootcamp"
        ])
    })

attendance_df = pd.DataFrame(attendance)

# ==========================================================
# REVENUE
# ==========================================================

revenue_types = [
    "Membership",
    "Personal Training",
    "Retail",
    "Drop-In",
    "Nutrition"
]

revenue = []

for txn_id in range(1, NUM_REVENUE + 1):

    member = members_df.sample(1).iloc[0]

    txn_type = np.random.choice(
        revenue_types,
        p=[0.70, 0.12, 0.06, 0.07, 0.05]
    )

    if txn_type == "Membership":
        amount = member.monthly_rate

    elif txn_type == "Personal Training":
        amount = round(
            np.random.normal(120, 25),
            2
        )

    elif txn_type == "Retail":
        amount = round(
            np.random.normal(45, 15),
            2
        )

    elif txn_type == "Drop-In":
        amount = round(
            np.random.normal(25, 5),
            2
        )

    else:
        amount = round(
            np.random.normal(65, 15),
            2
        )

    amount = max(amount, 10)

    revenue.append({
        "transaction_id": txn_id,
        "member_id": member.member_id,
        "studio_id": member.studio_id,
        "transaction_date": fake.date_between(
            start_date=max(
                member.join_date,
                START_DATE.date()
            ),
            end_date=END_DATE
        ),
        "revenue_type": txn_type,
        "amount": amount
    })

revenue_df = pd.DataFrame(revenue)

# ==========================================================
# EXPORT
# ==========================================================

studios_df.to_csv("studios.csv", index=False)
members_df.to_csv("members.csv", index=False)
leads_df.to_csv("leads.csv", index=False)
attendance_df.to_csv("attendance.csv", index=False)
revenue_df.to_csv("revenue.csv", index=False)

print("Files created:")
print("studios.csv")
print("members.csv")
print("leads.csv")
print("attendance.csv")
print("revenue.csv")