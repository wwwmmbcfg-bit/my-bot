import os
import yt_dlp
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# دالة التحميل الأساسية
def download_media(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'file.mp4',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "http" not in url: return

    # حظر روابط يوتيوب مؤقتاً لتجنب الحظر
    if "youtube.com" in url or "youtu.be" in url:
        await update.message.reply_text("⚠️ التحميل من يوتيوب متوقف حالياً.. جرب تيك توك أو إنستغرام.")
        return

    # 1. إرسال رسالة "يرجى الانتظار" فور استلام الرابط
    status_msg = await update.message.reply_text("🚶 استلمت الرابط، يرجى الانتظار قليلاً جاري التحميل...")

    try:
        path = download_media(url)
        with open(path, 'rb') as video:
            # 2. إرسال الفيديو مع كابشن "مشاهدة ممتعة 🤷"
            await update.message.reply_video(video=video, caption="مشاهدة ممتعة 🌚")
        
        os.remove(path)
        # حذف رسالة الانتظار بعد نجاح التحميل ليبقى الشات نظيفاً
        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text("❌ عذراً، حدث خطأ أثناء التحميل. تأكد من أن الرابط عام وليس خاص.")

if __name__ == '__main__':
    # ضع التوكن الخاص بك هنا
    TOKEN = "8351715808:AAHJLiiKypC4b8jWEs2QwQ6VDqtOJEfmaKk" 
    
    print("البوت يعمل الآن بنظام الرد الذكي... 🚀")
    
    # بناء التطبيق مع ميزة drop_pending_updates لحل مشكلة التكرار
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # تشغيل البوت مع مسح أي رسائل قديمة معلقة
    app.run_polling(drop_pending_updates=True)
