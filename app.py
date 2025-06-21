from flask import Flask, request, jsonify, render_template_string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Email configuration - you'll need to set these environment variables in Netlify
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS', 'your-email@gmail.com')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', 'your-app-password')
RECIPIENT_EMAIL = "jackodseattle@gmail.com"

@app.route('/')
def home():
    with open('index.html', 'r') as f:
        return f.read()

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    try:
        # Get form data
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        address = data.get('address')
        service_type = data.get('service_type')
        message = data.get('message')

        # Create email content
        email_subject = f"New Pressure Washing Inquiry from {name}"
        email_body = f"""
        New contact form submission from pwashing.com:

        Name: {name}
        Email: {email}
        Phone: {phone}
        Address: {address}
        Service Type: {service_type}
        Message: {message}

        Please respond to this inquiry promptly.
        """

        # Create email message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = email_subject
        msg.attach(MIMEText(email_body, 'plain'))

        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, text)
        server.quit()

        return jsonify({'success': True, 'message': 'Thank you! Your message has been sent successfully. We will contact you soon.'})

    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return jsonify({'success': False, 'message': 'There was an error sending your message. Please try again or call us directly.'})

@app.route('/styles.css')
def styles():
    with open('styles.css', 'r') as f:
        response = app.response_class(
            response=f.read(),
            status=200,
            mimetype='text/css'
        )
        return response

if __name__ == '__main__':
    app.run(debug=True)
