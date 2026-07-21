import os
from flask import Flask
from threading import Thread
import telebot
import yt_dlp
from telebot import types

# --- ឆែកមើល Server ឱ្យដំណើរការ 24/7 ---
app = Flask('')
@app.route('/')
def home(): return "Fast TikTok & Facebook Bot is running 24/7!"
def run_server(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
def keep_alive():
    t = Thread(target=run_server)
    t.start()

# --- បូខត Telegram ---
TOKEN = '8870524240:AAE1Ih0LhDEDcWXGs1hICNKx-VTojI73iqY'
bot = telebot.TeleBot(TOKEN)

# ដាក់ Link Channel របស់អ្នកនៅទីនេះ
CHANNEL_LINK = "https://t.me/only_study_shadow"
CHANNEL_NAME = "📢 ចូលរួម Channel ដើម្បីទទួលបានវីដេអូថ្មីៗ!"

# --- សារស្វាគមន៍ ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "⚡ **ប្រព័ន្ធទាញយកវីដេអូ TikTok & Facebook ទំនើប និងលឿនបំផុត!**\n\n"
        "🚀 **លឿនរហ័ស ឥតគិតថ្លៃ (Free 100%)**\n"
        "📥 គាំទ្រការទាញយកពី៖ `TikTok` និង `Facebook` ភ្លាមៗ!\n\n"
        "👇 **គ្រាន់តែផ្ញើ Link TikTok ឬ Facebook មកទីនេះភ្លាម Bot នឹងទាញយកជូនភ្លែត!**"
    )
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(CHANNEL_NAME, url=CHANNEL_LINK))
    
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown', reply_markup=markup)

# --- ទទួល Link ពី TikTok ឬ Facebook និង Download ភ្លាមៗ ---
@bot.message_handler(func=lambda message: True)
def get_link(message):
    url = message.text.strip()
    if not url.startswith('http'):
        bot.reply_to(message, "❌ សូមផ្ញើ Link វីដេអូ TikTok ឬ Facebook ឱ្យបានត្រឹមត្រូវ!")
        return

    # ត្រួតពិនិត្យមិនឱ្យទទួលយក Link YouTube
    if 'youtube.com' in url or 'youtu.be' in url:
        bot.reply_to(message, "⚠️ Bot នេះគាំទ្រតែវីដេអូ **TikTok** និង **Facebook** ប៉ុណ្ណោះ!")
        return

    msg = bot.reply_to(message, "⚡ **កំពុងទាញយកយ៉ាងលឿន...** សូមរង់ចាំបន្តិច! ⏳", parse_mode='Markdown')

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_video.%(ext)s',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            title = info.get('title', 'Downloaded Video')

        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="🚀 **ទាញយកជោគជ័យ! កំពុងផ្ញើជូន...**", parse_mode='Markdown')

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔥 ចូលរួម Channel ផ្លូវការ", url=CHANNEL_LINK))

        with open(filename, 'rb') as video_file:
            bot.send_video(message.chat.id, video=video_file, caption=f"🎬 **{title}**\n\n✨ _ទាញយកដោយជោគជ័យ!_", parse_mode='Markdown', reply_markup=markup)

        if os.path.exists(filename):
            os.remove(filename)
            
        bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)

    except Exception as e:
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=f"❌ មានបញ្ហាក្នុងការទាញយក (លីងប្រហែលជាត្រូវបានដាក់កម្រិត ឬឯកជន)៖ {str(e)}")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
