import streamlit as st

# ------------------ Page Config ------------------
st.set_page_config(page_title="Mental Health Score Checker", page_icon="🧠", layout="centered")
st.title("🧠 Mental Health Score Checker")
st.write("Welcome! This tool helps you reflect on your current mental state and gives simple suggestions. Your answers stay private.")

# ------------------ Placeholder Questions ------------------
st.subheader("Answer the following questions:")

questions = [
    "1. How often do you feel anxious or on edge?",
    "2. Do you feel motivated to do daily tasks?",
    "3. Are you able to focus on studies/work without getting distracted?",
    "4. How well are you sleeping?",
    "5. Do you feel connected to people around you?"
]

options = ["Never", "Rarely", "Sometimes", "Often", "Always"]

responses = []

for q in questions:
    answer = st.radio(q, options, key=q)
    responses.append(answer)

# ------------------ Scoring Logic ------------------
def calculate_score(answers):
    score_map = {"Never": 0, "Rarely": 1, "Sometimes": 2, "Often": 3, "Always": 4}
    return sum(score_map[a] for a in answers)

# ------------------ Suggestions ------------------
def get_suggestion(score):
    if score >= 17:
        return ("✅ You're doing quite well! Keep up the healthy habits, and don’t hesitate to check in with yourself often.")
    elif score >= 10:
        return ("⚠️ You’re doing okay, but there are signs of stress. Try journaling, talking to a friend, or taking regular breaks.")
    else:
        return ("🚨 You might be struggling right now. Consider reaching out to a counselor or a trusted adult. You're not alone.")

# ------------------ Display Result ------------------
if st.button("Check My Score"):
    total_score = calculate_score(responses)
    st.markdown(f"### 🧾 Your Score: {total_score} / 20")
    suggestion = get_suggestion(total_score)
    st.info(suggestion)

    st.markdown("---")
    st.markdown("_This is not a medical diagnosis. For serious concerns, please consult a licensed mental health professional._")