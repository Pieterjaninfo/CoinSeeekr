import cfscrape
import re
import smtplib
from time import sleep
import sys

# Constant variables and initializations
REGEX = '\d beschikbaar'
SENDER = 'coinseeekr@gmail.com'
RECEIVERS = ['pieterjaninfo@gmail.com', 'roelofsbalkbrug@online.nl', 'roelofsroland@gmail.com', 'alrikhummerboy@hotmail.com']
SEND_DELAY = 60
LOOP_DELAY = 5

#Create instance handlers
scraper = cfscrape.create_scraper() # CloudflareScrapper
reg = re.compile(REGEX) # Regex handler


def get_data(coin_url):
    """ Returns the web-page html code. """
    return scraper.get('https://www.litebit.eu/nl/kopen/{}'.format(coin_url)).content


def process_data(raw_data):
    """ Processes the raw data and returns how many coins are available. """
    data = reg.findall(raw_data)
    return data[0].split(' ')[0] if (len(data) > 0) else None

def send_mail(subject, message):
    """ Sends a mail from the SENDER to the RECEIVERS with the given message. """
    msg = 'Subject: {0}\n\n{1}'.format(subject, message)
    try:
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(SENDER, 'kojwnskek')
        smtp.sendmail(SENDER, RECEIVERS, msg)
        smtp.quit()
        print("Send mails successfully.")
    except Exception:
        print("Unable to send mail.")


if __name__ == '__main__':
    print("Program started...")
    #send_mail('Eeerste mailtje - PJ', 'Verwijder mij ff van je spam -PJ')
    reset = True
    while True:
        coin_type = 'reddcoin'
        amount_coins = process_data(str(get_data(coin_type)))
        if amount_coins != None and int(amount_coins) != 0 and reset:
            send_mail('Coins available', 'There are {0} {1} coins available!'.format(amount_coins, coin_type))
            print("Coins detected!")
            #sleep(SEND_DELAY)
        elif amount_coins != None:
            print("TICK")
        else:
            reset = False
            print("TICK failed")
        sleep(LOOP_DELAY)
