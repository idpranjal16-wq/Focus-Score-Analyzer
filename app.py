import streamlit as st

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="FocusFlow",
    page_icon="🧠",
    layout="wide"
)

# ---------------- STYLE ----------------
st.markdown("""
<style>

.stApp{
    background-color:#0f172a;
    color:white;
}

.block-container{
    padding-top:2rem;
    max-width:1100px;
}

h1,h2,h3,label{
    color:white !important;
}

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input{
    background:#1e293b;
    color:white;
}

div[data-testid="stSelectbox"]{
    color:white;
}

.stButton>button{
    width:100%;
    height:50px;
    border-radius:12px;
    background:#2563eb;
    color:white;
    font-size:18px;
    font-weight:bold;
    border:none;
}

.stButton>button:hover{
    background:#1d4ed8;
}

.card{
    background:#1e293b;
    padding:18px;
    border-radius:12px;
    margin-bottom:15px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------

st.title("🧠 FocusFlow")
st.caption("Track your day. Improve your focus.")

st.divider()

# ---------------- USER ----------------

name = st.text_input("👤 Your Name")

goal = st.text_input(
    "🎯 Today's Goal",
    placeholder="Example: Complete Python Project"
)

st.divider()

st.subheader("📝 What did you do today?")

activities = []

categories = [
    "Work / Study",
    "Health",
    "Entertainment",
    "Social Media",
    "Other"
]

total_hours = 0

for i in range(5):

    st.markdown(f"### Activity {i+1}")

    col1, col2, col3 = st.columns([3,1,2])

    with col1:
        activity = st.text_input(
            "Activity",
            key=f"name{i}",
            placeholder="Example: Coding"
        )

    with col2:
        hours = st.number_input(
            "Hours",
            min_value=0.0,
            max_value=24.0,
            step=0.5,
            key=f"hour{i}"
        )

    with col3:
        category = st.selectbox(
            "Category",
            categories,
            key=f"cat{i}"
        )

    total_hours += hours

    activities.append({
        "Activity": activity,
        "Hours": hours,
        "Category": category
    })

st.divider()

st.subheader("⏰ Hours Logged")

st.progress(min(total_hours/24,1.0))

st.write(f"**{total_hours:.1f} / 24 hours logged**")

if total_hours > 24:
    st.error("You have entered more than 24 hours.")

analyze = st.button("📊 Generate Report")
# ---------------- REPORT ----------------

if analyze:

    # Remove empty activities
    data = [a for a in activities if a["Activity"].strip() != "" and a["Hours"] > 0]

    if len(data) == 0:
        st.warning("Please enter at least one activity.")
        st.stop()

    import pandas as pd
    import plotly.express as px

    df = pd.DataFrame(data)

    # Productive Categories
    productive_categories = ["Work / Study", "Health"]

    productive_hours = df[df["Category"].isin(productive_categories)]["Hours"].sum()
    distracting_hours = df[~df["Category"].isin(productive_categories)]["Hours"].sum()

    total = productive_hours + distracting_hours

    if total == 0:
        score = 0
    else:
        score = int((productive_hours / total) * 100)

    # Grade
    if score >= 90:
        grade = "A+ 🌟"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 60:
        grade = "C"
    else:
        grade = "D"

    st.divider()

    st.header("📊 Daily Report")

    st.success(f"Hello **{name if name else 'User'}** 👋")

    st.write(f"**🎯 Today's Goal:** {goal if goal else 'No goal entered'}")

    col1, col2, col3 = st.columns(3)

    col1.metric("🎯 Focus Score", f"{score}%")
    col2.metric("🏆 Grade", grade)
    col3.metric("⏰ Hours Logged", f"{total_hours:.1f}/24")

    st.progress(score/100)

    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        st.metric("🟢 Productive Hours", f"{productive_hours:.1f}")

    with c2:
        st.metric("🔴 Distracting Hours", f"{distracting_hours:.1f}")

    st.divider()

    # Pie Chart
    pie = px.pie(
        names=["Productive", "Distracting"],
        values=[productive_hours, distracting_hours],
        title="Time Distribution"
    )

    st.plotly_chart(pie, use_container_width=True)

    # Bar Chart
    bar = px.bar(
        df,
        x="Activity",
        y="Hours",
        color="Category",
        title="Activity Breakdown"
    )

    st.plotly_chart(bar, use_container_width=True)

    st.divider()

    st.subheader("💡 Recommendations")

    if score >= 80:
        st.success("✅ Excellent day! Keep maintaining this routine.")

    elif score >= 60:
        st.info("👍 Good work! Try reducing entertainment or social media.")

    else:
        st.warning("⚠️ You spent more time on distractions than productive work.")

    if total_hours > 24:
        st.error("Your total hours exceed 24. Please check your entries.")

    elif total_hours < 24:
        st.info(f"🕒 You still have **{24-total_hours:.1f} hours** unaccounted for.")

    if productive_hours < 4:
        st.warning("📚 Try spending more time on work, study, or health activities.")

    st.divider()

    st.caption("Built with ❤️ using Python, Streamlit and Plotly")