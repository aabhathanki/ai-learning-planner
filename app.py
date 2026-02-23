import streamlit as st
import pandas as pd

from planner.generator import generate_learning_plan
from utils.export import generate_markdown
from utils.calendar_export import create_calendar
from components.plan_editor import edit_plan

st.set_page_config(page_title="AI Learning Planner", layout="wide")

st.title(" AI Personal Learning Planner")

# ---------- SESSION STATE ----------
if "data" not in st.session_state:
    st.session_state.data = None

# ---------- INPUTS ----------
skills = st.text_area("Enter your current skills")
target = st.text_input("Enter your target role")
compare_role = st.text_input("Compare with another role (optional)")

col1, col2 = st.columns(2)

with col1:
    time_commitment = st.selectbox(
        " Daily Study Time",
        ["30 mins", "1 hour", "2 hours", "3 hours"]
    )

with col2:
    difficulty = st.selectbox(
        " Difficulty Level",
        ["Beginner", "Intermediate"]
    )

# ---------- VALIDATION HELPER ----------
def is_valid_input(text, min_length=3):
    """Check if input is meaningful (not random characters)."""
    if not text or not text.strip():
        return False
    text = text.strip()
    if len(text) < min_length:
        return False
    # Count alphabetic characters
    alpha_chars = sum(c.isalpha() for c in text)
    # At least 60% of characters should be alphabetic
    if alpha_chars / len(text) < 0.6:
        return False
    # Must contain at least one space or comma (i.e., more than one word/skill)
    # OR be a valid single word of reasonable length
    words = [w for w in text.replace(",", " ").split() if w.isalpha()]
    if len(words) == 0:
        return False
    # Check for keyboard mashing (too many consecutive consonants)
    vowels = set("aeiouAEIOU")
    for word in words:
        if len(word) > 4:
            consonant_streak = 0
            for ch in word:
                if ch.isalpha() and ch not in vowels:
                    consonant_streak += 1
                else:
                    consonant_streak = 0
                if consonant_streak > 4:
                    return False
    return True

# ---------- GENERATE PLAN ----------
if st.button("Generate Plan"):

    # --- Validate Skills ---
    if not skills.strip():
        st.error(" Please enter your current skills (e.g., Python, Excel, SQL)")
        st.stop()
    elif not is_valid_input(skills, min_length=3):
        st.error(" Skills don't look valid. Please enter real skills like: *Python, SQL, Excel, communication*")
        st.stop()

    # --- Validate Target Role ---
    if not target.strip():
        st.error(" Please enter a target role (e.g., Data Scientist, Product Manager)")
        st.stop()
    elif not is_valid_input(target, min_length=3):
        st.error(" Target role doesn't look valid. Please enter a real role like: *Data Scientist* or *Web Developer*")
        st.stop()

    # --- Validate Compare Role (optional but must be valid if provided) ---
    if compare_role.strip() and not is_valid_input(compare_role, min_length=3):
        st.error(" Comparison role doesn't look valid. Please enter a real role or leave it empty.")
        st.stop()

    with st.spinner("Generating your personalized plan..."):
        st.session_state.data = generate_learning_plan(
            skills, target, time_commitment, difficulty
        )

# ---------- DISPLAY ----------
data = st.session_state.data

if data:

    # ---------- ERROR HANDLING ----------
    if "error" in data:
        st.error(data.get("error", "Something went wrong"))
        st.stop()

    # ---------- SKILL GAP ----------
    st.header(" Skill Gap Analysis")
    gap = data.get("skill_gap_analysis", {})

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader(" Strong Skills")
        for item in gap.get("strong_skills", []):
            if isinstance(item, dict):
                st.success(item.get("skill", str(item)))
            else:
                st.success(item)

    with col2:
        st.subheader(" Partial Gaps")
        for item in gap.get("partial_gaps", []):
            if isinstance(item, dict):
                st.warning(item.get("skill", str(item)))
            else:
                st.warning(item)

    with col3:
        st.subheader(" Missing Skills")
        for item in gap.get("missing_skills", []):
            if isinstance(item, dict):
                st.error(item.get("skill", str(item)))
            else:
                st.error(item)

    # ---------- WEEKLY PLAN ----------
    st.header(" Weekly Milestones")

    for week in data.get("weekly_plan", []):
        with st.expander(f" Week {week.get('week')} — {week.get('theme')}"):
            st.write(" **Milestone:**", week.get("milestone"))
            st.checkbox(f"Mark Week {week.get('week')} Complete", key=f"week_{week.get('week')}")

    # ---------- EDITABLE PLAN ----------
    if st.toggle(" Edit Plan"):
        data["daily_plan"] = edit_plan(data.get("daily_plan", []))
        st.session_state.data = data

    # ---------- DAILY PLAN ----------
    st.header(" 30-Day Plan")

    for day in data.get("daily_plan", []):
        with st.expander(f"Day {day.get('day')} — {day.get('title')}"):

            st.markdown(f"** Objective:** {day.get('objective')}")

            st.markdown("** Tasks:**")
            for task in day.get("tasks", []):
                st.write(f"• {task}")

            st.markdown("** Resources:**")
            for res in day.get("resources", []):
                if isinstance(res, dict):
                    title = res.get("title", "Resource")
                    platform = res.get("platform", "")
                    url = res.get("url", "")
                    if url:
                        st.markdown(f"- [{title}]({url}) — *{platform}*")
                    else:
                        st.markdown(f"- **{title}** — *{platform}*")
                else:
                    st.write(f"- {res}")

    # ---------- EXPORTS ----------
    st.header("⬇ Export Plan")

    try:
        markdown = generate_markdown(data, target)
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(" Download Markdown", markdown, "learning_plan.md")
        with col2:
            st.download_button(" Download TXT", markdown, "learning_plan.txt")
    except Exception as e:
        st.warning(f"Markdown export failed: {e}")

    try:
        cal = create_calendar(data)
        st.download_button("Download Calendar", str(cal), "learning_plan.ics")
    except Exception as e:
        st.warning(f"Calendar export failed: {e}")

    # ---------- ROLE COMPARISON ----------
    if compare_role:
        st.header(" Role Comparison")

        comparison = generate_learning_plan(
            skills, compare_role, time_commitment, difficulty
        )

        if comparison and "role_skill_map" in comparison:

            col1, col2 = st.columns(2)

            with col1:
                st.subheader(f" {target}")
                for skill in list(data.get("role_skill_map", {}).values())[0] if data.get("role_skill_map") else []:
                    st.write(f"• {skill}")

            with col2:
                st.subheader(f" {compare_role}")
                for skill in list(comparison.get("role_skill_map", {}).values())[0] if comparison.get("role_skill_map") else []:
                    st.write(f"• {skill}")

        else:
            st.warning("Comparison data not available")