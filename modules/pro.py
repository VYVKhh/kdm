from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeExpired
from pyrogram.errors.exceptions.bad_request_400 import PasswordHashInvalid, PhoneCodeInvalid
from pyrogram.errors.exceptions.not_acceptable_406 import PhoneNumberInvalid
from pyromod import listen

class Pro:
    def __init__(self, api_id, api_hash, token):
        self.api_id = api_id
        self.api_hash = api_hash
        self.token = token
        self.app = Client("Session", api_id=self.api_id, api_hash=self.api_hash, bot_token=self.token, in_memory=True)

    async def extract_session(self, query, context):
        app = self.app

        await app.start()

        c = Client("Pyrogram", self.api_id, self.api_hash, device_model="Paddington3", in_memory=True)
        await c.connect()
        
        chat_id = query.message.chat_id
        user_mention = query.from_user.mention
        
        msg = await context.bot.send_message(chat_id, f"يا {user_mention} ارسل رقمك الان \n مثال : +20112801111")

        try:
            msg = await context.bot.listen(chat_id, filters=filters.text)
            Number = msg.text
            
            send = await c.send_code(Number)
            
            SendCode = send.phone_code_hash
            code = await context.bot.send_message(chat_id, f"يا {user_mention} ارسل الان كود التحقق \n مثال : `1 2 3 4 5 6`")
            code = await context.bot.listen(chat_id, filters=filters.text)
            RecepionCode = code.text

            try:
                await c.sign_in(Number, SendCode, RecepionCode)
            except SessionPasswordNeeded:
                Password = await context.bot.send_message(chat_id, f"يا {user_mention} ارسل الان كود التحقق بخطوتين")
                Password = await context.bot.listen(chat_id, filters=filters.text)
                PasswordAss = Password.text
                await c.check_password(password=PasswordAss)

            await c.sign_in(Number, SendCode, RecepionCode)
        except PhoneNumberInvalid:
            return await context.bot.send_message(chat_id, "الرقم الذي ارسلته خاطئ", quote=True)
        except (PhoneCodeInvalid, PhoneCodeExpired):
            return await context.bot.send_message(chat_id, "الكود خطأ", quote=True)
        except PasswordHashInvalid:
            return await context.bot.send_message(chat_id, "الباسورد خطأ", quote=True)
        except Exception as e:
            return await context.bot.send_message(chat_id, "حدث خطأ حاول مرة أخرى", quote=True)

        a = await context.bot.send_message(chat_id, "انتظر قليلا", quote=True)
        
        get = await c.get_me()
        text = f"||**معلومات عنك**|| :\n\n"
        text += f"**اسمك الاول**: {get.first_name}\n"
        text += f"**ايديك**: {get.id}\n"
        text += f"**رقمك**: {Number}\n"
        text += f"\n\n شاهد الرسائل المحفوظة [{get.first_name}](tg://openmessage?user_id={get.id})\n"
        text += "للاستخراج مرة أخرى اضغط /start"

        Session = await c.export_session_string()
        await a.delete()

        await c.send_message("me", text=f"الجلسة الخاصة بك : \n\n||`{Session}`||\n\nلا تشارك هذا الكود مع احد \n معلومات عن المطور : @N0040")

        await c.disconnect()
        
        await context.bot.send_message(chat_id, text)
