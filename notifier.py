import smtplib
from email.mime.text import MIMEText

def send_email(config, message):
    """Send an email notification."""
    try:
        msg = MIMEText(message)
        msg['Subject'] = 'Hyperliquid Monitor Alert'
        msg['From'] = config['from']
        msg['To'] = config['to']
        server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        server.starttls()
        server.login(config['username'], config['password'])
        server.sendmail(config['from'], config['to'], msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

def send_wechat(config, message):
    """Send a WeChat notification (placeholder)."""
    # Implement WeChat API call here using config['appid'], config['secret'], config['to_user']
    print(f"WeChat notification (not implemented): {message}")

def send_notification(config, message):
    """Send notification based on config type."""
    if config['type'] == 'email':
        send_email(config['email'], message)
    elif config['type'] == 'wechat':
        send_wechat(config['wechat'], message)
    else:
        print("Unknown notification type")
