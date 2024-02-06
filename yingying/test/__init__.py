from gsuid_core.bot import Bot
from gsuid_core.sv import SL, SV
from gsuid_core.models import Event

sv_switch = SV('测试开关')

@sv_switch.on_fullmatch('开始测试')
async def get_resp_msg(bot: Bot, ev: Event):
    await bot.send('开始多步会话测试')
    resp = await bot.receive_resp(
        '接下来你说的话我都会提取出来噢？',
    )
    if resp is not None:
        await bot.send(f'你说的是 {resp.text} 吧？')
