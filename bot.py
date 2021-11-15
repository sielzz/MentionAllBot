import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("__**Halo Anak Yatim Saya Mention Bot Sielzz**, Saya dapat menyebutkan hampir semua anggota di grup atau saluran 👻\nPencet **/help** Untuk Informasi Lebih Lanjut__\n\n Tuan Gua [sielzz](https://t.me/arsilaf) on Telegram",
                    buttons=(
                      [Button.url('📣 Channel', 'https://t.me/sielzzproject'),
                      Button.url('🗣️ Tuan Gua', 'https://t.me/arsilaf')]
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**Menu Bantuan dari Mention Bot Sielzz**\n\nMemerintah: /mentionall\n__Anda dapat menggunakan perintah ini dengan teks apa yang ingin Anda sebutkan orang lain.__\n`Contoh: /mentionall Halo Yatim!`\n__Anda dapat memberikan perintah ini sebagai balasan untuk pesan apa pun. Bot akan menandai pengguna ke pesan balasan itu__.\n\n Tuan Gua [Sielzz](https://t.me/arsilaf) on Github"
  await event.reply(helptext,
                    buttons=(
                      [Button.url('📣 Channel', 'https://t.me/sielzzproject'),
                      Button.url('🗣️ Tuan Gua', 'https://t.me/arsilaf')]
                    ),
                    link_preview=False
                   )
  
@client.on(events.NewMessage(pattern="^/mentionall ?(.*)"))
async def mentionall(event):
  if event.is_private:
    return await event.respond("__Perintah ini dapat digunakan dalam grup dan saluran!__")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("__Hanya admin yang boleh mention semua!__")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__Saya tidak bisa menyebut anggota untuk pesan lama! (pesan yang dikirim sebelum saya ditambahkan ke grup)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Give me one argument!__")
  else:
    return await event.respond("__Membalas pesan atau memberi saya beberapa teks untuk menyebutkan orang lain!__")
  
  if mode == "text_on_cmd":
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  if mode == "text_on_reply":
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
print(">> BOT AKTIF YA NGENTOT!!! <<")
client.run_until_disconnected()
