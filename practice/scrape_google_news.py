import requests
import json
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from termcolor import colored as cl
import datetime
import time
from decouple import config
from urllib.request import urlopen

current_time = datetime.datetime.now()

content_body = ""


def get_google_news(news_path):
    print("[+]" + cl(" FETCHING WORLD NEWS HEADLINE ", 'red') + "[+]")
    news_extract = str()
    news_extract += ("<br><b>LATEST WORLD NEWS</b><br>\n" +
                     "<br>" + "=" * 20 + "<br>")
    news_response = requests.get(news_path)
    soup_content = news_response.content
    soup_obj = BeautifulSoup(soup_content, 'html.parser')

    for x, tags in enumerate(soup_obj.find_all('h3', attrs={'class': 'ipQwMb ekueJc RD0gLb'})):
        news_id = str(x + 1)
        news_text_body = tags.text
        link_addr = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen"
        link_message = "Read more..."
        news_extract += ("<br /><br />" + news_id + "::" + news_text_body + "<br />"
                         + "<a href='{}'>".format(link_addr) + f"{link_message}" + "</a>"
                         if news_text_body != 'More' else '')

    return news_extract


news_compose = get_google_news(
    'https://news.google.com/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNR3QwTlRFU0FtVnVLQUFQAQ?hl=en-US&gl=US&ceid=US%3Aen'
)
content_body += news_compose
content_body += "\n<br /> ************************ <br />"
content_body += "<br /><br /><b> END OF LATEST INFLUENTIAL NEWS</b> <br />"

email_list = ['jeckonia23@gmail.com', 'alvan55zecky@gmail.com', 'Petermuia280@gmail.com', 'Senelwajabez1234@gmail.com',
              'francismarwa2@gmail.com', 'dantemilimo@gmail.com', 'jeckoniaonyango051@gmail.com',
              'mzametonny@gmail.com', 'amosdissappointed@gmail.com', 'kabericollins923@gmail.com',
              'vinyodinga@gmail.com', ]

ip_data_load = json.loads(urlopen('http://httpbin.org/ip').read())
prev_public_ip = ip_data_load['origin']

while True:
    data_pre = json.loads(urlopen('http://httpbin.org/ip').read())
    current_public_ip = data_pre['origin']
    if current_public_ip != prev_public_ip:
        try:
            for x in email_list:
                SERVER = config('server')
                PORT = config('email_port', default=587)
                FROM = config('Sender_address')
                TO = x
                PASSWORD = config("sender_pass")
                msg = MIMEMultipart()
                msg['Subject'] = "AUTOMATED EMAIL GOOGLE CRAWLER " + str(current_time.year) \
                                 + "/" + str(current_time.month) + "/" + str(current_time.day)
                msg['From'] = FROM
                msg['To'] = TO

                msg.attach(MIMEText(content_body, 'html'))
                server = smtplib.SMTP(SERVER, PORT)
                server.set_debuglevel(1)
                server.ehlo()
                server.starttls()
                server.login(FROM, PASSWORD)
                server.sendmail(FROM, TO, msg.as_string())
                server.quit()
                print("MAIL SENT")
                time.sleep(720)
        except smtplib.SMTPException:
            print("Error with the SMTP Server\nResolving.......")
