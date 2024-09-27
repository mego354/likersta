from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time

class InstagramLikerCollector:
    def __init__(self, username, password, post_url, headless=False):
        self.username = username
        self.password = password
        self.post_url = post_url
        self.driver = self.setup_driver(headless)

    def setup_driver(self, headless):
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        return driver

    def login_to_instagram(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(self.username)
            self.driver.find_element(By.NAME, "password").send_keys(self.password)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
            
            # Ensure login is successful by checking the URL
            WebDriverWait(self.driver, 10).until(EC.url_contains("instagram.com"))
        except Exception as e:
            print(f"Login failed: {e}")
            self.driver.quit()
            exit(1)

    def read_likers(self, usernames):
        elements = self.driver.find_elements(By.XPATH, "//span[contains(@class, '_aacl') or contains(@class, '_aacx')]")
        for element in elements:
            try:
                username = element.text
                if username and username not in usernames:
                    usernames.add(username)
            except Exception as e:
                print(f"Error retrieving username: {e}")
        return usernames

    def scroll_and_collect(self):
        usernames = set()
        total_page_height = self.driver.execute_script("return document.body.scrollHeight")
        print(total_page_height)
        scroll_position = 0

        while scroll_position < total_page_height:
            usernames = self.read_likers(usernames)

            body = self.driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.PAGE_DOWN)  # Simulate pressing "Page Down"
            time.sleep(2)

            scroll_position = self.driver.execute_script("return window.scrollY + window.innerHeight")
            print(scroll_position)

        return usernames

    def get_likers(self):
        if 'reel' in self.post_url:
            self.post_url = self.post_url.replace('reel', 'p')

        likers_url = f"{self.post_url}liked_by/"
        print(f"Accessing likers URL: {likers_url}")
        self.driver.get(likers_url)

        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(5)
        
        usernames = self.scroll_and_collect()
        return usernames

    def run(self):
        try:
            self.login_to_instagram()
            time.sleep(10)

            likers = self.get_likers()
            print("Usernames of likers:")
            for liker in sorted(likers):
                print(liker)
            print(f"Total likers collected: {len(likers)}")
            print(f"--------------------------------------")
        finally:
            self.driver.quit()

if __name__ == "__main__":
    # Replace with your actual Instagram username, password, and post URL
    username = 'mahmoud_zaki_megahd'
    password = '@adminnnn'
    post_url = 'https://www.instagram.com/reel/C_upqRsyHaG/'

    collector = InstagramLikerCollector(username, password, post_url, headless=False)
    collector.run()
