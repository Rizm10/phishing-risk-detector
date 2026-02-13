import streamlit as st 
import joblib 

st.set_page_config(page_title= "Phishing Risk Detector", layout= "centered")

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
    
st.title("Phishing Risk Detector")
st.write("paste the email content below to assess its phishing risk level.")

email_content = st.text_area("Email Content", height=200)
if st.button("Assess Risk"):
    if email_content.strip() == "":
        st.warning("Please enter the email content to assess.")
    else:
        # Preprocess the input as needed (e.g., vectorization)
        # Here we assume the model can handle raw text input directly
        probability = model.predict_proba([email_content])[0][1]
        risk_level = risk_band(probability)
        
        st.subheader("Risk Assessment Result")
        st.write(f"Phishing Risk Level: **{risk_level}**")
        st.metric("Phishing Probability", f"{probability*100:.1f}%")
