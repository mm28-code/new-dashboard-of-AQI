import streamlit as st
import streamlit.components.v1 as components
import pdfkit  # Requires wkhtmltopdf to be installed

# Set your credentials
USERNAME = "mm28"
PASSWORD = "manish@28"

# Configure pdfkit to use wkhtmltopdf
pdfkit_config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')

# Function to check login credentials
def check_credentials():
    """Prompt for username and password, and verify credentials."""
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")
    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Logged in successfully as {username}!")
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
    # Page title with username
    st.title("Indian Air Quality Index Dashboard")
    st.markdown(f"<h3 style='text-align: center;'>Welcome, {st.session_state.username}!</h3>", unsafe_allow_html=True)

    # Embed Power BI dashboard
    power_bi_iframe = """
        <iframe title="Indian Air Quality Index new final" width="100%" height="1000px"
        src="https://app.powerbi.com/view?r=eyJrIjoiZjdlZjg3NDUtNjcwNC00MWY3LWE5OWYtZTIxZDQ4NTY0NDliIiwidCI6ImRjNTdkYjliLWNjNTQtNDI5Yi1iOWU4LTBhZmZhMzZmMDY2NiJ9"
        frameborder="0" allowFullScreen="true"></iframe>
    """
    components.html(power_bi_iframe, height=1000)

    # Button to download the dashboard as a PDF
    st.markdown("### Download Dashboard")
    if st.button("Download as PDF"):
        # Convert the Power BI iframe to PDF using the configured path for wkhtmltopdf
        pdfkit.from_string(power_bi_iframe, "dashboard.pdf", configuration=pdfkit_config)
        with open("dashboard.pdf", "rb") as pdf_file:
            st.download_button(
                label="Download Dashboard as PDF",
                data=pdf_file,
                file_name="Indian_Air_Quality_Dashboard.pdf",
                mime="application/pdf"
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

    # FAQ Section
    st.subheader("Frequently Asked Questions (FAQ)")
    st.markdown("""
    **Q1: What is the purpose of this dashboard?**  
    A: This dashboard provides an interactive visualization of the air quality index (AQI) in various locations across India.

    **Q2: How often is the data updated?**  
    A: The data in this dashboard is updated periodically to ensure it reflects the latest air quality information.

    **Q3: Can I download the data?**  
    A: Yes, you can download the data by clicking the "Download Dashboard as PDF" button above.
    """)
