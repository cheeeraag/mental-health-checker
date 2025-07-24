import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="MindMirror", page_icon="🧠")

st.title("🧠 MindMirror – Mental Health Check")

# Questions and Options
questions = [
    "How often do you feel overwhelmed or stressed lately?",
    "Do you find it hard to get out of bed or complete daily tasks?",
    "Are you able to enjoy things you used to like?",
    "Do you feel lonely even when you're not alone?",
    "How often do you find your thoughts racing at night?",
    "Have you experienced changes in sleep or appetite recently?",
    "Do you feel motivated about your future?",
    "How often do you feel irritable or angry without clear reason?",
    "Do you feel like your emotions are hard to control?",
    "Do you avoid social situations or responsibilities lately?",
]

options = {
    "A": ("Almost always", 2),
    "B": ("Sometimes", 1),
    "C": ("Rarely/Never", 0)
}

st.markdown("### 📝 Answer the following questions:")

user_answers = []
total_score = 0

for i, q in enumerate(questions):
    st.write(f"**Q{i+1}. {q}**")
    selected = st.radio(
        f"Question {i+1}", 
        [f"{key}: {text}" for key, (text, _) in options.items()],
        key=f"q{i}"
    )
    user_answers.append(selected[0])
    total_score += options[selected[0]][1]

# Feedback Text Input
st.markdown("### 💬 Any feedback or suggestion?")
user_feedback = st.text_area("We’d love to hear from you!", placeholder="Your thoughts here...")

# Submit Button
if st.button("🚀 Submit"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Suggestion based on score
    if total_score <= 5:
        suggestion = "You're doing fine. Keep taking care of yourself! 🌿"
    elif total_score <= 12:
        suggestion = "Moderate signs of stress. Consider talking to someone or using mindfulness. 🤝"
    else:
        suggestion = "You may be facing high mental pressure. Professional help is advised. 💬"

    st.success(f"✅ Your Mental Health Score: **{total_score}/20**")
    st.info(suggestion)

    # Save to CSV
    data = [timestamp, ",".join(user_answers), total_score, suggestion, user_feedback]
    with open("user_data_log.csv", "a") as f:
        f.write(",".join([str(x) for x in data]) + "\n")

# Admin View
st.markdown("---")
if st.checkbox("👀 View All Responses (Admin Only)"):
    if os.path.exists("user_data_log.csv"):
        df = pd.read_csv("user_data_log.csv", header=None)
        df = df.iloc[:, :5]
        df.columns = ["Timestamp", "Answers", "Score", "Suggestion", "Feedback"]
        st.dataframe(df)
    else:
        st.info("No response data available yet.")
