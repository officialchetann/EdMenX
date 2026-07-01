from pdf_generator import generate_pdf

import streamlit as st

from engines.city_engine import evaluate_cities

st.title("🎓 EdMenX")

st.subheader("Int'l Student Decision Support System")

st.caption("Helping international students choose the most "
           "suitable German cities for education, based on finances, career opportunities, "
           "and lifestyle preferences.")

st.write("Answer below and get recommendations!")

country = st.selectbox("🌍 Destination Country:",
                       ["Germany",
                        "France",
                        "Belgium",
                        "Netherlands",
                        "Austria",
                        "All Available Countries"])

budget = st.number_input(

    "💶 Monthly Budget (€)",

    min_value=500,

    max_value=3000,

    value=1100

)

priority = st.selectbox(

    "🎯 What matters most to you?",
    [
        "Affordability",
        "Career Opportunities",
        "Student Life"
    ]
)

city_size = st.selectbox(

    "🌃 Preferred City Size",
    [
        "Small",
        "Medium",
        "Large"
    ]
)

part_time = st.selectbox(
    "🏢 Need for Part-time Jobs",
    [
        "Yes",
        "No"
    ]
)

if st.button("🚀 Analyze"):

    from datetime import datetime
    timestamp = datetime.now().strftime("%d %B %Y | %I:%M %p")
    results = evaluate_cities(country, budget, priority, city_size, part_time)

    st.session_state["results"] = results

    st.session_state["country"] = country
    st.session_state["budget"] = budget
    st.session_state["priority"] = priority
    st.session_state["city_size"] = city_size
    st.session_state["part_time"] = part_time

    summary = []

    if priority == "Affordability":
        summary.append("Your choices prioritize affordability.")

    elif priority == "Career Opportunities":
        summary.append("Your choices prioritize career opportunities.")

    else:
        summary.append("Your choices prioritize student life.")

    if city_size == "Small":
        summary.append(
            "Budget-friendly locations with good part-time job opportunities are favored to support a financially sustainable student experience."
        )

    elif city_size == "Medium":
        summary.append(
            "Balanced cities with a supportive student environment are favored."
        )

    else:
        summary.append(
            "Larger cities with stronger employment opportunities are favored."
        )

    st.info(
        "📝 Preference Summary\n\n"
        + " ".join(summary)
    )

    st.session_state["summary"] = " ".join(summary)

results = st.session_state.get("results", [])

if results:
        st.write("## 🏆 Recommended Cities")

        for index, city in enumerate(results[:3], start=1):

            if index == 1:
                medal = "🥇"
            elif index == 2:
                medal = "🥈"
            elif index == 3:
                medal = "🥉"
            else:
                medal = "🏅"

            st.markdown(
                f"### {medal} {index}. {city['city']} ({city['score']}/100)"
            )
            if index == 1: st.success("⭐ Best Match!")

            for reason in city["reasons"]:
                st.write(f"- {reason}")

            st.markdown(
                f"🔹 **Confidence:** {city['confidence']}"
            )

            if st.button(f"📘 Learn More About {city['city']}",
                        key=f"guide_{city['city']}"):
                st.session_state["selected_city"] = city["city"]
                st.switch_page("pages/student_guide.py")


            with st.expander("📜 View Details"):

                st.write(f"Monthly Expenses: € {city['monthly_expenses']}")
                st.write(f"Average Rent: € {city['avg_rent']}")
                st.write(f"Job Score: € {city['job_score']}/100")
                st.write(f"Student Score: € {city['student_score']}/100")
                

            st.write("---")

        st.subheader("Top 3: Score Comparison")

        chart_data = {
            "City": [],
            "Score": []
        }

        for city in results[:3]:

            chart_data["City"].append(city["city"])
            chart_data["Score"].append(city["score"])

        st.bar_chart(data=chart_data,
                    x="City",
                    y="Score"
        )

        with st.expander("📑 Detailed Comparison"):

            comparison_data = []

            for city in results[:3]:

                comparison_data.append({

                    "City": city["city"],

                    "Monthly Expenses (€)": city["monthly_expenses"],

                    "Average Rent (€)": city["avg_rent"],

                    "Job Score": city["job_score"],

                    "Student Score": city["student_score"]

                })

            st.table(comparison_data)

if "results" in st.session_state:

    if st.button("📄 Generate Report"):

        generate_pdf(

            st.session_state["summary"],

            st.session_state["results"]

        )

        st.success(
            "Report created successfully!"
        )