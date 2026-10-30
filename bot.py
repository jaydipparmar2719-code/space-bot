import os
import random
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from PIL import Image, ImageDraw, ImageFont
#from moviepy.editor import ImageClip

BOT_TOKEN = os.getenv("BOT_TOKEN")

def create_space_video(text, output_path="space_video.mp4"):
    W, H = 720, 1280
    img = Image.new('RGB', (W, H), (5, 5, 20))
    draw = ImageDraw.Draw(img)
    for _ in range(300):
        x = random.randint(0, W)
        y = random.randint(0, H)
        r = random.randint(1, 3)
        draw.ellipse([x, y, x+r, y+r], fill=(255,255,255))
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 50)
        small_font = ImageFont.truetype("DejaVuSans.ttf", 36)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    draw.text((W//2, 640), "YOUR VOICE IN SPACE", font=font, fill=(255,255,255), anchor="mm")
    draw.text((W//2, 740), text[:40], font=small_font, fill=(200,200,200), anchor="mm")
    img.save("bg.jpg")
    clip = ImageClip("bg.jpg", duration=6)
    clip.write_videofile(output_path, fps=24, codec='libx264', audio=False, logger=None)
    return output_path

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Voice mili! Video bana raha hu...")
    try:
        voice_file = await update.message.voice.get_file()
        await voice_file.download_to_drive("voice.ogg")
        user_name = update.effective_user.first_name or "Explorer"
        video_path = create_space_video(f"{user_name}")
        await update.message.reply_video(video=open(video_path, 'rb'), caption=f"{user_name}, teri awaz space me hai!")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Mujhe Voice Message bhej, mai Space Video bana dunga!")

def main():
    print("Bot Started...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
