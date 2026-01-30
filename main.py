import os
import yt_dlp
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from flask import Flask
from threading import Thread

# سيرفر وهمي لإبقاء الخدمة تعمل
app_web = Flask('')
@app_web.route('/')
def home(): return "Bot is Online!"
def run_web(): app_web.run(host='0.0.0.0', port=7860)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith("http"): return
    msg = await update.message.reply_text("⏳ جاري التحميل... انتظر قليلاً")
    try:
        # إعدادات التحميل
        ydl_opts = {'format': 'best', 'outtmpl': 'video.mp4'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        with open('video.mp4', 'rb') as v:
            await update.message.reply_video(video=v, caption="✅ تم التحميل")
        
        os.remove('video.mp4')
        await msg.delete()
    except Exception as e:
        await msg.edit_text(f"❌ حدث خطأ: {str(e)}")

if __name__ == '__main__':
    # تشغيل السيرفر الوهمي
    Thread(target=run_web).start()
    
    # التوكن الجديد الخاص بك
    TOKEN = "8351715808:AAHYmi3NxfLYKI6m5kAdh_gO9eWu-tOQ5mQ"
    
    # إعداد البوت مع زيادة مهلة الاتصال (Timeout) لحل مشكلة NetworkError
    application = Application.builder().token(TOKEN).connect_timeout(30).read_timeout(30).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("البوت يحاول الاتصال الآن... ✅")
    application.run_polling(drop_pending_updates=True)
    
