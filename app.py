import streamlit as st
from datetime import datetime
import csv

st.set_page_config(page_title="Mental Health Checker", layout="centered")

st.title("🧠 Mental Health Checker")
st.markdown("Answer the following questions to check your current mental health status. This is **anonymous** and just for awareness.")

# Placeholder questions (replace with final ones later)
q1 = st.selectbox("1. How often do you feel overwhelmed?", ["Never", "Sometimes", "Often", "Always"])
q2 = st.selectbox("2. How well are you sleeping these days?", ["Very well", "Okay", "Poorly", "Barely sleeping"])
q3 = st.selectbox("3. Do you enjoy your daily routine?", ["Yes", "Somewhat", "Rarely", "Not at all"])
q4 = st.selectbox("4. How often do you feel anxious or sad?", ["Rarely", "Occasionally", "Frequently", "Constantly"])
q5 = st.selectbox("5. Do you feel connected to people around you?", ["Yes", "Somewhat", "Not really", "Very isolated"])

# Scoring logic (adjust later with expert-backed values)
score_map = {
    "Never": 0, "Very well": 0, "Yes": 0, "Rarely": 0,
    "Sometimes": 1, "Okay": 1, "Somewhat": 1, "Occasionally": 1,
    "Often": 2, "Poorly": 2, "Rarely": 2, "Not really": 2,
    "Always": 3, "Barely sleeping": 3, "Not at all": 3, "Constantly": 3, "Very isolated": 3
}

answers = [q1, q2, q3, q4, q5]
score = sum(score_map[ans] for ans in answers)

# Function to suggest based on score
def get_suggestion(score):
    if score <= 5:
        return "✅ You're doing well. Stay self-aware and consistent."
    elif score <= 10:
        return "🟡 You're showing early signs of stress. Try mindfulness, journaling, or talking to someone."
    elif score <= 15:
        return "🟠 You may be struggling. Consider taking breaks, setting boundaries, or speaking to a peer counselor."
    else:
        return "🔴 You're likely facing high mental distress. Please consult a licensed therapist if possible."

# Logging function
def log_user_response(answers, score, suggestion, feedback):
    with open("user_data_log.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), answers, score, suggestion, feedback])

if st.button("🧾 Submit"):
    suggestion = get_suggestion(score)
    feedback = st.text_area("💬 Optional: Share how you're feeling or any thoughts you want to express anonymously")
    log_user_response(answers, score, suggestion)
    st.markdown(f"### 🧮 Your Mental Health Score: `{score}/15`")
    st.success(suggestion)

import pandas as pd
if st.checkbox("🔐 Admin: Show User Logs"):
    df = pd.read_csv("user_data_log.csv", header=None)
    df.columns = ["Timestamp", "Answers", "Score", "Suggestion", "Feedback"]
    st.dataframe(df)
    st.line_chart(df["Score"])
