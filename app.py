import datetime as dt
import os
import pandas as pd
from facebook_scraper import get_posts

import telegram

def lambda_handler(event, context):
    API_USERNAME = os.getenv('FB_USERNAME')
    API_KEY = os.getenv('SECRET_KEY')
    TELE_TOKEN = os.getenv('TELE_TOKEN')

    date_time = []
    link = []
    text = []

    for post in get_posts('bilahari.kausikan', pages=2, credentials=(API_USERNAME,API_KEY)):
        if post["link"] != None:
            date_time.append(post["time"])
            link.append(post["link"])
            text.append(post["text"])

    if link: 
        df = pd.DataFrame({"Time" : date_time, "Link" : link, "Text" : text})
        to_send = df[df['Time'] >= (dt.datetime.now() - dt.timedelta(hours = 24))]

        msg = '\n\n'.join(f"{i+1}: {d['Text']} \n{d['Link']} " for i,d in to_send.iterrows())
        preamble = "Good Morning! 🌅 Here's your daily dose 📫 of Bilahari posts from yesterday"
        total_msg = preamble + '\n\n' + msg

        bot = telegram.Bot(token=TELE_TOKEN)
        bot.send_message(chat_id="@bilaharibot", text=total_msg, parse_mode=telegram.ParseMode.HTML)

    else:
        total_msg = "Tis' a sad morning! 🌦️ There were no posts from Bilahari yesterday"

        bot = telegram.Bot(token=TELE_TOKEN)
        bot.send_message(chat_id="@bilaharibot", text=total_msg, parse_mode=telegram.ParseMode.HTML)

    return "Done"