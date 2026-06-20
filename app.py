import streamlit as st

from engines.city_engine import evaluate_cities


st.title("EdMenX")

st.subheader(

    "International Student Decision Support"

)

budget = st.number_input(

    "Monthly Budget (€)",

    min_value=500,

    max_value=3000,

    value=1100

)

priority = st.selectbox(

    "What matters most to you?",
    [
        "Affordability",
        "Career Opportunities",
        "Student Life"
    ]
)

city_size = st.selectbox(

    "Preferred City Size:",
    [
        "Small",
        "Medium",
        "Large"
    ]
)

if st.button("Analyze"):
    results = evaluate_cities(budget, priority, city_size)

    st.write("## 🏆 Recommended Cities")

    for index, city in enumerate(results[:3], start=1):

        st.write(
            f"### 🎖️ {index}. {city['city']} ({city['score']}/100)"
        )

        for reason in city["reasons"]:
            st.write(f"- {reason}")

        st.markdown(
            f"🔹 **Confidence:** {city['confidence']}"
        )

        st.write("---")