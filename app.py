import streamlit as st
import pandas as pd
import datetime
import io

st.set_page_config(page_title="🧠 Mental Health Score Predictor", layout="centered")

st.title("🧠 Mental Health Check")
st.markdown("Welcome! Answer the questions below to check in on your mental health. It's anonymous and free.")

questions = [
    "I have felt down, depressed, or hopeless.",
    "I have little interest or pleasure in doing things.",
    "I feel nervous, anxious, or on edge.",
    "I find it difficult to control worrying.",
    "I feel tired or have little energy.",
    "I have trouble falling or staying asleep.",
    "I feel bad about myself or that I'm a failure.",
    "I have trouble concentrating on tasks.",
    "I feel alone or isolated.",
    "I have thoughts that I would be better off not existing."
]

options = ["A. Never", "B. Rarely", "C. Sometimes", "D. Often", "E. Almost Always"]

with st.form("mental_health_form"):
    answers = []
    for i, question in enumerate(questions):
        ans = st.radio(f"**{i+1}. {question}**", options, key=f"q{i}")
        answers.append(ans)

    feedback = st.text_area("💬 Optional Feedback (Tell us what you think or suggest improvements):", key="feedback")
    submitted = st.form_submit_button("📩 Submit")

if submitted:
    # Calculate score
    score = sum([options.index(ans) for ans in answers])

    # Generate suggestion
    if score <= 10:
        suggestion = "✅ You're doing great! Keep maintaining your mental well-being."
    elif score <= 20:
        suggestion = "🙂 You're okay, but some self-care or reflection may help."
    elif score <= 30:
        suggestion = "⚠️ You may be experiencing mild stress. Try talking to someone you trust."
    else:
        suggestion = "🚨 Consider seeking support from a professional or counselor."

    # Show result
    st.markdown("### 🧾 Your Result")
    st.markdown(f"- **Mental Health Score:** `{score}` out of `{len(questions) * 4}`")
    st.markdown(f"- **Interpretation:** {suggestion}")

    # Save to CSV
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("user_data_log.csv", "a") as f:
        f.write(f"{timestamp},{answers},{score},{suggestion},{feedback}\n")

    st.success("✅ Your response has been recorded anonymously. Thank you!")

# CSV download section
if st.checkbox("⬇️ Download Log CSV"):
    try:
        df = pd.read_csv("user_data_log.csv", header=None)
        df.columns = ["Timestamp", "Answers", "Score", "Suggestion", "Feedback"]
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download CSV", csv, "user_data_log.csv", "text/csv")
    except FileNotFoundError:
        st.warning("No CSV file found.")
