def get_email_templete(application,scheduled_date,status):
    if status == 1:
        message_html = f"""
        <html>
        <body>
            <h1>Congratulations!</h1>
            <p>Your interview has been scheduled successfully.</p>
            <p><strong>Date:</strong> {scheduled_date.strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>We wish you the best of luck!</p>
        </body>
        </html>
        """
    elif status == 2:
        message_html = f"""
        <html>
        <body>
            <h1>Thank You!</h1>
            <p>Unfortunately, your application was not successful.</p>
            <p>We appreciate your interest and encourage you to apply for future opportunities.</p>
        </body>
        </html>
        """
    elif status == 3:
        message_html = f"""
        <html>
        <body>
            <h1>Application Update</h1>
            <p>Your application has been moved to the waiting list.</p>
            <p>We will notify you about any updates or changes.</p>
        </body>
        </html>
        """
    elif status == 4:
        message_html = f"""
        <html>
        <body>
            <h1>Application Update</h1>
            <p>Your application has been moved to the waiting list.</p>
            <p>We will notify you about any updates or changes.</p>
        </body>
        </html>
        """