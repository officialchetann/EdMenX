import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="EdMenX Student Guide",
    page_icon="🎓",
    layout="wide"
)

if "selected_city" not in st.session_state:
    st.warning("⚠ Please select a city from the recommendation page!")
    st.stop()
selected_city = st.session_state["selected_city"]

city_info = pd.read_csv("data/city_info.csv")
universities_df = pd.read_csv("data/universities.csv")
city_data = city_info[city_info["city"] == selected_city].iloc[0]

city_universities = universities_df[
    universities_df["city"] == selected_city
]

st.title(f"🎓 EdMenX for {selected_city}")
st.caption(city_data["summary"])

st.write("___")

col1, col2 = st.columns(2)
with col1:
    st.metric("🌍 Country", city_data["country"])
    st.metric("👥 Population", city_data["population"])
with col2:
    st.metric("⭐ Student Rating", city_data["student_rating"])

    selected_result = next(city for city in st.session_state["results"]
                         if city["city"] == selected_city)
    st.metric("💶 Estimated Monthly Cost", f"€{selected_result['monthly_expenses']}")

comparison_data = [
    {
        "Preference": "💶 Monthly Budget",
        "City Profile": f"€{city_data['recommended_budget']}",
        "Your Input": f"€{st.session_state['budget']}",
        "Status": "🟢"
        if st.session_state["budget"] >= city_data["recommended_budget"]
        else "🟡"
    },
    {
        "Preference": "🌃 Preferred City Size",
        "City Profile": city_data["city_size"],
        "Your Input": st.session_state["city_size"],
        "Status": "🟢"
        if st.session_state["city_size"] == city_data["city_size"]
        else "🟡"
    },
    {
        "Preference": "🏢 Part-time Job Market",
        "City Profile": city_data["job_market"],
        "Your Input": st.session_state["part_time"],
        "Status": "🟢"
        if (
            st.session_state["part_time"] == "No"
            or city_data["job_market"] in ["Strong", "Excellent"]
        )
        else "🟡"
    },
    {
        "Preference": "🎯 Priority",
        "City Profile": st.session_state["priority"],
        "Your Input": st.session_state["priority"],
        "Status": "🟢"
    }
]

st.write("---")
st.subheader("📋 Your Compatibility with This City")

st.table(comparison_data)

st.write("---")
st.subheader("🧠 EdMenX Insight")

insight = []

# Budget
if st.session_state["budget"] >= city_data["recommended_budget"]:
    insight.append(
        "Your monthly budget is sufficient for this city's recommended cost of living."
    )
else:
    insight.append(
        "Your monthly budget is below this city's recommended level, so careful financial planning will be important."
    )

# City Size
if st.session_state["city_size"] == city_data["city_size"]:
    insight.append(
        "Your preferred city size aligns well with what this city offers."
    )
else:
    insight.append(
        "This city's size differs from your preference, so your living experience may be slightly different from what you expect."
    )

# Part-time Jobs
if st.session_state["part_time"] == "Yes":
    if city_data["job_market"] in ["Strong", "Excellent"]:
        insight.append(
            "The city's job market is favourable for students seeking part-time employment."
        )
    else:
        insight.append(
            "Part-time opportunities are available but may require additional effort to secure."
        )

st.success(" ".join(insight))

# -----------------------------
# S3
# -----------------------------
st.write("----")
st.subheader("🎓 Recommended Universities")

for _, uni in city_universities.iterrows():

    st.markdown(
        f"### {uni['university']}"
    )

    st.caption(
        f"🏅 Rank in Country: #{uni['rank_in_country']}"
    )

    with st.expander("📘 View Details"):

        st.write(
            f"**Annual Fees:** {uni['annual_fee']}"
        )

        st.write(
            uni["description"]
        )

        st.link_button(
            "🌐 Visit Official Website",
            uni["website"]
        )

    st.write("---")

st.divider()

# -----------------------------
# S4
# -----------------------------
st.subheader("📍 City Snapshot")

snapshot_data = [
    ("💼 Employment", city_data["employment"]),
    ("🎓 Student Environment", city_data["student_environment"]),
    ("💰 Living Cost", city_data["living_cost"]),
    ("🌍 International Community", city_data["international_community"]),
    ("🚆 Public Transport", city_data["public_transport"]),
    ("🛡️ Safety", city_data["safety"]),
]

for title, value in snapshot_data:
    col1, col2 = st.columns([3, 1])

    with col1:
        st.write(title)

    with col2:
        st.write(value)

st.divider()

st.write("----")
st.subheader("🌍 Next Steps")

col1, col2 = st.columns(2)

with col1:
    st.link_button(
        "🌐 Explore the City",
        city_data["wikipedia"]
    )

    st.link_button(
        "🎓 Official Study Portal",
        city_data["study_portal"]
    )

with col2:
    st.link_button(
        "💰 Scholarships",
        city_data["scholarship"]
    )

    st.link_button(
        "🛂 Visa Information",
        city_data["visa"]
    )