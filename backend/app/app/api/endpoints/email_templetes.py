from app.models import *

def get_email_templete(application = None,scheduled_date=None,status=None,subject=None):
    if status == 1:#schedule interview
       
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    padding: 20px;
                    border: 1px solid #ddd;
                    border-radius: 10px;
                    background-color: #f9f9f9;
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .header h1 {{
                    font-size: 24px;
                    color: #0073e6;
                }}
                .content {{
                    margin-bottom: 20px;
                }}
                .footer {{
                    margin-top: 20px;
                    font-size: 14px;
                    text-align: center;
                    color: #555;
                }}
                .footer a {{
                    color: #0073e6;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Congratulations!</h1>
                </div>
                <div class="content">
                    <p>Dear <strong>{getattr(application, 'name', 'Candidate')}</strong>,</p>
                    <p>
                        Congratulations! We are pleased to inform you that you have been shortlisted for 
                        the <strong>{getattr(application.courses, 'name', 'the position')}</strong> position based on your resume.
                    </p>
                    <p>We would like to invite you to an interview scheduled as follows:</p>
                    <p>
                        <strong>Date and Time:</strong> 
                        {scheduled_date.strftime('%A, %d %B %Y, %I:%M %p')}
                    </p>
                    <p>Please confirm your availability by replying to this email.</p>
                    <p>
                        For any queries, please feel free to mail us at 
                        <a href="mailto:hr@team.themaestro.in">hr@team.themaestro.in</a> or call us at 
                        <a href="tel:+918637615560">+91-863-7615560</a>.
                    </p>
                </div>
                <div class="footer">
                    <p>Regards,</p>
                    <p><strong>GOWRI PRIYA D</strong></p>
                    <p>Accounts Head,<br>Maestro Technology Services Pvt. Ltd.<br>Coimbatore, Tamil Nadu.</p>
                    <p>
                        Contact No: <a href="tel:+918637615560">+91-863-7615560</a><br>
                        <a href="https://themaestro.in/">https://themaestro.in/</a>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
    elif status == 2:
        return f"""
        <html>
        <body>
            <h1>Thank You!</h1>
            <p>Unfortunately, your application was not successful.</p>
            <p>We appreciate your interest and encourage you to apply for future opportunities.</p>
        </body>
        </html>
        """
    elif status == 3:
        return f"""
        <html>
        <body>
            <h1>Application Update</h1>
            <p>Your application has been moved to the waiting list.</p>
            <p>We will notify you about any updates or changes.</p>
        </body>
        </html>
        """
    elif status == 4:#allocate batch
        return f"""
        <html>
        <body>
            <h1>Application Update</h1>
            <p>batch allocated</p>
            <p></p>
        </body>
        </html>
        """