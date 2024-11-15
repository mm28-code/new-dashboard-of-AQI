import streamlit as st
import streamlit.components.v1 as components
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pdfkit  # Ensure pdfkit is installed
import os

# Set your credentials
USERNAME = "mm28"
PASSWORD = "manish@28"

# SMTP configuration
smtp_server = "smtp.office365.com"
smtp_port = 587
smtp_user = "support@aptpath.in"
smtp_password = "kjydtmsbmbqtnydk"
sender_email = "support@aptpath.in"
receiver_emails = ["mks60209@gmail.com"]

# Function to send feedback email
def send_email(subject, body, receiver_emails):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ", ".join(receiver_emails)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(sender_email, receiver_emails, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False

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

# Function to generate PDF from HTML content
def generate_pdf(html_content, output_filename):
    try:
        pdfkit.from_string(html_content, output_filename)
        return True
    except Exception as e:
        st.error(f"Error generating PDF: {e}")
        return False

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
    iframe_code = """
        <iframe title="Indian Air Quality Index new final" width="100%" height="1000px"
        src="https://app.powerbi.com/view?r=eyJrIjoiZjdlZjg3NDUtNjcwNC00MWY3LWE5OWYtZTIxZDQ4NTY0NDliIiwidCI6ImRjNTdkYjliLWNjNTQtNDI5Yi1iOWU4LTBhZmZhMzZmMDY2NiJ9"
        frameborder="0" allowFullScreen="true"></iframe>
    """
    components.html(iframe_code, height=1000)

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
        if feedback.strip():
            feedback_body = f"User Feedback:\n\nRating: {rating} stars\n\nFeedback:\n{feedback}"
            email_sent = send_email("Dashboard Feedback", feedback_body, receiver_emails)
            if email_sent:
                st.success("Thank you for your feedback! It has been sent successfully.")
            else:
                st.error("Failed to send feedback. Please try again later.")
        else:
            st.warning("Please provide feedback before submitting.")
    
    # PDF Download Section
    st.subheader("Download Dashboard")
    if st.button("Download Dashboard as PDF"):
        html_dashboard = f"""
        <html>
            <head><title>Indian Air Quality Dashboard</title></head>
            <body>
                <h1>Indian Air Quality Index Dashboard</h1>
                {iframe_code}
                <h2>Feedback</h2>
                <p>Rating: {rating} stars</p>
                <p>Feedback: {feedback}</p>
            </body>
        </html>
        """
        pdf_filename = "dashboard.pdf"
        if generate_pdf(html_dashboard, pdf_filename):
            with open(pdf_filename, "rb") as file:
                st.download_button(
                    label="Download PDF",
                    data=file,
                    file_name=pdf_filename,
                    mime="application/pdf"
                )
            os.remove(pdf_filename)  # Cleanup after download
