import pickle
from selenium import webdriver
import time
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import pandas as pd
import time

# Function to load cookies from a .pkl file into the browser
def load_cookies(driver, pkl_filename="cookies.pkl"):
    with open(pkl_filename, 'rb') as file:  # Open the file in binary mode
        cookies = pickle.load(file)  # Deserialize the cookies
        for cookie in cookies:
            # Modify the sameSite attribute to "Lax" if it doesn't exist or isn't valid
            if "sameSite" in cookie:
                if cookie["sameSite"] not in ["Strict", "Lax", "None"]:
                    cookie["sameSite"] = "Lax"  # Default value

            else:
                cookie["sameSite"] = "Lax"  # Default value for cookies without sameSite attribute

            driver.add_cookie(cookie)  # Add each cookie to the browser session

# Function to run the browser with cookies from the .pkl file
def access_with_cookies():
    options = webdriver.FirefoxOptions()
    options.headless = True  # Run browser in headless mode for automation

    driver = webdriver.Firefox(options=options)
    driver.get("https://x.com")  # Visit the URL to set the domain where the cookies are valid

    # Load cookies from the .pkl file into the browser session
    load_cookies(driver)

    # Refresh the page to apply the cookies
    driver.refresh()
    time.sleep(5)  # Wait for the page to load completely after refreshing

    driver.get("https://x.com/elonmusk")  
    time.sleep(2)

    print(driver.title)  # Print the title of the page to confirm we're logged in
    
    if True:
        elon_url = "https://x.com/elonmusk"
        driver.get(elon_url)
        time.sleep(5)

        tweet_times = []

        for _ in range(3):
            tweet_elements = driver.find_elements(By.TAG_NAME, "time")
            tweet_times.extend([tweet.get_attribute("datetime") for tweet in tweet_elements])

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)

        df = pd.DataFrame(tweet_times, columns=["datetime"])
        df["datetime"] = pd.to_datetime(df["datetime"])


        df.to_csv("ElonTweets.csv", index=False)
        print(f"Scraped {len(df)} tweets")

        return df
    
    else:
        driver.quit()

    

    # Optionally, interact with the page
    # For example: scraping tweets, interacting with the UI, etc.
    # You can use driver.find_elements, driver.find_element, etc.

    driver.quit()  # Close the browser after you're done

# Call the function to access the site using cookies
access_with_cookies()
