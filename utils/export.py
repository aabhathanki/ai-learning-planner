def generate_markdown(plan, target_role):

    md = f"# 30-Day Learning Plan for {target_role}\n\n"

    for day in plan["daily_plan"]:
        md += f"## Day {day['day']}: {day['title']}\n"
        md += f"**Objective:** {day['objective']}\n\n"

        md += "**Tasks:**\n"
        for task in day["tasks"]:
            md += f"- {task}\n"

        md += "\n**Resources:**\n"
        for res in day["resources"]:
            md += f"- {res['title']} ({res['platform']})\n"

        md += "\n"

    return md