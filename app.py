import streamlit as st

from engines.city_engine import evaluate_cities

st.title("🎓 EdMenX")

st.subheader("Int'l Student Decision Support System")

st.caption("Helping international students choose the most "
           "suitable German cities for education, based on finances, career opportunities, "
           "and lifestyle preferences.")

st.write("Answer below and get recommendations!")

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
    results = evaluate_cities(budget, priority, city_size, part_time)

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