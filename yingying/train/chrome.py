from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time
import hashlib
import os

class TrainTicketFetcher:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--disable-gpu")
        self.target_dir = os.path.join(os.getcwd(), "gsuid_core", "plugins", "YingYing", "data", "train")
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)  # 如果目标目录不存在，则创建它
        self.cookies_file_path = os.path.join(self.target_dir, "cookies.json")

    def get_and_save_cookies(self):
        driver = webdriver.Chrome(options=self.chrome_options)
        print("访问12306首页...")
        driver.get("https://kyfw.12306.cn")
        time.sleep(2)  # 等待页面加载完成
        print("访问完毕。")
        cookies = driver.get_cookies()
        print(f"获取到的Cookies: {cookies}")
        with open(self.cookies_file_path, "w") as f:
            json.dump(cookies, f)
            print("Cookies已保存到本地。")
        driver.quit()

    def load_cookies(self):
        try:
            with open(self.cookies_file_path, "r") as f:
                cookies = json.load(f)
                print("从本地加载Cookies成功。")
                return cookies
        except FileNotFoundError:
            print("本地Cookies文件不存在，重新获取...")
            self.get_and_save_cookies()
            return self.load_cookies()

    def use_cookies_to_fetch_and_save_data(self, url):
        driver = webdriver.Chrome(options=self.chrome_options)
        driver.get("https://kyfw.12306.cn")
        cookies = self.load_cookies()
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get(url)
        time.sleep(5)  # 等待页面加载完成
        url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        filename = f"page_content_{url_hash}.html"
        file_path = os.path.join(self.target_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
            print(f"页面内容已保存到本地: {file_path}")
        driver.quit()
        return file_path

if __name__ == "__main__":
    fetcher = TrainTicketFetcher()
    target_url = "https://kyfw.12306.cn/otn/leftTicket/queryE?leftTicketDTO.train_date=2024-02-11&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=SHH&purpose_codes=ADULT"
    html_save_path = fetcher.use_cookies_to_fetch_and_save_data(target_url)
    print(f"HTML文件保存地址: {html_save_path}")
