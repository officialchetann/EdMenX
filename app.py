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

if st.button("Analyze"):

    results = evaluate_cities(budget)

    st.write("## Recommended Cities")

    for index, city in enumerate(results[:3], start=1):

        st.write(

            f"{index}. {city['city']} "

            f"({city['score']}/100)"

        )