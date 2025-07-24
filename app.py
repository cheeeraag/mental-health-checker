import streamlit as st
import csv
import os
from datetime import datetime
import pandas as pd
import io

st.title("🧠 MindMirror: Mental Health Check")

st.markdown("""
Welcome to **MindMirror** — a simple, private tool to check in on your mental health.
Answer the following questions honestly. This is not a diagnosis but a quick mental wellness reflection.
""")

# Sample Questions (To be finalized by licensed psychologists)
questions = [
    "I’ve been feeling low, down, or hopeless.",
    "I’ve lost interest in activities I usually enjoy.",
    "I feel tired or have little energy.",
    "I struggle with sleep (too much or too little).",
    "I find it hard to concentrate or make decisions."
]

options = ["Never", "Rarely", "Sometimes", "Often", "Always"]

score_mapping = {
    "Never": 0,
    "Rarely": 1,
    "Sometimes": 2,
    "Often": 3,
    "Always": 4
}

answers = []

for i, q in enumerate(questions):
    answer = st.radio(f"{i+1}. {q}", options, key=i)
    answers.append(answer)

if st.button("🔍 Get My Mental Health Score"):
    score = sum([score_mapping[ans] for ans in answers])

    if score <= 5:
        suggestion = "You're doing well, but keep checking in with yourself. 😊"
    elif score <= 10:
        suggestion = "You're facing some stress. Consider healthy habits or talk to someone you trust. 💬"
    else:
        suggestion = "You might be struggling. Please consider talking to a therapist or support group. ❤️"

    st.subheader("🧠 Your Mental Health Score")
    st.write(f"**{score} / 20**")
    st.write(suggestion)

    # Optional feedback box
    feedback = st.text_area("💬 Optional: Share how you're feeling or any thoughts you want to express anonymously")

    # Save data to CSV
    file_exists = os.path.isfile("user_data_log.csv")
    with open("user_data_log.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Answers", "Score", "Suggestion", "Feedback"])
        writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), answers, score, suggestion, feedback])

# Admin view
if st.checkbox("🔐 Admin: Show User Logs"):
    try:
        df = pd.read_csv("user_data_log.csv")
        st.dataframe(df)
        st.line_chart(df["Score"])
    except FileNotFoundError:
        st.warning("No data available yet.")

# Optional download
if st.checkbox("⬇️ Download Log CSV"):
    try:
        df = pd.read_csv("user_data_log.csv")
        df.columns = ["Timestamp", "Answers", "Score", "Suggestion", "Feedback"]
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "user_data_log.csv", "text/csv")
    except FileNotFoundError:
        st.warning("No CSV file found.")
