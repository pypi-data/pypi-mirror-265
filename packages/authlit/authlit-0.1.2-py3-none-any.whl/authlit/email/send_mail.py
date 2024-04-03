import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from authlit.config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD, SENDER_NAME


def send_email(recipient_email, subject, body):
    # Set up the MIME object
    msg = MIMEMultipart()
    msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg["To"] = recipient_email
    msg["Subject"] = subject

    # Attach the body of the email
    msg.attach(MIMEText(body, "plain"))

    if not all([SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD]):
        print("Email not sent. Please configure the SMTP server settings.")
        return

    # Establish a connection to the SMTP server (in this case, Gmail's SMTP server)
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Send the email
        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())


def send_otp_via_email(
    username: str,
    user_email: str,
    company: str,
    otp: str,
) -> None:
    """
    Sends an email to the user containing the OTP.
    """
    msg_content = f"Hello {username},\n\nYour OTP for {company} is {otp}.\n\nBest,\n{company}"
    send_email(user_email, f"OTP for {company}", msg_content)
