import streamlit as st

# Set page configuration
st.set_page_config(page_title="Creamy Zach", page_icon="🧈", layout="centered")

# Display content
st.title("🥛 Zach is Creamy 🥛")
st.write("This is an undeniable fact. 🫡")

# Add some styling
st.markdown(
    """
    <style>
    .big-text {
        font-size: 30px;
        font-weight: bold;
        color: #FFDDC1;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p class="big-text">Zach is creamy like the finest butter. 🧈</p>', unsafe_allow_html=True)

# Optional: Add a fun button
if st.button("Acknowledge Zach's Creaminess"):
    st.balloons()
    st.success("You have acknowledged the creamy truth. 🥛")

