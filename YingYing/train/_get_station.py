# _get_station.py
import json
import os
import re

import requests


def get_station():
    """
    获取或更新12306站点信息并保存到本地文件。
    如果本地文件存在且有内容，则不重新下载。
    控制台将输出操作状态。
    """
    file_name = "gsuid_core/plugins/YingYing/data/train/station.json"

    # 检查文件是否存在且有内容
    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
        try:
            with open(file_name, "r", encoding="utf-8") as f:
                station_dict = json.load(f)
                if station_dict:
                    print("已存在站点信息文件，无需重新下载。")
                    return station_dict
        except json.JSONDecodeError as e:
            print(f"读取站点信息文件失败: {e}, 将尝试重新下载。")
        except Exception as e:
            print(f"检查站点信息文件时出错: {e}, 将尝试重新下载。")

    # 文件不存在或读取失败，重新下载数据
    url = "https://www.12306.cn/index/script/core/common/station_name.js"
    print("开始请求12306站点信息...")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 确保请求成功
        print("请求成功，开始解析站点数据...")
    except requests.RequestException as e:
        print(f"请求站点数据失败: {e}")
        return

    # 解析站点名称和英文缩写
    names = re.findall(r"([\u4e00-\u9fa5]+)\|([A-Z]+)", response.text)
    if names:
        print(f"共找到 {len(names)} 个站点信息。")
        station_dict = {name: code for name, code in names}
        # 保存数据到本地JSON文件
        try:
            with open(file_name, "w", encoding="utf-8") as f:
                json.dump(station_dict, f, ensure_ascii=False, indent=4)
            print(f"12306站点信息已经爬取完成并保存到本地文件：{file_name}")
        except IOError as e:
            print(f"保存文件失败: {e}")
    else:
        print("未找到站点信息。")
        return

    return station_dict


if __name__ == "__main__":
    get_station()
