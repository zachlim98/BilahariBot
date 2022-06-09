import datetime as dt
import os
import pandas as pd
from facebook_scraper import get_posts

from decouple import config, AutoConfig
import telegram

def lambda_handler(event, context):
    API_USERNAME = config('FB_USERNAME')
    API_KEY = config('SECRET_KEY')
    TELE_TOKEN = config('TELE_TOKEN')

    date_time = []
    link = []
    text = []

    for post in get_posts('bilahari.kausikan', pages=1, credentials=(API_USERNAME,API_KEY)):
        if post["link"] != None:
            date_time.append(post["time"])
            link.append(post["link"])
            text.append(post["text"])

    df = pd.DataFrame({"Time" : date_time, "Link" : link, "Text" : text})
    df["Date"] = df['Time'].dt.date
    to_send = df[(df['Date'] == dt.datetime.now().date())]

    msg = '\n\n'.join(f"{i}: {d['Text']} \n{d['Link']} " for i,d in to_send.iterrows())
    preamble = "Good Morning! 🌅 Here's your daily dose 📫 of Bilahari posts from yesterday"
    total_msg = preamble + '\n\n' + msg

    # use token generated in first step
    bot = telegram.Bot(token=TELE_TOKEN)
    status = bot.send_message(chat_id="@bilaharibot", text=total_msg, parse_mode=telegram.ParseMode.HTML)