from app.models import *

def get_email_templete(application = None,scheduled_date=None,status=None,subject=None,username = None,password=None):
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
                <h1>Interview Invitation</h1>
            </div>
            <div class="content">
                <p>Dear <strong>{getattr(application, 'name', 'Candidate')}</strong>,</p>
                <p>
                    Thank you for applying to the internship role at Velava Foundation. 
                    We are pleased to inform you that you have been shortlisted for the interview.
                </p>
                <p>We would like to invite you for the interview which is scheduled as follows:</p>
                <p>
                    <strong>Date:</strong> {scheduled_date.strftime('%A, %d %B %Y')}<br>
                    <strong>Mode:</strong> In-Person<br>
                    <strong>Venue:</strong> Site No. 4, Maestro Building, Sp Garden, 
                    Sathy Road, Kaapi Kadai, Vilankurichi, Coimbatore – 641035
                </p>
                <p><strong>Interview Process:</strong></p>
                <ul>
                    <li>Written Test: Includes aptitude and technical questions</li>
                    <li>Technical Round: Face-to-face interview with technical personnel</li>
                    <li>HR Round: Final round with the HR Team</li>
                </ul>
                <p>
                    If you have any questions or concerns, please feel free to contact us at 
                    <a href="tel:+918637615560">+91-863-761-5560</a>.
                </p>
                <p>We look forward to meeting you!</p>
            </div>
            <div class="footer">
                <p>Best Regards,</p>
                <p><strong>Gowri Priya D.</strong><br>
                   Operations<br>
                   Velava Foundation
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    elif status == 2:# resume Not seleted
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
                color: #e74c3c;
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
                <h1>Thank You for Your Application</h1>
            </div>
            <div class="content">
                <p>Dear <strong>{getattr(application, 'name', 'Candidate')}</strong>,</p>
                <p>
                    Thank you for applying for the internship role at Velava Foundation. 
                    We truly appreciate the time and effort you invested in the application process.
                </p>
                <p>
                    After careful consideration, we regret to inform you that you have not been selected 
                    for the internship position at this time. 
                </p>
                <p>
                    Please know that this decision was a difficult one, as we received many strong applications. 
                    We encourage you to apply for future opportunities with us that align with your skills and interests.
                </p>
                <p>
                    If you have any questions or would like feedback on your application, feel free to 
                    contact us at <a href="mailto:hr@velavafoundation.org">hr@velavafoundation.org</a>.
                </p>
                <p>We wish you the very best in your future endeavors!</p>
            </div>
            <div class="footer">
                <p>Best Regards,</p>
                <p><strong>Gowri Priya D.</strong><br>
                   Operations<br>
                   Velava Foundation
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    elif status == 3: #selected
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
                color: #28a745;
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
                    We are delighted to inform you that you have been selected for the internship role at Velava Foundation. 
                    Congratulations on successfully completing the interview process!
                </p>
                <p>
                    We were impressed with your skills, enthusiasm, and potential, and we are excited to have you as part of our team. 
                    Further details about your internship, including the joining date and onboarding process, will be shared with you soon.
                </p>
                <p>
                    If you have any questions or require further information, please feel free to reach out to us at 
                    <a href="tel:+918637615560">+91-863-7615560</a> or reply to this email.
                </p>
                <p>Welcome aboard! We look forward to a rewarding journey together.</p>
            </div>
            <div class="footer">
                <p>Best Regards,</p>
                <p><strong>Gowri Priya D.</strong><br>
                   Operations<br>
                   Velava Foundation
                </p>
                <p>
                    Contact No: <a href="tel:+918637615560">+91-863-7615560</a><br>
                    <a href="https://velavafoundation.org/">https://velavafoundation.org/</a>
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    elif status == 4:# not seleted in interview
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
                color: #dc3545;
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
                <h1>Thank You for Your Application</h1>
            </div>
            <div class="content">
                <p>Dear <strong>{getattr(application, 'name', 'Candidate')}</strong>,</p>
                <p>
                    Thank you for attending the interview for the internship role at Velava Foundation. 
                    After careful consideration, we regret to inform you that you have not been selected for this position.
                </p>
                <p>
                    We appreciate your effort and encourage you to apply for future opportunities with us. 
                    Wishing you the very best in your career.
                </p>
            </div>
            <div class="footer">
                <p>Best Regards,</p>
                <p><strong>Gowri Priya D.</strong><br>
                   Operations<br>
                   Velava Foundation
                </p>
                <p>
                    Contact No: <a href="tel:+918637615560">+91-863-7615560</a><br>
                    <a href="https://velavafoundation.org/">https://velavafoundation.org/</a>
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    elif status == 5:#waiting list
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
                color: #ffc107;
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
            
            <div class="content">
                <p>Dear <strong>{getattr(application, 'name', 'Candidate')}</strong>,</p>
                <p>
                    Thank you for attending the interview for the internship role at Velava Foundation. 
                    We appreciate the time and effort you invested in the interview process.
                </p>
                <p>
                    After careful consideration, we regret to inform you that we are unable to offer you a position at this time. 
                    However, we are placing you on our waiting list, as we were impressed with your skills and background.
                </p>
                <p>
                    Should a suitable position become available, we will contact you immediately. We encourage you to stay in touch with us 
                    and apply for future opportunities that may align with your profile.
                </p>
            </div>
            <div class="footer">
                <p>Best Regards,</p>
                <p><strong>Gowri Priya D.</strong><br>
                   Operations<br>
                   Velava Foundation
                </p>
                <p>
                    Contact No: <a href="tel:+918637615560">+91-863-7615560</a><br>
                    <a href="https://velavafoundation.org/">https://velavafoundation.org/</a>
                </p>
            </div>
        </div>
    </body>
    </html>"""

    elif status == 6: # sending user name password
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
                    <h1>Your Account Details</h1>
                </div>
                <div class="content">
                    <p>Dear <strong>{getattr(application, 'name', 'User')}</strong>,</p>
                    <p>
                        Welcome to Velava Foundation! We are pleased to provide you with your account details below:
                    </p>
                    <p>
                        <strong>Username:</strong> {username}<br>
                        <strong>Password:</strong> {password}
                    </p>
                    <p>
                        To log in and access your account, please visit the following link:
                    </p>
                    <p>
                        <a href="https://samplewebsite.com/login" target="_blank">https://samplewebsite.com/login</a>
                    </p>
                    <p>
                        If you have any questions or need assistance, feel free to reach out to us at 
                        <a href="tel:+918637615560">+91-863-7615560</a> or reply to this email.
                    </p>
                    <p>We look forward to seeing you onboard!</p>
                </div>
                <div class="footer">
                    <p>Best Regards,</p>
                    <p><strong>Gowri Priya D.</strong><br>
                    Operations<br>
                    Velava Foundation
                    </p>
                    <p>
                        Contact No: <a href="tel:+918637615560">+91-863-7615560</a><br>
                        <a href="https://velavafoundation.org/">https://velavafoundation.org/</a>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """