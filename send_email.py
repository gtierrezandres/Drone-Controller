import smtplib
import imghdr
from email.message import EmailMessage
import os

msg = EmailMessage()
msg['Subject'] = "Sunset Photos"
msg["From"] = "SenderEmail"
msg["To"] = "ReceiverEmail"
msg.set_content("How about this for a stupid drone huh?")

files = os.listdir("photos")

os.chdir(os.path.abspath('photos'))

for file in files:
    with open(file, 'rb') as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)

    msg.add_attachment(file_data, filename=f.name, maintype="image", subtype=file_type)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login("SenderEmail", "Password")
    smtp.send_message(msg)
