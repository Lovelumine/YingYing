import json
from urllib.parse import urlencode
import os
import base64
from io import BytesIO
from bs4 import BeautifulSoup  # 引入BeautifulSoup库进行HTML解析

# 假设 render_tickets_to_image 和 TrainTicketFetcher 已经按照之前的描述实现
from gsuid_core.plugins.YingYing.YingYing.train._picture_ import render_tickets_to_image
from gsuid_core.plugins.YingYing.YingYing.train.chrome import TrainTicketFetcher


def extract_tickets_data_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    # 假设车票信息包含在<pre>标签内
    pre_tag = soup.find('pre')
    if pre_tag:
        tickets_data = json.loads(pre_tag.text)  # 解析<pre>标签内的文本作为JSON
        return tickets_data
    else:
        print("未找到<pre>标签或车票信息。")
        return None


def get_tickets_and_render_image_as_bytes(from_station, to_station, travel_date):
    params = {
        "leftTicketDTO.train_date": travel_date,
        "leftTicketDTO.from_station": from_station,
        "leftTicketDTO.to_station": to_station,
        "purpose_codes": "ADULT",
    }
    url = "https://kyfw.12306.cn/otn/leftTicket/query?" + urlencode(params)
    fetcher = TrainTicketFetcher()
    print(f"请求的URL: {url}")
    file_path = fetcher.use_cookies_to_fetch_and_save_data(url)
    tickets_data = extract_tickets_data_from_html(file_path)

    if tickets_data and tickets_data.get("data") and tickets_data["data"].get("result"):
        results = tickets_data["data"]["result"]
        tickets_json = json.dumps({"results": results})
        # 修改这里，确保图片保存在同一个目录并且名称与HTML相同
        image_path = file_path.replace('.html', '.png')  # 使用相同的路径，但扩展名改为.png
        render_tickets_to_image(tickets_json, image_path)  # 确保这个函数可以接收image_path作为参数
        # 读取图片并直接返回字节数据
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()
        print("车票信息图片已转换为字节格式")

        # 删除图片和HTML文件
        os.remove(file_path)
        os.remove(image_path)

        return image_bytes
    else:
        print("未找到有效的车票数据或数据格式错误")
        # 删除HTML文件，即使未生成图片
        os.remove(file_path)
        return None


def main():
    # 示例调用，替换为实际参数
    from_station = 'BJP'
    to_station = 'SHH'
    travel_date = '2024-02-11'
    print("从12306获取车票信息并生成图片...")

    image_bytes = get_tickets_and_render_image_as_bytes(from_station, to_station, travel_date)

    if image_bytes:
        # 示例：保存图片到文件中进行检查，这里不再需要，因为图片已经被删除
        # output_image_path = "output_tickets_image.png"
        # with open(output_image_path, "wb") as image_file:
        #     image_file.write(image_bytes)
        # print(f"车票信息图片已保存到 {output_image_path}")
        pass
    else:
        print("查询失败或未找到对应的车票信息。")


if __name__ == "__main__":
    main()
