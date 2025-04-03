from mcp.server.fastmcp import FastMCP
import smtplib
import ssl
from telethon import TelegramClient
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv
load_dotenv()
mcp = FastMCP("Send")

@mcp.tool()
def send_emails(filename:str)->str:
    """To Send Files Through Emails"""
    smtp_port,smtp_server,email_from, password=587,"smtp.gmail.com","manumanuvkm123@gmail.com","ouupizkcuioxqddf"
    simple_email_context = ssl.create_default_context()
    body = f"The Files are sended from Manu.AI "
    msg = MIMEMultipart()
    reciver="manuzmanuz79@gmail.com"
    files=[f"./download/{filename}"]
    msg['From'] = email_from
    msg['To'] = reciver
    msg['Subject'] = "File Transfer Through Manu AI"
    msg.attach(MIMEText(body, 'plain'))

    # Attach multiple files
    for file in files:
        try:
            with open(file, "rb") as attachment:
                attachment_package = MIMEBase("application", "octet-stream")
                attachment_package.set_payload(attachment.read())
                encoders.encode_base64(attachment_package)
                attachment_package.add_header("Content-Disposition", f"attachment; filename={file}")
                msg.attach(attachment_package)
        except Exception as e:
            print(f"Error attaching file {file}: {e}")
    text = msg.as_string()
    try:
        print("Connecting to server...")
        tie_server = smtplib.SMTP(smtp_server, smtp_port)
        tie_server.starttls(context=simple_email_context)
        tie_server.login(email_from, password)
        print("Sending email...")
        tie_server.sendmail(email_from,reciver, text)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
        return {"messages":e}
    finally:
        tie_server.quit()
    return "Email sent successfully!"
import requests
@mcp.tool()
async def Telegram(filename: str) -> str:
    """Send Files Through Telegram"""
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") 
    FILE_PATH = f"C:/Users/Manu/Desktop/Drive_AI/download/{filename}"
    # Removed emoji to avoid encoding issues
    MESSAGE = "Here is your file sent from Manu.AI!"
    
    if not BOT_TOKEN or not CHAT_ID:
        print("Error: BOT_TOKEN or CHAT_ID is missing!")
        return "Error: BOT_TOKEN or CHAT_ID is missing!"

    # Check if file exists first
    if not os.path.exists(FILE_PATH):
        print(f"Error: File not found at {FILE_PATH}")
        return f"Error: File not found at {FILE_PATH}"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    
    try:
        with open(FILE_PATH, "rb") as file:
            files = {"document": file}
            data = {"chat_id": CHAT_ID, "caption": MESSAGE}
            response = requests.post(url, data=data, files=files)
        
        if response.status_code == 200:
            print("File and message sent successfully!")
            return "File sent successfully!"
        else:
            print(f"Error: {response.text}")
            # Return a clean error message without special characters
            return f"Error sending file: {response.status_code}"
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}"
if __name__ == "__main__":
    mcp.run(transport="stdio")