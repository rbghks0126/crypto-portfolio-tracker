from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from datetime import datetime
import time
import pandas as pd


def get_staking_element(url, sleep_time):

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    time.sleep(sleep_time)
    p_element = driver.find_elements(By.CLASS_NAME, "_1nv4amt6o")
    return p_element, driver
