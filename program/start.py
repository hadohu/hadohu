from datetime import datetime
from sys import version_info
from time import time

from config import (
    ALIVE_IMG,
    ALIVE_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)
from program import __version__
from driver.veez import user
from driver.filters import command, other_filters
from pyrogram import Client, filters
from pyrogram import __version__ as pyrover
from pytgcalls import (__version__ as pytover)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

__major__ = 0
__minor__ = 2
__micro__ = 1

__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


@Client.on_message(
    command(["start", f"start@{BOT_USERNAME}"]) & filters.private & ~filters.edited
)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""โจ **Welcome {message.from_user.mention()} !**\n
๐ญ [{BOT_NAME}](https://t.me/{BOT_USERNAME}) **โ โข ูุณูุญ ูู ุจุงูุจุญุซ ุนู ุงูููุณููู ูุงูููุฏูู ูุชุดุบูููุง ูู ุงููุฌููุนุงุช ูู ุฎูุงู ุงููุญุงุฏุซู ุงูุตูุชูู ูู ุชููุฌุฑุงู**

๐ก **ุงูุชุดู ุฌููุน ุฃูุงูุฑ ุงูุฑูุจูุช ูููููุฉ ุนูููุง ูู ุฎูุงู ุงูููุฑ ุนูู ุฒุฑ ุงูุฃูุงูุฑ ยป๐**

๐ **ููุนุฑูุฉ ููููุฉ ุงุณุชุฎุฏุงู ูุฐุง ุงูุฑูุจูุช ุ ุงูุฑุฌุงุก ุงูููุฑ ููู ุงูุฒุฑ ยป๐ง ููููุฉ ุงูุฃุณุชุฎุฏุงู !**
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "โ ๐ ุงุถููููููู ุขููุจููฐู?ูผูู ุฅูููู ูุฌ ูู?ุนููฐููผูููฺช ๐ โ",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("๐ง ฺชููููููููุฉ ุขุณอเนูผููุฎุฏุขู ูุฐุข ุขููุฑ?ุจููฐู?ูผูู ๐ง", callback_data="cbhowtouse")],
                [
                    InlineKeyboardButton("๐ ุขููุฃ?ุขูููุฑ ๐", callback_data="cbcmds"),
                    InlineKeyboardButton("๐จโ๐ป ููููุฃุณอเนโูผููููููุณอเนโูุขเขชุขูผูู ๐ฉโ๐ป", url=f"https://t.me/{OWNER_NAME}"),
                ],
                [
                    InlineKeyboardButton(
                        "๐ฅ ุฌ ูุฑ?ุจููฐ ุขููุฏุนููฐููู ๐ฅ", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "๐ฃ ูููููุขุฉ ุขููุณอเนโู?เขชุณอเนโ  ๐ฃ", url=f"https://t.me/{UPDATES_CHANNEL}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "โโฏ แดแดแด? โข สแดสสแด โฏโ", url="https://t.me/bar_lo0o0"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_message(
    command(["alive", f"alive@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
async def alive(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("ุงูุฏุนููููููู โข โจ", url=f"https://t.me/{GROUP_SUPPORT}"),
                InlineKeyboardButton(
                    "ููููุงุฉ ุงูุณูููุฑุณ โข ๐ฃ", url=f"https://t.me/{UPDATES_CHANNEL}"
                ),
            ]
        ]
    )

    alive = f"**Hello {message.from_user.mention()}, i'm {BOT_NAME}**\n\nโจ Bot is working normally\n๐ My Master: [{ALIVE_NAME}](https://t.me/{OWNER_NAME})\nโจ Bot Version: `v{__version__}`\n๐ Pyrogram Version: `{pyrover}`\nโจ Python Version: `{__python_version__}`\n๐ PyTgCalls version: `{pytover.__version__}`\nโจ Uptime Status: `{uptime}`\n\n**Thanks for Adding me here, for playing video & music on your Group's video chat** โค"

    await message.reply_photo(
        photo=f"{ALIVE_IMG}",
        caption=alive,
        reply_markup=keyboard,
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text("๐ `PONG!!`\n" f"โก๏ธ `{delta_ping * 1000:.3f} ms`")


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "๐ค bot status:\n"
        f"โข **uptime:** `{uptime}`\n"
        f"โข **start time:** `{START_TIME_ISO}`"
    )


@Client.on_message(filters.new_chat_members)
async def new_chat(c: Client, m: Message):
    ass_uname = (await user.get_me()).username
    bot_id = (await c.get_me()).id
    for member in m.new_chat_members:
        if member.id == bot_id:
            return await m.reply(
                "**๐ฎโโ๏ธโูู ุจุชุฑููุชู ูุดุฑู ุจุงููุฌููุนู ุ**\n\n"
                "**๐ฅโูุฃุชููู ูู ุชุดุบูู ุงูููุฏูู ูุงูููุณููู ุ**\n\n"
                "**๐ฃโุชุฃูุฏ ูู ุงุนุทุงุฆู ุตูุงุญูู [ุญุฐู ุงูุฑุณุงุฆู] ุ**\n\n"
                "**ููุง ุชูุณู ูุชุงุจุฉ ูุฐุง ุงูุฃูุฑ /join ูุฏุนูุฉ ุงูุญุณุงุจ ุงููุณุงุนุฏ ููุจูุช โข ๐ถ๐ง**\n\n"
               "**ุจูุฌุฑุฏ ุงูุงูุชูุงุก ุงูุชุจ** /reload",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("ููููุงุฉ ุงูุณูููุฑุณ โข ๐ฃ", url=f"https://t.me/{UPDATES_CHANNEL}"),
                            InlineKeyboardButton("ุงูุฏุนููููููู โข ๐ญ", url=f"https://t.me/{GROUP_SUPPORT}")
                        ],
                        [
                            InlineKeyboardButton("ุงูุญูุณูุงุจ ุงูููุณูุงุนูุฏ โข ๐ค", url=f"https://t.me/{ass_uname}")
                        ]
                    ]
                )
            )
