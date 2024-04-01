import sys

sys.path.append("../../src/")

from datetime import datetime

from melobot import BotPlugin, ForwardWsConn, MeloBot, msg_event, send, send_reply

plugin = BotPlugin(__name__, "1.0.0")
OWNER_QID = 1574260633


@plugin.on_start_match(".hello")
async def say_hi() -> None:
    # send_reply 第一参数与 send 完全相同
    e = msg_event()
    if e.sender.id != 1574260633:
        await send_reply("你好~ 你不是我的主人哦")
        return
    # 接下来是机器人主人的处理逻辑
    await send(">w<")
    await send("主人好")

if __name__ == "__main__":
    bot = MeloBot(__name__)
    bot.init(ForwardWsConn("127.0.0.1", 8080))
    bot.load_plugin(plugin)
    bot.run()
