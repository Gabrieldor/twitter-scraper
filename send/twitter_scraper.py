from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
import time
import requests

# Set up the browser
browser = webdriver.Chrome()

# Navigate to Twitter login page
url = "https://twitter.com/login"
browser.get(url)

# Pause and wait for manual login and navigation to search results
input("After logging in, navigating to search, and switching to the 'Latest' tab, press Enter to continue...")

# Function to scroll to the end of the page
def scroll_to_end(browser):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

tweet_urls = []

# Scroll multiple times to load content
for _ in range(5):  # Adjust based on how many scrolls you want
    tweet_elements = browser.find_elements(By.XPATH, "//div[@data-testid='cellInnerDiv']")
    print(f"Identified new tweets.")
    
    for tweet_element in tweet_elements:
        # More refined search to ensure we're looking at tweet images specifically
        try:
            image_elements = tweet_element.find_element(By.XPATH, ".//div[@aria-label='Image']")
        except:
            image_elements = None
        try:
            video_element = tweet_element.find_element(By.XPATH, ".//video")
        except:
            video_element = None
        if image_elements != None or video_element != None:  # If tweet contains images
            try:
                # Extracting timestamp link, which is the link to the tweet itself
                try:
                    if tweet_element.find_element(By.XPATH, ".//div[@class='css-901oao r-1bwzh9t r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0']").text == "Ad":
                        continue
                except:
                    pass
                try:
                    timestamp_link = tweet_element.find_element(By.XPATH, ".//a[@class='css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1pi2tsx r-1ny4l3l']")
                except:
                    timestamp_link = tweet_element.find_element(By.XPATH, ".//a[@class='css-4rbku5 css-18t94o4 css-901oao r-1bwzh9t r-1loqt21 r-xoduu5 r-1q142lx r-1w6e6rj r-37j5jr r-a023e6 r-16dba41 r-9aw3ui r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0']")
                
                tweet_urls.append(timestamp_link.get_attribute("href"))
                print("Image Scraped")
            except:
                print(tweet_element.text)
                print(traceback.format_exc())
                print("Error extracting URL for a tweet, it didn't had video or image")

    scroll_to_end(browser)

# Find all tweets
tweet_urls = list(set(tweet_urls))

# List to store URLs
print(tweet_urls)

# Save URLs to a text file
with open("tweets_with_images.txt", "w") as file:
    for url in tweet_urls:
        file.write(f"{url}\n")


print(f"Saved {len(tweet_urls)} tweet URLs to tweets_with_images.txt")
print("Starting Download!")

for link in tweet_urls:
    browser.get(link)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//time")))
    print(browser.page_source)
    time_name = browser.find_element(By.XPATH, "//time").get_attribute("datetime").replace("T", " ").replace(":", "-")
    try:
        srcs = browser.find_elements(By.XPATH, "//div[@data-testid='tweetPhoto']/img")
        for src in srcs:
            if "media" in src.get_attribute("src"):
                src = src.get_attribute("src")

        extension = ".png"
    except:
        src = browser.find_element(By.XPATH, "//video").get_attribute("src")
        extension = ".mp4"
        

    name = time_name + extension

    
    try:
        r = requests.get(src)
        with open(f"output/{name}", 'wb') as f:
                f.write(r.content)
    except:
            pass

# Close the browser
browser.close()
