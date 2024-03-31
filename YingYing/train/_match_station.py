# _match_station.py
import json


def load_station_dict():
    """加载站点字典"""
    file_path = "gsuid_core/plugins/YingYing/data/train/station.json"
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"加载站点字典失败: {e}")
        return {}


def match_station(input_station, station_dict):
    """模糊匹配站点名称到站点代码"""
    matched_station = None
    for name, code in station_dict.items():
        if input_station in name:
            matched_station = code
            break
    if matched_station:
        print(f"匹配到站点: {input_station} -> {matched_station}")
    else:
        print(f"未找到匹配的站点: {input_station}")
    return matched_station
