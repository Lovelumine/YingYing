import json
import os
from urllib.parse import urlencode
import requests
import base64
from io import BytesIO
from gsuid_core.plugins.YingYing.YingYing.train._picture_ import render_tickets_to_image
# from _picture_ import render_tickets_to_image

# 设置User-Agent和Cookie
USER_AGENT = os.getenv(
    "MY_USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
)
COOKIE = os.getenv(
    "MY_12306_COOKIE",
    "JSESSIONID=62B103BCC83AA95A52158921799A98F6; tk=fpOqDgiB7tS5nXVe3xhucVYea2TnKii92N2S3vYm2aEmkO1O0; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; BIGipServerpassport=954728714.50215.0000; route=6f50b51faa11b987e576cdb301e545c4; BIGipServerotn=568852746.50210.0000; BIGipServerportal=3084124426.17695.0000; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u4E0A%u6D77%2CSHH; _jc_save_wfdc_flag=dc; _jc_save_toDate=2024-02-06; _jc_save_fromDate=2024-02-10; uKey=cf728646e6546b8fabc26aca36a45bbfb6384b192e44784c9a39b11b806ef838",
)

headers = {
    "User-Agent": USER_AGENT,
    "Cookie": COOKIE,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive",
}

def get_tickets_and_render_image_as_bytes(from_station, to_station, travel_date):
    params = {
        "leftTicketDTO.train_date": travel_date,
        "leftTicketDTO.from_station": from_station,
        "leftTicketDTO.to_station": to_station,
        "purpose_codes": "ADULT",
    }
    url = "https://kyfw.12306.cn/otn/leftTicket/query?" + urlencode(params)

    print(f"请求的URL: {url}") 
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"响应状态码: {response.status_code}")  # 打印响应状态码
        print(f"响应内容: {response.text}")  # 打印响应内容

        response.raise_for_status()  # 这将会在响应状态码不是200时抛出异常

        tickets_data = response.json()  # 尝试解析JSON

        if tickets_data.get("status") and tickets_data["data"].get("result"):
            results = tickets_data["data"]["result"]
            tickets_json = json.dumps({"results": results})
            image_path = render_tickets_to_image(tickets_json)
            # 读取图片并直接返回字节数据
            with open(image_path, "rb") as image_file:
                image_bytes = image_file.read()
            print("车票信息图片已转换为字节格式")
            return image_bytes
        else:
            print("未找到有效的车票数据或数据格式错误")
            return None

    except requests.RequestException as e:
        print(f"网络请求异常: {e}")
        return None
    except json.JSONDecodeError:
        print("JSON解析异常")
        return None


def main():
    from_station = "BJP"  # 北京北
    to_station = "SHH"    # 上海虹桥
    travel_date = "2024-02-10"  # 出发日期

    print(f"查询从{from_station}到{to_station}，日期{travel_date}的车票信息...")

    image_bytes = get_tickets_and_render_image_as_bytes(from_station, to_station, travel_date)

    if image_bytes:
        # 保存图片到文件中进行检查
        output_image_path = "output_tickets_image.png"
        with open(output_image_path, "wb") as image_file:
            image_file.write(image_bytes)
        print(f"车票信息图片已保存到 {output_image_path}")
    else:
        print("查询失败或未找到对应的车票信息。")

if __name__ == "__main__":
    main()
