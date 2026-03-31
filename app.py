import streamlit as st
import joblib

st.set_page_config(page_title="Phishing Risk Detector", layout="centered")

@st.cache_resource
def load_model():
    return joblib.load("phishing_risk_model.joblib")

model = load_model()

def risk_band(p):
    if p < 0.34:
        return "Low Risk"
    elif p < 0.67:
        return "Medium Risk"
    else:
        return "High Risk"

def recommendation(risk_level):
    if risk_level == "Low Risk":
        return "Low phishing risk detected. Proceed with normal caution when interacting with the email."
    elif risk_level == "Medium Risk":
        return "Review the sender and email content carefully. Avoid clicking links unless you can confirm the source is legitimate."
    else:
        return "Do not click any links or download attachments. Verify the sender through an official source before taking any action."

st.title("Phishing Risk Detector")
st.write("Paste the email content below to classify its phishing risk.")

email_content = st.text_area("Email Content", height=200)

if st.button("Analyze Email"):
    if email_content.strip() == "":
        st.warning("Please enter the email content to assess.")
    else:
        probability = model.predict_proba([email_content])[0][1]
        risk_level = risk_band(probability)
        advice = recommendation(risk_level)

        st.subheader("Risk Assessment Result")

        if risk_level == "Low Risk":
            st.success(f"Phishing Risk Level: {risk_level}")
        elif risk_level == "Medium Risk":
            st.warning(f"Phishing Risk Level: {risk_level}")
        else:
            st.error(f"Phishing Risk Level: {risk_level}")

        st.metric("Phishing Probability", f"{probability * 100:.1f}%")

        st.subheader("Recommended Action")
        st.info(advice)