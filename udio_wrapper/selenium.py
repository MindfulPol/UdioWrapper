import aiohttp
import asyncio
import json
import os
import string
import random
from aiohttp import ContentTypeError

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth

chrome_options = Options()
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("detach", True)
    
#set user data directory to the default Chrome profile
chrome_options.add_argument(r"--user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data")
chrome_options.add_argument(r'--profile-directory=Default')
chrome_options.add_argument("--disable-blink-features")
chrome_options.add_argument('--remote-debugging-port=9222')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

url = ""
session_id = ""

def randtime():
    return random.uniform(0.45, 3.0)

def page_load_complete(driver):
    return driver.execute_script("return document.readyState") == "complete"

class UdioClient:
    def __init__(self, session_cookie):
        self.session_cookie = session_cookie
        print(f"Initialized udio session cookie: {self.session_cookie}")

    def update_cookies(self, session_cookie):
        self.session_cookie = session_cookie
        print(f"Updated udio session cookie: {self.session_cookie}")

    async def create_song(self, prompt, instrumental=False, lyrics=None):
        print("Creating webdriver")
        global url, session_id
        #connect to existing chrome if open
        try:
            driver = webdriver.Remote(command_executor=url, desired_capabilities={})
            driver.close()
            driver.session_id = session_id
            print("Reusing existing chrome session")
        except:
            driver = webdriver.Chrome(options=chrome_options)
            url = driver.command_executor._url
            session_id = driver.session_id
            print("Created new chrome session at " + url + " with session: " + session_id)
            #check if more than 1 chrome session is open
            if len(driver.window_handles) > 1:
                #close the extra window
                driver.switch_to.window(driver.window_handles[1])
                driver.close()
                #switch back to the main window
                driver.switch_to.window(driver.window_handles[0])


        # Selenium Stealth settings
        stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        await asyncio.sleep(5+randtime())
        #soft navigate to udio.com if not already there
        if driver.current_url != "https://www.udio.com/" or driver.current_url != "https://www.udio.com/my-creations":
            print("Navigating to udio.com")
            driver.get("https://www.udio.com/")
            await asyncio.sleep(5+randtime())
        
        # Wait for the page to load until you can click on "my creations"
        WebDriverWait(driver, 12+randtime()).until(page_load_complete)
        #navigate to my creations by href="/my-creations"
        asyncio.sleep(randtime())
        driver.find_element(By.CSS_SELECTOR, 'a[href="/my-creations"]').click()
        
        await asyncio.sleep(randtime())

        driver.find_element(By.CSS_SELECTOR, 'input[type="prompt"]').click()
        await asyncio.sleep(randtime())

        #REMOVE ANY EMOJIS FROM PROMPT
        prompt = ''.join(filter(lambda x: x in string.printable, prompt))
        
        driver.find_element(By.CSS_SELECTOR, 'input[type="prompt"]').send_keys(prompt)
        await asyncio.sleep(randtime())
 
        if instrumental:
            driver.find_element(By.XPATH, '//div[text()="Instrumental"]').click()
            await asyncio.sleep(randtime())

        if lyrics:
            driver.find_element(By.XPATH, '//div[text()="Custom"]').click()
            element = driver.find_element(By.XPATH, '//textarea[@placeholder="Write custom lyrics here"]')
            lyrics = ''.join(filter(lambda x: x in string.printable, lyrics))
            element.send_keys(lyrics)
            #press return
            element.send_keys("\n")
            await asyncio.sleep(6+randtime())

        # Inject the JavaScript code to override the XMLHttpRequest
        driver.execute_script("""
            window.trackIds = [];
            var originalXHR = window.XMLHttpRequest;
            window.XMLHttpRequest = function() {
                var xhr = new originalXHR();
                xhr.addEventListener('load', function() {
                    if (this.responseURL.includes('/generate-proxy')) {
                        var responseText = this.responseText;
                        console.log('Response Text:', responseText);
                        
                        if (responseText.includes('"track_ids":')) {
                            var startIndex = responseText.indexOf('"track_ids":') + '"track_ids":'.length;
                            var endIndex = responseText.indexOf(']', startIndex) + 1;
                            var trackIdsString = responseText.substring(startIndex, endIndex);
                            window.trackIds = JSON.parse(trackIdsString);
                            console.log('Track IDs:', window.trackIds);
                        } else {
                            console.log('Track IDs not found in the response');
                        }
                    }
                });
                return xhr;
            };
        """)

        driver.find_element(By.XPATH, '//button[text()="Create"]').click()

        #wait for capcha check
        await asyncio.sleep(12+randtime())

        # Wait for the track IDs to be populated
        track_ids = WebDriverWait(driver, randtime()).until(
            lambda driver: driver.execute_script("return window.trackIds;")
        )

        await asyncio.sleep(randtime())
        driver.quit()
        return track_ids

    async def get_song_info(self, track_ids):
        track_id_string = ','.join(track_ids)
        async with aiohttp.ClientSession() as session:
            while True:
                async with session.get(f'https://www.udio.com/api/songs?songIds={track_id_string}',
                                    headers={
                                        'Cookie': f'sb-api-auth-token={self.session_cookie}'
                                    }) as response:
                    if response.status == 200:
                        try:
                            result = await response.json()
                        except ContentTypeError:
                            result = await response.json(content_type=None)
                        
                        songs = result.get('songs')

                        #check for moderation
                        if songs and any(song['error_type'] == 'MODERATION' for song in songs):
                            print("Song got moderated, sorry...")
                            return "Error", "song got moderated - stupid corpos..."

                        if songs and all(song['finished'] for song in songs):
                            return songs
                        await asyncio.sleep(5)
                    else:
                        print(f"Error getting song info: {response.status}")
                        return None
                    