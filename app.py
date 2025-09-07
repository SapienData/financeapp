import streamlit as st
import pandas as pd

# Expanded mock claims data with more fields
claims_data = [
    {"claim_id": "C001", "claim_type": "Auto", "amount": 5000, "fraud_risk": 0.1, "status": "Pending",
     "claimant_age": 34, "location": "Dubai", "days_to_settle": 10},
    {"claim_id": "C002", "claim_type": "Home", "amount": 12000, "fraud_risk": 0.4, "status": "Pending",
     "claimant_age": 58, "location": "Riyadh", "days_to_settle": 25},
    {"claim_id": "C003", "claim_type": "Health", "amount": 3000, "fraud_risk": 0.05, "status": "Approved",
     "claimant_age": 48, "location": "Doha", "days_to_settle": 7},
    {"claim_id": "C004", "claim_type": "Auto", "amount": 8000, "fraud_risk": 0.8, "status": "Pending",
     "claimant_age": 27, "location": "Manama", "days_to_settle": 15},
    {"claim_id": "C005", "claim_type": "Travel", "amount": 1500, "fraud_risk": 0.2, "status": "Pending",
     "claimant_age": 42, "location": "Muscat", "days_to_settle": 5},
]

df_claims = pd.DataFrame(claims_data)

def evaluate_fraud_risk(row):
    return "High Risk - Manual Review" if row["fraud_risk"] > 0.5 else "Low Risk - Auto Approve"

def assess_claim_amount(row):
    return "High Claim - Further Assessment" if row["amount"] > 10000 else "Standard Claim"

# Bright color mappings for better differentiation
def color_risk(val):
    return "color: #ff0000; font-weight: bold" if "High" in val else "color: #00cc00; font-weight: bold"

def color_assessment(val):
    return "color: #ff9900; font-weight: bold" if "High" in val else "color: #0066ff; font-weight: bold"

def color_status(val):
    colors = {
        "Pending": "background-color: #fff176; color: black; font-weight: bold",
        "Approved": "background-color: #81c784; color: black; font-weight: bold",
        "Rejected": "background-color: #e57373; color: black; font-weight: bold",
    }
    return colors.get(val, "")

# Add evaluations to dataframe
df_claims["Fraud_Evaluation"] = df_claims.apply(evaluate_fraud_risk, axis=1)
df_claims["Claim_Assessment"] = df_claims.apply(assess_claim_amount, axis=1)

# Sidebar for filtering
st.sidebar.title("Filter Claims")
claim_types = df_claims["claim_type"].unique().tolist()
selected_types = st.sidebar.multiselect("Claim Types", options=claim_types, default=claim_types)
statuses = df_claims["status"].unique().tolist()
selected_statuses = st.sidebar.multiselect("Claim Status", options=statuses, default=statuses)

filtered_claims = df_claims[
    (df_claims["claim_type"].isin(selected_types)) & (df_claims["status"].isin(selected_statuses))
]

st.title("Agentic AI Insurance Claims Dashboard")

# Summary metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Claims", len(df_claims))
col2.metric("High Risk Claims", sum(df_claims["Fraud_Evaluation"] == "High Risk - Manual Review"))
col3.metric("High Amount Claims", sum(df_claims["Claim_Assessment"] == "High Claim - Further Assessment"))

st.markdown("---")

st.write("### Claims Overview")

# Display filtered data with styling and bright colors
st.dataframe(
    filtered_claims.style
    .applymap(color_risk, subset=["Fraud_Evaluation"])
    .applymap(color_assessment, subset=["Claim_Assessment"])
    .applymap(color_status, subset=["status"])
    .format({"amount": "${:,.2f}"})
)

st.markdown("---")

st.write("### Claim Details and Actions")

claim_id = st.selectbox("Select Claim ID to process", filtered_claims["claim_id"].tolist())

selected_claim = df_claims[df_claims["claim_id"] == claim_id].iloc[0]

# Display details neatly in columns
col1, col2 = st.columns(2)
col1.subheader("Claim Info")
col1.write(f"**Claim ID:** {selected_claim['claim_id']}")
col1.write(f"**Type:** {selected_claim['claim_type']}")
col1.write(f"**Amount:** ${selected_claim['amount']:,.2f}")
col1.write(f"**Status:** {selected_claim['status']}")
col1.write(f"**Claimant Age:** {selected_claim['claimant_age']}")
col1.write(f"**Location:** {selected_claim['location']}")
col1.write(f"**Days to Settle:** {selected_claim['days_to_settle']}")

col2.subheader("AI Assessments")
col2.write(f"**Fraud Risk:** {selected_claim['fraud_risk']:.2f}")
col2.write(f"**Fraud Evaluation:** {selected_claim['Fraud_Evaluation']}")
col2.write(f"**Claim Assessment:** {selected_claim['Claim_Assessment']}")

# Action buttons with feedback
if st.button("Approve Claim Automatically"):
    if selected_claim["Fraud_Evaluation"] == "Low Risk - Auto Approve":
        st.success("Claim Approved Automatically.")
    else:
        st.error("Claim flagged for manual review. Auto-approval not allowed.")

if st.button("Flag for Manual Review"):
    st.warning("Claim flagged for manual review.")

st.markdown("---")

st.write("### Claims Risk Distribution")

# Simple bar chart of claim counts by fraud evaluation for filtered claims
risk_counts = filtered_claims["Fraud_Evaluation"].value_counts()
st.bar_chart(risk_counts)
