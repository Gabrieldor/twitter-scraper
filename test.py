from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta
from random import randint
import os
import traceback
import time
import requests

with open("aa.txt") as f:
    tweet_urls = [x.strip() for x in f.readlines()]

print(len(tweet_urls))

browser = webdriver.Chrome()
url = "https://twitter.com/login"
browser.get(url)
input()

for link in tweet_urls:
    browser.get(link)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//article")))
    stop = False
    for art in browser.find_elements(By.XPATH, "//article"):
        for a in art.find_elements(By.XPATH, ".//a"):
            print(link.split("status/")[1].replace("/photo/1", ""))
            if link.split("status/")[1].replace("/photo/1", "") in a.get_attribute("href"):
                if stop == False:
                    article = art
                stop = True
                break

    print(art.text)
    input()
    t = datetime.strptime(art.find_element(By.XPATH, ".//time").get_attribute("datetime")[:-1], '%Y-%m-%dT%H:%M:%S.%f')
    t = t + timedelta(hours=4, milliseconds=randint(0,999))
    time_name = t.strftime("%Y-%m-%d %H-%M-%S.%f")[:-3]
    try:
        imgs = article.find_elements(By.XPATH, ".//div[@data-testid='tweetPhoto']/img")
        if not imgs:
            try:
                browser.find_element(By.XPATH, "//video")
                with open("tweets_videos.txt", "a") as file:
                        file.write(f"{link}\n")
                continue
            except:
                print(traceback.format_exc())
        for img in imgs:
            src = img.get_attribute("src")
            extension = ".png"
            with open("tweets_imgs.txt", "a") as file:
                        file.write(f"{link}\n")

            name = time_name + extension            

            if os.path.exists("output/"+name):
                print("TEM IGUALAAAAAAAAAA")
                name = time_name + f"{randint(0,99)}" +extension
        
            try:
                r = requests.get(src)
                with open(f"output/{name}", 'wb') as f:
                        f.write(r.content)
                
            except:
                pass
    except:
       pass

   