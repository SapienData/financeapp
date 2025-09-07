import streamlit as st
import pandas as pd

# Mock claims data
claims_data = [
    {"claim_id": "C001", "claim_type": "Auto", "amount": 5000, "fraud_risk": 0.1, "status": "Pending"},
    {"claim_id": "C002", "claim_type": "Home", "amount": 12000, "fraud_risk": 0.4, "status": "Pending"},
    {"claim_id": "C003", "claim_type": "Health", "amount": 3000, "fraud_risk": 0.05, "status": "Pending"},
    {"claim_id": "C004", "claim_type": "Auto", "amount": 8000, "fraud_risk": 0.8, "status": "Pending"},
]

df_claims = pd.DataFrame(claims_data)

def evaluate_fraud_risk(row):
    return "High Risk - Manual Review" if row["fraud_risk"] > 0.5 else "Low Risk - Auto Approve"

def assess_claim_amount(row):
    return "High Claim - Further Assessment" if row["amount"] > 10000 else "Standard Claim"

def color_risk(val):
    color = "red" if "High" in val else "green"
    return f"color: {color}; font-weight: bold"

def color_assessment(val):
    color = "orange" if "High" in val else "blue"
    return f"color: {color}; font-weight: bold"

# Add evaluations to dataframe
df_claims["Fraud_Evaluation"] = df_claims.apply(evaluate_fraud_risk, axis=1)
df_claims["Claim_Assessment"] = df_claims.apply(assess_claim_amount, axis=1)

# Sidebar for filtering
st.sidebar.title("Filter Claims")
claim_types = df_claims["claim_type"].unique().tolist()
selected_types = st.sidebar.multiselect("Claim Types", options=claim_types, default=claim_types)

filtered_claims = df_claims[df_claims["claim_type"].isin(selected_types)]

st.title("Agentic AI Insurance Claims Dashboard")

# Summary metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Claims", len(df_claims))
col2.metric("High Risk Claims", sum(df_claims["Fraud_Evaluation"] == "High Risk - Manual Review"))
col3.metric("High Amount Claims", sum(df_claims["Claim_Assessment"] == "High Claim - Further Assessment"))

st.markdown("---")

st.write("### Claims Overview")

# Display filtered data with styling
st.dataframe(
    filtered_claims.style
    .applymap(color_risk, subset=["Fraud_Evaluation"])
    .applymap(color_assessment, subset=["Claim_Assessment"])
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

# Simple bar chart of claim counts by fraud evaluation
risk_counts = filtered_claims["Fraud_Evaluation"].value_counts()
st.bar_chart(risk_counts)
