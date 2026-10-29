import os
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from moviepy.editor import AudioFileClip, ImageClip
from PIL import Image

TOKEN = os.getenv("BOT_TOKEN")

# 1. Background image download (Space)
if not os.path.exists("bg.jpg"):
    print("Downloading background...")
    try:
        # Beautiful space image
        url = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1080&q=80"
        r = requests.get(url, timeout=15)
        open("bg.jpg", "wb").write(r.content)
    except:
        # agar net fail to black background
        Image.new('RGB', (1080, 1920), (5, 10, 30)).save("bg.jpg")

async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Voice mil gaya! Space video bana raha hu... 30 sec lagega")

    try:
        # Voice download
        file = await context.bot.get_file(update.message.voice.file_id)
        await file.download_to_drive("voice.ogg")

        # OGG to MP3
        audio = AudioFileClip("voice.ogg")
        audio.write_audiofile("voice.mp3", logger=None)
        audio = AudioFileClip("voice.mp3")
        
        # Image ko video banao - jitni audio utna video
        bg_clip = ImageClip("bg.jpg", duration=audio.duration)
        bg_clip = bg_clip.set_audio(audio)
        bg_clip = bg_clip.resize(height=1920)
        # Center crop to 1080x1920
        w, h = bg_clip.size
        bg_clip = bg_clip.crop(x_center=w/2, y_center=h/2, width=1080, height=1920)
        
        bg_clip.write_videofile("final.mp4", fps=24, codec="libx264", audio_codec="aac", logger=None)

        await update.message.reply_text("✅ Ban gaya! Bhej raha hu...")
        await update.message.reply_video(video=open("final.mp4", "rb"), caption="🚀 Your Space Voice Video Ready!")

    except Exception as e:
        print(e)
        await update.message.reply_text(f"Error aaya: {e}")

# Bot start
app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.VOICE, voice_handler))
print("Bot Started...")
app.run_polling()
