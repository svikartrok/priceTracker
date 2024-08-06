 
import smtplib
import pandas as pd
import requests
from bs4 import BeautifulSoup
from price_parser import Price
from icecream import ic
from datetime import datetime
import pytz
import os

PRODUCT_URL_CSV = "data/products.csv"
SAVE_TO_CSV = True
PRICES_CSV = "data/prices.csv"
SEND_MAIL = True
TIMESTAMP = datetime.now(pytz.timezone('Europe/Berlin')).strftime('%Y-%m-%d %H:%M:%S')

# email variables, get from docker system
MAIL_USER = os.environ['MAIL_USER']
MAIL_PASS = os.environ['MAIL_PASS']
MAIL_TO = os.environ['MAIL_TO']


def get_urls(csv_file):
    df = pd.read_csv(csv_file)
    return df

def get_response(url):
    response = requests.get(url)
    return response.text

def get_price(html, selector):
    soup = BeautifulSoup(html, "lxml")
    el = soup.select_one(selector)
    price = Price.fromstring(el.text)
    ret = 0
    try:
        ret = price.amount_float
    except:
        # TODO mal lepši logging?
        ic(TIMESTAMP)
        ic(el)
        ic(price)
        send_mail_ex(f"{TIMESTAMP} | {el} | {price}")
    finally:
        return ret

def process_products(df: pd.DataFrame):
    updated_products = []
    for product in df.to_dict("records"):
        if product["active"] == "D":
            try:
                html = get_response(product["url"])
                product["price"] = get_price(html, product["css_selector"])
            except Exception as e:
                ic(e)
                send_mail_ex(e)
            product["alert"] = product["price"] < product["alert_price"]
            product["timestamp"] = TIMESTAMP
            updated_products.append(product)
    return pd.DataFrame(updated_products)

def get_mail(df: pd.DataFrame):
    subject = "Price Drop Alert"
    body = df[df["alert"]].to_string()
    subject_and_message = f"Subject:{subject}\n\n{body}"
    return subject_and_message

def send_mail_from_df(df: pd.DataFrame):
    if df[df["alert"]].empty:
        return

    message_text = get_mail(df)
    send_mail(message_text)
    
def send_mail(message_text):
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(MAIL_USER, MAIL_PASS)
        smtp.sendmail(MAIL_USER, MAIL_TO, message_text)

def send_mail_ex(message):
    send_mail(f"Subject:{'Exception in tracker.py'}\n\n{message}")

def main():
    df = get_urls(PRODUCT_URL_CSV)
    df_updated = process_products(df)
    if SAVE_TO_CSV:
        df_updated.to_csv(PRICES_CSV, index=False, mode="a", header=False,columns=["product_id","price","timestamp"])
    if SEND_MAIL:
        send_mail_from_df(df_updated)

if __name__ == "__main__":
    main()