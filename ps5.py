from selenium import webdriver
from time import sleep
import yaml
import os
import subprocess
import logging
from random import randrange


# Configure logging
log_format = '%(asctime)s - %(levelname)s - %(message)s'
LOG_LEVEL = os.getenv("LOG_LEVEL", default=logging.INFO)
logging.basicConfig(format=log_format, level=LOG_LEVEL)
logger = logging.getLogger(__name__)


def load_config():
    with open("config.yaml", 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def notify(title, text):
    CMD = '''on run argv
        display notification (item 2 of argv) with title (item 1 of argv)
        end 
    '''
    subprocess.call(['osascript', '-e', CMD, title, text])


class PS5Bot():
    def __init__(self, chrome_driver, item_url):
        self.driver = webdriver.Chrome(chrome_driver)
        self.item_url = item_url

    def login(self):
        self.driver.get('https://www.amazon.de')
        sleep(5)

    def check_ps5(self):
        # you can use 'controller' to test the script
        self.driver.get(self.item_url)
        while True:
            stock  = self.driver.find_element_by_xpath('//*[@id="availability"]/span').text
            if stock == "In stock.":
                logger.warning("PS5 in stock on Amazon.de, go and buy: {}".format(self.item_url))
                notify("PS5 Status Report", "PS5 IN STOCK!!!")
            elif stock == "Currently unavailable.":
                logger.info("PS5 status: {} :(".format(stock))
            else:
                logger.error("Script misconfigured")
            random_sleep = randrange(60,90)
            sleep(random_sleep)
            self.driver.refresh()
        self.driver.quit()

    def buy_ps5(self):
        pass


def main():
    conf = load_config()
    chrome_driver = conf['chrome_driver']
    # switch the below lines if you want to test your notification
    # item_url = conf['controller']
    item_url = conf['ps5']
    bot = PS5Bot(chrome_driver, item_url)
    bot.check_ps5()


if __name__ == "__main__":
    main()