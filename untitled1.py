New app




import streamlit as st
import streamlit.components.v1 as components

# Set your credentials
USERNAME = "mm28"
PASSWORD = "manish@28"

# Function to check login credentials
def check_credentials():
    """Prompt for username and password, and verify credentials."""
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")
    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
        else:
            st.error("Incorrect Username or Password")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Login Page
if not st.session_state.logged_in:
    st.title("Login to Access Indian Air Quality Dashboard")
    check_credentials()

# Dashboard Page
else:
    # Page title
    st.title("Indian Air Quality Index Dashboard")

    # Embed Power BI dashboard
    components.html(
        """
        <iframe title="Indian Air Quality Index new final" width="100%" height="1000px"
        src="https://app.powerbi.com/view?r=eyJrIjoiZjdlZjg3NDUtNjcwNC00MWY3LWE5OWYtZTIxZDQ4NTY0NDliIiwidCI6ImRjNTdkYjliLWNjNTQtNDI5Yi1iOWU4LTBhZmZhMzZmMDY2NiJ9"
        frameborder="0" allowFullScreen="true"></iframe>
        """,
        height=1000
    )

    # Feedback Section
    st.subheader("Feedback")

    # Rating with colored styling
    cols = st.columns(5)
    with cols[2]:  # Center the rating slider
        rating = st.slider("Rate the Dashboard:", min_value=1, max_value=5, value=3)
    
    # Rating Display with Colors
    if rating == 5:
        st.markdown("<h3 style='color:green;'>⭐️⭐️⭐️⭐️⭐️ Amazing!</h3>", unsafe_allow_html=True)
    elif rating == 4:
        st.markdown("<h3 style='color:blue;'>⭐️⭐️⭐️⭐️ Great!</h3>", unsafe_allow_html=True)
    elif rating == 3:
        st.markdown("<h3 style='color:orange;'>⭐️⭐️⭐️ Good</h3>", unsafe_allow_html=True)
    elif rating == 2:
        st.markdown("<h3 style='color:red;'>⭐️⭐️ Needs Improvement</h3>", unsafe_allow_html=True)
    else:
        st.markdown("<h3 style='color:darkred;'>⭐️ Poor</h3>", unsafe_allow_html=True)
    
    # Text area for feedback
    feedback = st.text_area("Please provide your feedback (below):")
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")
