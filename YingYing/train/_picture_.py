import json
from PIL import Image, ImageDraw, ImageFont

def parse_ticket_info(ticket_data):
    # 解析单条车次信息
    data = ticket_data.split("|")
    info = {
        "train_no": data[3],  # 车次
        "from_to": f"{data[6]}->{data[7]}",  # 出发站->到达站
        "starttime": data[8],  # 出发时间
        "endtime": data[9],  # 到站时间
        "duration": data[10],  # 历时
        "seat_info": {
            "商务/特等座": data[32] or "--",
            "一等座": data[31] or "--",
            "二等座": data[30] or "--",
            "高级软卧": data[21] or "--",
            "软卧": data[23] or "--",
            "动卧": data[33] or "--",
            "硬卧": data[28] or "--",
            "无座": data[26] or "--",
        },
    }
    return info

def render_tickets_to_image(tickets_json, image_path):
    # 解析JSON数据
    tickets_data = json.loads(tickets_json)
    results = tickets_data["results"]

    # 准备绘图
    img_width = 1000
    row_height = 50  # 增加行高以适应更大的字体
    header_height = 40  # 为标题设置较大的高度
    img_height = header_height + row_height * len(results)
    image = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(image)

    # 使用已安装的文泉驿正黑字体
    font_path = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
    header_font_size = 18  # 标题行较大字体大小
    detail_font_size = 22  # 详情行较大字体大小
    header_font = ImageFont.truetype(font_path, header_font_size)
    detail_font = ImageFont.truetype(font_path, detail_font_size)

    # 定义颜色
    header_color = "darkblue"  # 标题颜色
    text_color = "black"  # 文本颜色
    alternate_row_color = "#F0F0F0"  # 交替行的背景色

    # 绘制标题背景
    draw.rectangle([0, 0, img_width, header_height], fill=alternate_row_color)

    # 绘制标题
    headers = [
        "车次", "出发站->到达站", "出发时间", "到站时间", "历时",
        "商务/特等座", "一等座", "二等座", "高级软卧", "软卧", "动卧", "硬卧", "无座"
    ]
    column_widths = [70, 140, 90, 90, 70, 100, 60, 60, 90, 50, 50, 50, 50]
    x_offset = 0
    for i, header in enumerate(headers):
        draw.text((x_offset, 0), header, fill=header_color, font=header_font)
        x_offset += column_widths[i]

    # 绘制车次信息
    y_offset = header_height
    for index, ticket in enumerate(results):
        if index % 2 == 1:  # 为每个交替的行添加背景色
            draw.rectangle([0, y_offset, img_width, y_offset + row_height], fill=alternate_row_color)
        x_offset = 10
        info = parse_ticket_info(ticket)
        details = [
            info["train_no"], info["from_to"], info["starttime"], info["endtime"], info["duration"],
            info["seat_info"]["商务/特等座"], info["seat_info"]["一等座"], info["seat_info"]["二等座"],
            info["seat_info"]["高级软卧"], info["seat_info"]["软卧"], info["seat_info"]["动卧"],
            info["seat_info"]["硬卧"], info["seat_info"]["无座"]
        ]
        for i, detail in enumerate(details):
            draw.text((x_offset, y_offset), detail, fill=text_color, font=detail_font)
            x_offset += column_widths[i]
        y_offset += row_height

    # 保存图片
    image.save(image_path)
    return image_path



# 假定的JSON数据字符串
tickets_json = """
{
  "results": [
    "cTPmqV7zZx92IPIX%2FLsy5fJTwiOejp3X01f4MVVUNTN09Jto5Qp8DB7I4aOjuvSbqV5TcrgyhcQU%0AQd3csxRwyk%2BNkXOyg083eJNVQlti16RODlbpPcQEybmOQvMy%2FZhll8lSye3V8v%2BP2ZISD2KHrBv1%0AHnqDrS7VWLf2XN1%2Bq5Y3iO%2Bno8Y%2BLIrICJAtZUEq9Z7drqVkjFzB8tI3QyNrZ7AjNka84NoBDJS9%0Ay33PhLhRRKg9UAePxasjZgAsFMFuCvPl%2BxR5BYQd448F%2FwOzVPZQaZ5s%2BBWxeV6d8KqofLBeMdZ5%0ArES17jjKwYOfGezIRPft%2BxkXfhFQYO9XMP%2FQDftiix0%3D|预订|24000000D520|D5|BJP|SHH|BJP|SHH|21:21|09:27|12:06|Y|NQAj2sETyyA%2ByHmaglreY%2Fql6jaTb4I7gaedNF2wcKc2dzwdQUKAK%2BGud9k%3D|20240209|3|P4|01|05|1|0||||有|||有||有||有||||I0J0O0W0|IJOO|1|0||I068600021J054200021O036100021O036103036|0|||||1|0#1#0#0#z#0#IJ|||CHN,CHN|||N#N#|I306860I107770J305420J106320J205780|I3080I1080J3081J1080J2081O0080W0080|202401261000|",
    "rOcDUAW1zIxju3p78Y8VuFMmZIOnfrVGdZSHbJ%2B%2B587%2F6gKQuKQtTJ25KQsABAXkDdBi6DM2atzi%0A3eTUH5PobPyrqB5NHO5I6vj9rFeZVhhiQg%2BKcxTIz9Kiq5MGNh0haKxk5mt%2BCOFp0XRDJWVt1RD9%0AWvCktmg%2FWg9hPhmxiAoxBvKHtvOzJfTKkcoHwgLHBQ8BSJMQVEuCHBg%2FpZ04MUd8k%2By2UKYycFtl%0AmbUUEAFBuwetZLU5joDPV0x8Qaa6xALHnDM73CEO52sEnL1MsoAUuLBjqk%2FHOJP79Sn%2FCzhdEoFO%0AP95Z6IMoAPQNg0LPNiOHDA8WZLZD0HAM|预订|24000000G300|G3|VNP|SHH|VNP|SHH|08:00|12:32|04:32|Y|XRegS7nw9gh5NfiHmRaMluRtMoTRFYDuvhthFhOhGW8nJ5mV|20240209|3|P3|01|04|1|0|||||||||||有|有|无||90M0O0|9MO|1|1||9233100000M106700021O066700021|0|||||1|0#1#0#0#z#0#z|||CHN,CHN|||N#N#|||202401261230|"
  ]
}
"""

# 调用函数并渲染图片
image_path = render_tickets_to_image(tickets_json,"ok.png")
print(f"生成的图片路径为: {image_path}")
