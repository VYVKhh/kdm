from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from modules.downloader import Downloader
from modules.converter import Con
from modules.pro import Pro
from modules.translator import Translator  # استيراد كلاس الترجمة
from modules.song_identifier import SongIdentifier  # استيراد كلاس معرفة الأغنية

BOT_TOKEN = '7376905431:AAGuKezo_TZr7UwJvhNzNSDtu46rnSzfXF8'
API_ID = 23074879
API_HASH = "71a6cabebb752f1f0be92d26efde3d01"

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("قسم تحميل السوشيال 🤖", callback_data='downloader'),
            InlineKeyboardButton("حول ملفاتك 🗂️", callback_data='file_converter'),
            InlineKeyboardButton("استخرج جلستك 💻", callback_data='extract_session'),
            InlineKeyboardButton("ترجمة 🌐", callback_data='translate'),
            InlineKeyboardButton("معرفة الأغنية 🎵", callback_data='identify_song')  # إضافة خيار معرفة الأغنية
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('اختر خيارًا:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'downloader':
        query.edit_message_text(text="أرسل رابط أي موقع 🌚")

    elif query.data == 'file_converter':
        keyboard = [
            [
                InlineKeyboardButton("تحويل صورة إلى PDF 🖼️📄", callback_data='image_to_pdf'),
                InlineKeyboardButton("تحويل فيديو إلى صوت 🎥🔊", callback_data='video_to_audio')
            ],
            [
                InlineKeyboardButton("تحويل فيديو إلى GIF 📹✨", callback_data='video_to_gif'),
                InlineKeyboardButton("إنشاء باركود QR 📊", callback_data='qr_code')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text="اختر خيار التحويل:", reply_markup=reply_markup)

    elif query.data == 'extract_session':
        pro = Pro(API_ID, API_HASH, BOT_TOKEN)
        pro.extract_session(query, context)

    elif query.data == 'translate':
        translator = Translator()
        query.edit_message_text(text="أرسل النص الذي تريد ترجمته")
        context.user_data['translator'] = translator

    elif query.data == 'identify_song':
        query.edit_message_text(text="أرسل مقطع الصوت أو الفيديو الذي تريد معرفة تفاصيله")
        context.user_data['song_identifier'] = SongIdentifier()

def handle_song_identification(update: Update, context: CallbackContext) -> None:
    file = update.message.voice or update.message.audio or update.message.video
    if file:
        file_info = context.bot.get_file(file.file_id)
        downloaded_file = file_info.download()

        song_identifier = context.user_data.get('song_identifier')
        if song_identifier:
            song_info = song_identifier.identify_song(downloaded_file)
            update.message.reply_text(f"معلومات الأغنية: {song_info}")
        else:
            update.message.reply_text("يرجى تحديد خيار معرفة الأغنية من القائمة الرئيسية أولاً.")

def handle_link(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    wait_message = update.message.reply_text("عزيزي المستخدم انتظر قليلاً 🕘")
    downloader = Downloader()
    video_info = downloader.download(url)

    context.bot.delete_message(chat_id=update.message.chat_id, message_id=wait_message.message_id)
    
    if video_info:
        keyboard = [
            [
                InlineKeyboardButton("تحويل إلى ملف صوتي 🎵", callback_data='convert_audio'),
                InlineKeyboardButton("تحويل إلى رسالة صوتية 🎤", callback_data='convert_voice')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_video(chat_id=update.message.chat_id, video=open(video_info['video'], 'rb'), caption=video_info['description'], reply_markup=reply_markup)
        context.user_data['video_info'] = video_info

    else:
        update.message.reply_text("عذرًا، لا يمكنني التحميل من هذا الرابط.")

def handle_conversion(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    video_info = context.user_data.get('video_info')

    if video_info:
        converter = Con()
        if query.data == 'convert_audio':
            audio_path = converter.video_to_audio(video_info['video'])
            context.bot.send_audio(chat_id=query.message.chat_id, audio=open(audio_path, 'rb'))
        elif query.data == 'convert_voice':
            voice_path = converter.video_to_voice(video_info['video'])
            context.bot.send_voice(chat_id=query.message.chat_id, voice=open(voice_path, 'rb'))

def handle_image(update: Update, context: CallbackContext) -> None:
    photo = update.message.photo[-1]
    file = context.bot.get_file(photo.file_id)
    downloaded_file = file.download(custom_path="temp_image.jpg")

    converter = Con()
    pdf_path = converter.image_to_pdf("temp_image.jpg")
    context.bot.send_document(chat_id=update.message.chat_id, document=open(pdf_path, 'rb'))

def handle_video_conversion(update: Update, context: CallbackContext) -> None:
    video = update.message.video
    file = context.bot.get_file(video.file_id)
    downloaded_file = file.download(custom_path="temp_video.mp4")

    query = context.user_data.get('query')
    converter = Con()

    if query == 'convert_audio':
        audio_path = converter.video_to_audio("temp_video.mp4")
        context.bot.send_audio(chat_id=update.message.chat_id, audio=open(audio_path, 'rb'))
    elif query == 'convert_voice':
        voice_path = converter.video_to_voice("temp_video.mp4")
        context.bot.send_voice(chat_id=update.message.chat_id, voice=open(voice_path, 'rb'))

def handle_video_to_gif(update: Update, context: CallbackContext) -> None:
    video = update.message.video
    file = context.bot.get_file(video.file_id)
    downloaded_file = file.download(custom_path="temp_video.mp4")

    converter = Con()
    gif_path = converter.video_to_gif("temp_video.mp4")
    context.bot.send_document(chat_id=update.message.chat_id, document=open(gif_path, 'rb'))

def handle_qr_code(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    converter = Con()
    qr_code_path = converter.generate_qr_code(text)
    context.bot.send_photo(chat_id=update.message.chat_id, photo=open(qr_code_path, 'rb'))

def main() -> None:
    updater = Updater(BOT_TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_translation))
    updater.dispatcher.add_handler(MessageHandler(Filters.voice | Filters.audio | Filters.video, handle_song_identification))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_link))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, handle_image))
    updater.dispatcher.add_handler(MessageHandler(Filters.video, handle_video_conversion))
    updater.dispatcher.add_handler(CallbackQueryHandler(handle_conversion, pattern='^(convert_audio|convert_voice)$'))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()