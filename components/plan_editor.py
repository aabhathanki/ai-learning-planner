import streamlit as st

def edit_plan(daily_plan):

    for day in daily_plan:
        with st.expander(f"Edit Day {day['day']}"):

            day["title"] = st.text_input(
                f"Title {day['day']}", day["title"]
            )

            day["objective"] = st.text_area(
                f"Objective {day['day']}", day["objective"]
            )

    return daily_plan