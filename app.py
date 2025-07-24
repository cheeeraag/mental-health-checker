import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="MindMirror", page_icon="🧠")

st.title("🧠 MindMirror: Mental Health Self-Check")

st.markdown("Take this short self-assessment to reflect on your current mental state. It's completely anonymous and free.")

# Options for each question
options = [
    "A. Never",          # 0
    "B. Rarely",         # 1
    "C. Sometimes",      # 2
    "D. Often",          # 3
    "E. Almost Always"   # 4
]

# Sample questions (to be replaced by expert-approved ones)
questions = [
    "Do you feel overwhelmed or anxious frequently?",
    "Are you able to sleep well most nights?",
    "Do you enjoy activities you used to enjoy?",
    "Do you feel hopeful about the future?",
    "Do you find it hard to concentrate or stay focused?"
]

# --- Form Begins ---
with st.form("mental_health_form"):
    st.markdown("### 📝 Self-Assessment")

    answers = []
    score = 0

    for i, q in enumerate(questions, 1):
        ans = st.radio(f"{i}. {q}", options, key=f"q{i}")
        answers.append(ans)
        score += options.index(ans)  # A=0, E=4

    feedback = st.text_area("💬 Would you like to share any feedback or thoughts?", "")

    submitted = st.form_submit_button("Submit")

    if submitted:
        # Generate suggestion based on score
        if score <= 5:
            suggestion = "✅ You're doing great! Keep maintaining your mental well-being."
        elif score <= 10:
            suggestion = "🙂 You're okay, but some self-care or reflection may help."
        elif score <= 15:
            suggestion = "⚠️ You may be experiencing mild stress. Try talking to someone you trust."
        else:
            suggestion = "🚨 Consider seeking support from a professional or counselor."

        # Show result
        st.markdown(f"### 🧾 Result: **{suggestion}**")

        # Save to CSV log
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("user_data_log.csv", "a") as f:
            f.write(f"{timestamp},{answers},{score},{suggestion},{feedback}\n")

        st.success("✅ Your response has been recorded anonymously. Thank you!")

# --- Form Ends ---

# Admin Panel to View Logs
st.markdown("---")
if st.checkbox("🔐 Admin: Show User Logs"):
    try:
        df = pd.read_csv("user_data_log.csv", header=None)
        df.columns = ["Timestamp", "Answers", "Score", "Suggestion", "Feedback"]
        st.dataframe(df)

        # CSV download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download CSV", csv, "user_data_log.csv", "text/csv")

    except FileNotFoundError:
        st.warning("No user data available yet.")
