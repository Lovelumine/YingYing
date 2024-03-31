from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time
import hashlib
import os

class TrainTicketFetcher:
    def __init__(self):
        self.chrome_options = Options()
        # 禁用GPU加速，有助于减少某些平台的bug
        self.chrome_options.add_argument("--disable-gpu")
        # 启用无头模式，这样就不会打开GUI界面
        self.chrome_options.add_argument("--headless")
        # 添加其他必要的选项以支持无头模式下的正常运行
        self.chrome_options.add_argument("--no-sandbox")  # 绕过OS安全模型
        self.chrome_options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
        self.chrome_options.add_argument("start-maximized")  # 开始最大化，有助于避免某些元素不可见
        self.chrome_options.add_argument("enable-automation")  # 忽略导航栏警告
        self.chrome_options.add_argument("--disable-infobars")  # 隐藏"Chrome正在受到自动软件的控制"
        self.chrome_options.add_argument("--disable-extensions")  # 禁用扩展
        self.chrome_options.add_argument("--disable-browser-side-navigation")  # 禁用浏览器导航
        self.target_dir = os.path.join(os.getcwd(), "gsuid_core", "plugins", "YingYing", "data", "train")
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)  # 如果目标目录不存在，则创建它
        self.cookies_file_path = os.path.join(self.target_dir, "cookies.json")

    def get_and_save_cookies(self):
        driver = webdriver.Chrome(options=self.chrome_options)
        print("访问12306首页...")
        driver.get("https://kyfw.12306.cn/otn/resources/login.html")
        time.sleep(5)  # 等待页面加载完成
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
        driver.get("https://kyfw.12306.cn/otn/resources/login.html")
        cookies = self.load_cookies()
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get(url)
        time.sleep(2)  # 等待页面加载完成
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
    target_url = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2024-02-10&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=SHH&purpose_codes=ADULT"
    html_save_path = fetcher.use_cookies_to_fetch_and_save_data(target_url)
    print(f"HTML文件保存地址: {html_save_path}")
