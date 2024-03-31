import asyncio
import traceback  # 用于记录堆栈跟踪

from gsuid_core.bot import Bot
from gsuid_core.models import Event
from gsuid_core.sv import SV

from gsuid_core.plugins.YingYing.YingYing.train._get_station import get_station
from gsuid_core.plugins.YingYing.YingYing.train._get_tickets import get_tickets_and_render_image_as_bytes

sv_ticket = SV("火车票查询服务")

@sv_ticket.on_fullmatch(["查询火车票", "火车"])
async def query_ticket_init(bot: Bot, ev: Event):
    # 启动多步对话，先发送欢迎信息
    await bot.send("欢迎使用火车票查询服务，请输入出发站，目的站和出发日期（格式如：北京 上海 2024-02-10）。")
    # 等待用户回复
    resp = await bot.receive_resp()
    if resp is not None:
        # 处理用户回复
        await query_ticket_with_input(bot, resp, resp.text)

@sv_ticket.on_prefix(["火车"])
async def query_ticket_with_prefix(bot: Bot, ev: Event):
    # 由于框架自动处理前缀，可以直接使用ev.text获取去除前缀后的命令
    await query_ticket_with_input(bot, ev, ev.text.strip())

async def query_ticket_with_input(bot: Bot, ev: Event, user_input: str):
    try:
        parts = user_input.split()
        if len(parts) != 3:
            raise ValueError("输入格式不正确。")

        from_station, to_station, travel_date = parts

        station_dict = get_station()
        if not station_dict:
            await bot.send("站点信息加载失败，请稍后再试。")
            return

        from_code = station_dict.get(from_station)
        to_code = station_dict.get(to_station)
        if not from_code or not to_code:
            await bot.send("站点名称有误，请重新输入。")
            return

        image_bytes = get_tickets_and_render_image_as_bytes(from_code, to_code, travel_date)
        if image_bytes:
            await bot.send(f"查询成功，以下是{from_station}到{to_station}，日期{travel_date}的车票信息：")
            await bot.send(image_bytes)  # 直接发送字节数据
        else:
            await bot.send("查询失败或未找到对应的车票信息。")

    except ValueError as e:
        print(f"解析用户输入时发生错误：{e}")
        await bot.send("输入格式有误，请按照“出发站 目的站 出发日期”格式输入，例如：北京 上海 2024-02-10。")
    except Exception as e:
        error_info = traceback.format_exc()
        print(f"查询过程中发生未预期的错误：{e}\n完整堆栈跟踪信息：\n{error_info}")
        await bot.send("查询过程中发生了一个错误，请稍后再试。")
