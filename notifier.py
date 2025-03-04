import smtplib
from email.mime.text import MIMEText
import logging

logger = logging.getLogger('hyperliquid_monitor')

def send_email(config, message):
    """Send an email notification."""
    try:
        logger.debug(f"Preparing to send email with message: {message}")
        msg = MIMEText(message)
        msg['Subject'] = 'Hyperliquid Monitor Alert'
        msg['From'] = config['from']
        msg['To'] = config['to']
        server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        server.starttls()
        server.login(config['username'], config['password'])
        server.sendmail(config['from'], config['to'], msg.as_string())
        server.quit()
        logger.info("Email sent successfully")
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")

def send_wechat(config, message):
    """Send a WeChat notification (placeholder)."""
    try:
        logger.debug(f"Preparing to send WeChat message: {message}")
        # Implement WeChat API call here using config['appid'], config['secret'], config['to_user']
        logger.info("WeChat notification sent (placeholder)")
    except Exception as e:
        logger.error(f"Error sending WeChat message: {str(e)}")

def send_notification(config, message):
    """Send notification based on config type."""
    logger.debug(f"Sending notification with type: {config['type']}")
    if config['type'] == 'email':
        send_email(config['email'], message)
    elif config['type'] == 'wechat':
        send_wechat(config['wechat'], message)
    else:
        logger.warning("Unknown notification type")
