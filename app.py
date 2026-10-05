import streamlit as st
import pickle
import requests
import re
from email_fetcher import get_latest_email

# load trained model
model, vectorizer = pickle.load(open("phishing_model.pkl","rb"))

st.title("AI Phishing Email Detector")

# Manual input fields
email_text = st.text_area("Paste Email Content")
email_header = st.text_area("Paste Email Header")

# Extract IP
def extract_ip(header):
    ip_pattern = r'[0-9]+(?:\.[0-9]+){3}'
    match = re.findall(ip_pattern, header)
    if match:
        return match[0]
    return None

# Get location
def get_location(ip):
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url).json()
    return response

# Extract URLs
def extract_urls(text):
    url_pattern = r'(https?://\S+)'
    return re.findall(url_pattern, text)

# ------------------------------
# Button 1 : Analyze pasted email
# ------------------------------
if st.button("Analyze Email"):

    email_vector = vectorizer.transform([email_text])

    prediction = model.predict(email_vector)
    probability = model.predict_proba(email_vector)

    phishing_prob = probability[0][1] * 100

    st.subheader("AI Risk Analysis")
    st.write("Risk Score:", round(phishing_prob,2), "%")
    st.progress(int(phishing_prob))

    if prediction[0] == 1:
        st.error("⚠ Phishing Email Detected")
    else:
        st.success("✅ Normal Email")

    urls = extract_urls(email_text)

    if urls:
        st.subheader("Detected URLs")
        for url in urls:
            st.write(url)

    ip = extract_ip(email_header)

    if ip:
        location = get_location(ip)

        st.subheader("Sender IP Information")
        st.write("IP:", ip)
        st.write("Country:", location.get("country", "Unknown"))
        st.write("City:", location.get("city", "Unknown"))
        st.write("ISP:", location.get("isp", "Unknown"))


# ------------------------------
# Button 2 : Scan latest email automatically
# ------------------------------
if st.button("Scan Latest Email"):

    subject, sender, email_text, email_header = get_latest_email()

    st.subheader("Latest Email Details")
    st.write("Subject:", subject)
    st.write("Sender:", sender)

    email_vector = vectorizer.transform([email_text])

    prediction = model.predict(email_vector)
    probability = model.predict_proba(email_vector)

    phishing_prob = probability[0][1] * 100

    st.subheader("AI Risk Analysis")
    st.write("Risk Score:", round(phishing_prob,2), "%")
    st.progress(int(phishing_prob))

    if prediction[0] == 1:
        st.error("⚠ Phishing Email Detected")
    else:
        st.success("✅ Normal Email")

    urls = extract_urls(email_text)

    if urls:
        st.subheader("Detected URLs")
        for url in urls:
            st.write(url)

    ip = extract_ip(email_header)

    if ip:
        location = get_location(ip)

        st.subheader("Sender IP Information")
        st.write("IP:", ip)
        st.write("Country:", location["country"])
        st.write("City:", location["city"])
        st.write("ISP:", location["isp"])