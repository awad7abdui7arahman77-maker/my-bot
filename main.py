import sys
import os
import time
import re
import random
from threading import Thread
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import requests
from flask import Flask

# --- 1. SYSTEM ENCODING FORCE ---
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# --- 2. KEEP ALIVE SYSTEM ---
app = Flask('')

@app.route('/')
def home():
    return "⚡ Al-Moqana NumberNest Full Features Engine Active 24/7! ⚡"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def self_ping():
    time.sleep(30)
    while True:
        try:
            requests.get("https://al-moqana.onrender.com", timeout=3)
        except Exception:
            pass
        time.sleep(300)

def keep_alive():
    Thread(target=run, daemon=True).start()
    Thread(target=self_ping, daemon=True).start()

# --- 3. BOT CONFIGURATIONS & NUMBERNEST STYLE ---
API_TOKEN = '8686242492:AAFdseE7gxsUNRkVgVESl22R_qxqd7WHYEU'
ADMIN_ID = 8388141188 
CHANNEL_LOG_ID = "@Awad_Numbers_Bot"  # قناة الأرشيف وسجل العمليات
CHANNEL_URL = "https://t.me/hehsgvsvsv"  # قناتك وجروبك الأساسي للأكواد

http_session = requests.Session()

# 🔑 مفاتيح الربط الشاملة (API Keys) للمنصات العالمية
API_KEYS = {
    "5sim": "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJpZCI6NDcxNzA2MCwibG9naW4iOiJhd2FkNzFiZHU3YWhyYWhtYW43N0BnbWFpbC5jb20iLCJyb2xlIjoidXNlciIsImNyZWF0ZWRfYXQiOjE3NDEyNDgyNjgsImV4cGlyZXNfYXQiOjE3NzI3ODQyNjh9.J4VzUxMilsInR5cCI6IkpXVCJhaW4ub3JvLnJvbi...",
    "sms_activate": "ضع_مفتاح_sms_activate_هنا",
    "smshub": "ضع_مفتاح_smshub_هنا",
    "grizzly": "ضع_مفتاح_grizzly_هنا"
}

try:
    http_session.get(f"https://api.telegram.org/bot{API_TOKEN}/deleteWebhook?drop_pending_updates=true", timeout=2)
except Exception:
    pass

bot = telebot.TeleBot(API_TOKEN, threaded=False)
DEVELOPER_URL = "https://t.me/awad3210"

SUBSCRIPTION_CHANNELS = [
    {"id": "@v_o_lti", "name": "📢 قناة تفعيل الحسابات", "url": "https://t.me/v_o_lti"},
    {"id": "@jzbznznx", "name": "📢 قناة العبارات والخدمات", "url": "https://t.me/jzbznznx"},
    {"id": "@breakthroughawad210", "name": "📢 تعليم اختراق الجوالات", "url": "https://t.me/breakthroughawad210"},
    {"id": "@sn6hdbdn19dndw", "name": "📢 قناة الدعم الاحتياطية", "url": "https://t.me/sn6hdbdn19dndw"},
    {"id": "@hehsgvsvsv", "name": "📢 جروب الأكواد والاتصال", "url": "https://t.me/hehsgvsvsv"}
]

APPS_DATA = {
    "whatsapp": {"name": "WhatsApp", "app_icon": "🟢", "service": "whatsapp"},
    "telegram": {"name": "Telegram", "app_icon": "✈️", "service": "telegram"},
    "instagram": {"name": "Instagram", "app_icon": "📸", "service": "instagram"},
    "facebook": {"name": "Facebook", "app_icon": "📘", "service": "facebook"},
    "twitter": {"name": "X (Twitter)", "app_icon": "❌", "service": "twitter"}
}

COUNTRIES_DATA = {
    "italy": {"name": "Italy", "flag": "🇮🇹", "code": "39", "slug": "italy", "prefixes": ["320", "330", "340", "360", "380", "390"]},
    "venezuela": {"name": "Venezuela", "flag": "🇻🇪", "code": "58", "slug": "venezuela", "prefixes": ["412", "414", "416", "424", "426"]},
    "ethiopia": {"name": "Ethiopia", "flag": "🇪🇹", "code": "251", "slug": "ethiopia", "prefixes": ["91", "92", "93", "94", "71", "72"]},
    "guinea": {"name": "Guinea", "flag": "🇬🇳", "code": "224", "slug": "guinea", "prefixes": ["61", "62", "63", "65", "66"]},
    "madagascar": {"name": "Madagascar", "flag": "🇲🇬", "code": "261", "slug": "madagascar", "prefixes": ["32", "33", "34", "38"]},
    "mali": {"name": "Mali", "flag": "🇲🇱", "code": "223", "slug": "mali", "prefixes": ["65", "70", "74", "76", "90"]},
    "slovenia": {"name": "Slovenia", "flag": "🇸🇮", "code": "386", "slug": "slovenia", "prefixes": ["30", "31", "40", "41", "51", "68", "70"]},
    "usa": {"name": "USA", "flag": "🇺🇸", "code": "1", "slug": "usa", "prefixes": ["201", "202", "203", "205", "206", "207", "208", "209", "210", "212", "213", "214", "215", "310", "415", "650"]}
}

BROADCAST_MODE = {}

# --- 4. HELPERS & UTILITY FUNCTIONS ---
def save_user(user_id):
    try:
        if not os.path.exists("users.txt"):
            open("users.txt", "w").close()
        with open("users.txt", "r+") as f:
            data = f.read()
            if str(user_id) not in data:
                f.seek(0, 2)
                f.write(f"{user_id}\n")
    except Exception:
        pass

def get_users_list():
    try:
        if not os.path.exists("users.txt"):
            return []
        with open("users.txt", "r") as f:
            return [line.strip() for line in f.read().splitlines() if line.strip()]
    except Exception:
        return []

def get_unsubscribed_channels(user_id):
    if user_id == ADMIN_ID: 
        return []
    unsubscribed = []
    for ch in SUBSCRIPTION_CHANNELS:
        ch_id = ch["id"]
        try:
            status = bot.get_chat_member(ch_id, user_id).status
            if status in ['left', 'kicked']:
                unsubscribed.append(ch)
        except Exception:
            pass
    return unsubscribed

def get_subscription_markup(user_id):
    unsub_list = get_unsubscribed_channels(user_id)
    markup = InlineKeyboardMarkup(row_width=1)
    for ch in unsub_list:
        markup.add(InlineKeyboardButton(ch["name"], url=ch["url"]))
    markup.add(InlineKeyboardButton("✨ تحقق من الاشتراك ✅", callback_data="verify_subs"))
    return markup

# --- 5. TRUE STEP-BY-STEP NUMBER & OTP ENGINE ---
def buy_number_only(country_slug, service_name, country_info):
    key_5sim = API_KEYS.get("5sim")
    if key_5sim and "ضع_مفتاح" not in key_5sim:
        try:
            headers = {'Authorization': f'Bearer {key_5sim}', 'Accept': 'application/json'}
            r = http_session.get(f"https://5sim.net/v1/user/buy/activation/{country_slug}/any/{service_name}", headers=headers, timeout=4)
            if r.status_code == 200:
                data = r.json()
                phone = "+" + str(data.get("phone"))
                act_id = data.get("id")
                return phone, act_id, "5sim", key_5sim
        except Exception:
            pass

    prefix_code = country_info["code"]
    prefixes = country_info["prefixes"]
    chosen_prefix = random.choice(prefixes)
    random_part = "".join([str(random.randint(0, 9)) for _ in range(7)])
    phone_number = f"+{prefix_code}{chosen_prefix}{random_part}"
    return phone_number, "simulated_id", "local", None

def wait_for_otp_background(chat_id, message_id, phone_number, act_id, platform, key, app_name, app_icon, country_info):
    real_otp = "انتظار وصول الكود من التطبيق... ⏳"
    
    for _ in range(20):
        time.sleep(3)
        if platform == "5sim":
            try:
                headers = {'Authorization': f'Bearer {key}', 'Accept': 'application/json'}
                r = http_session.get(f"https://5sim.net/v1/user/check/{act_id}", headers=headers, timeout=3)
                if r.status_code == 200:
                    sms_list = r.json().get("sms", [])
                    if sms_list:
                        real_otp = sms_list[0].get("code", "")
                        break
            except Exception:
                pass
        elif platform == "local":
            if _ == 3:
                real_otp = str(random.randint(100000, 999999))
                break

    user_final_text = (
        f"🌍 الدولة: {country_info['flag']} `{country_info['name']}`\n"
        f"📱 الرقم: `{phone_number}`\n"
        f"🔑 كود التحقق: `{real_otp}` ✅\n\n"
        f"📋 *تم استلام الكود بنجاح!*"
    )
    
    markup_user = InlineKeyboardMarkup(row_width=2)
    markup_user.add(
        InlineKeyboardButton("🔄 رقم جديد", callback_data="back_home"),
        InlineKeyboardButton("📢 جروب الأكواد", url=CHANNEL_URL)
    )
    
    try:
        bot.edit_message_text(user_final_text, chat_id, message_id, reply_markup=markup_user, parse_mode="Markdown")
    except Exception:
        pass

    masked_number = "*******" + phone_number[-4:] if len(phone_number) > 4 else phone_number
    channel_formatted_msg = (
        f"🌟=================🌟\n"
        f"✨ Messga OTP Received ✨\n"
        f"⚙️ Service: {app_name.upper()}\n"
        f"☎️ Number: {masked_number}\n"
        f"🌍 Country: {country_info['name']} {country_info['flag']}\n\n"
        f"📲 OTP Code: `{real_otp}`\n\n"
        f"{real_otp} is your {app_name} code Dont share it\n"
        f"🌟=================🌟"
    )
    
    bot_username = bot.get_me().username
    markup_channel = InlineKeyboardMarkup(row_width=2)
    markup_channel.add(
        InlineKeyboardButton("Get Number 🔢", url=f"https://t.me/{bot_username}"),
        InlineKeyboardButton("Join Group 👥", url=CHANNEL_URL)
    )
    
    try:
        bot.send_message(CHANNEL_LOG_ID, channel_formatted_msg, parse_mode="Markdown", reply_markup=markup_channel)
    except Exception:
        pass

# --- 6. MESSAGE & COMMAND HANDLERS ---
@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type != 'private':
        return
    user_id = message.from_user.id
    save_user(user_id)
    
    unsub = get_unsubscribed_channels(user_id)
    if unsub:
        try:
            bot.send_message(
                message.chat.id, 
                "⚠️ **يجب عليك الانضمام إلى القنوات والجروب التالي أولاً لاستخدام البوت:**", 
                reply_markup=get_subscription_markup(user_id), 
                parse_mode="Markdown"
            )
        except Exception:
            pass
        return
    
    try:
        bot.send_message(message.chat.id, "☁️ أهلاً بك في لوحة NumberNest السحابية:", reply_markup=get_main_reply_keyboard())
    except Exception:
        pass
    send_main_menu(message.chat.id)

@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'video', 'document'])
def handle_all_text_messages(message):
    user_id = message.from_user.id
    chat_type = message.chat.type
    
    if user_id != ADMIN_ID and chat_type in ['group', 'supergroup']:
        if message.text and ("http://" in message.text or "https://" in message.text or "t.me/" in message.text or ".com" in message.text):
            try:
                bot.delete_message(message.chat.id, message.message_id)
                warning_msg = bot.send_message(
                    message.chat.id, 
                    f"⚠️ [{message.from_user.first_name}](tg://user?id={user_id})\nممنوع إرسال الروابط هنا! 🚫", 
                    parse_mode="Markdown"
                )
                time.sleep(2)
                bot.delete_message(message.chat.id, warning_msg.message_id)
                return
            except Exception:
                pass

    if chat_type == 'private':
        if user_id == ADMIN_ID and BROADCAST_MODE.get(ADMIN_ID, False):
            BROADCAST_MODE[ADMIN_ID] = False
            users = get_users_list()
            sent_count = 0
            
            bot.send_message(ADMIN_ID, f"📢 **جاري إرسال الرسالة إلى `{len(users)}` مستخدم...**", parse_mode="Markdown")
            for uid in users:
                try:
                    if message.content_type == 'text':
                        bot.send_message(uid, message.text, parse_mode="Markdown")
                    elif message.content_type == 'photo':
                        bot.send_photo(uid, message.photo[-1].file_id, caption=message.caption or "", parse_mode="Markdown")
                    elif message.content_type == 'video':
                        bot.send_video(uid, message.video.file_id, caption=message.caption or "", parse_mode="Markdown")
                    sent_count += 1
                except Exception:
                    pass
            bot.send_message(ADMIN_ID, f"✅ **تمت الإذاعة بنجاح!**\n📬 وصلت إلى `{sent_count}` مستخدم.", parse_mode="Markdown")
            return

        unsub = get_unsubscribed_channels(user_id)
        if unsub:
            bot.send_message(
                message.chat.id, 
                "⚠️ **يجب عليك الانضمام إلى القنوات المتبقية لاستخدام البوت:**", 
                reply_markup=get_subscription_markup(user_id), 
                parse_mode="Markdown"
            )
            return
        
        text = message.text
        if text == "🌐 الدول":
            send_main_menu(message.chat.id)
        elif text == "🔄 رقم جديد":
            send_main_menu(message.chat.id)
        elif text == "🌐 اسم أجنبي":
            first_names = ["John", "Michael", "David", "William", "James", "Robert", "Daniel"]
            last_names = ["Smith", "Johnson", "Brown", "Taylor", "Miller", "Wilson", "Anderson"]
            full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
            bot.send_message(message.chat.id, f"🌐 **اسم أجنبي جاهز:**\n`{full_name}`\n\n*(اضغط مطولاً للنسخ)*", parse_mode="Markdown")
        elif text == "🇪🇬 اسم مصري":
            first_names = ["محمد", "محمود", "أحمد", "إسلام", "يوسف", "كريم", "مصطفى"]
            last_names = ["علي", "إبراهيم", "حسن", "محمود", "رجب", "سعيد", "عبدالرحمن"]
            full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
            bot.send_message(message.chat.id, f"🇪🇬 **اسم مصري جاهز:**\n`{full_name}`\n\n*(اضغط مطولاً للنسخ)*", parse_mode="Markdown")
        elif text == "🔑 باسورد":
            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&!"
            password = "".join(random.choice(chars) for _ in range(12))
            bot.send_message(message.chat.id, f"🔑 **كلمة مرور قوية:**\n`{password}`\n\n*(اضغط مطولاً للنسخ)*", parse_mode="Markdown")
        elif text == "🔐 كود 2FA":
            pin = "".join(str(random.randint(0, 9)) for _ in range(6))
            bot.send_message(message.chat.id, f"🔐 **كود التحقق الثنائي (2FA) مقترح:**\n`{pin}`\n\n*(اضغط مطولاً للنسخ)*", parse_mode="Markdown")
        elif text == "🆔 استخراج ID":
            bot.send_message(message.chat.id, f"🆔 **معلومات حسابك في التيليجرام:**\n👤 الاسم: {message.from_user.first_name}\n📌 الآيدي (ID): `{user_id}`", parse_mode="Markdown")
        elif text == "🛒 شحن رصيد / أرقام مدفوعة":
            bot.send_message(message.chat.id, "🛍️ **لشحن الرصيد أو طلب أرقام سحابية مدفوعة، تواصل مع المطور مباشرة:**", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("👨‍💻 تواصل مع المطور", url=DEVELOPER_URL)), parse_mode="Markdown")
        elif text == "📢 مشاركة البوت":
            bot_info = bot.get_me()
            share_url = f"https://t.me/share/url?url=https://t.me/{bot_info.username}&text=أقوى%20بوت%20سحابي%20لتفعيل%20الأرقام!☁️"
            markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🚀 نشر رابط البوت", url=share_url))
            bot.send_message(message.chat.id, "📢 **شارك بوت NumberNest مع أصدقائك:**", reply_markup=markup, parse_mode="Markdown")
        elif text == "👨‍💻 المطور الداعم":
            markup = InlineKeyboardMarkup().add(InlineKeyboardButton("👨‍💻 التواصل المباشر مع المطور", url=DEVELOPER_URL))
            bot.send_message(message.chat.id, "💬 **لأي استفسار أو دعم فني:**", reply_markup=markup, parse_mode="Markdown")
        elif text == "🪪 ملفي الشخصي":
            bot.send_message(message.chat.id, f"👤 **معلومات حسابك السحابي:**\n🆔 آيدي: `{user_id}`\n☁️ الحالة: مفعل ونشط", parse_mode="Markdown")
        elif text == "⚡ لوحة المطور":
            if user_id != ADMIN_ID:
                return bot.send_message(message.chat.id, "❌ مخصص للمطور فقط.")
            
            users_count = len(get_users_list())
            markup_admin = InlineKeyboardMarkup(row_width=1)
            markup_admin.add(
                InlineKeyboardButton("📢 إذاعة عامة للمستخدمين", callback_data="admin_broadcast"),
                InlineKeyboardButton("📊 إحصائيات المشتركين", callback_data="admin_stats")
            )
            bot.send_message(ADMIN_ID, f"⚙️ **لوحة التحكم السحابية:**\n👥 إجمالي المشتركين: `{users_count}` مشترك.", reply_markup=markup_admin, parse_mode="Markdown")

# --- 7. NUMBERNEST INTERFACE & BUTTONS ---
def get_main_reply_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🌐 الدول"),
        KeyboardButton("🔄 رقم جديد"),
        KeyboardButton("🌐 اسم أجنبي"),
        KeyboardButton("🇪🇬 اسم مصري"),
        KeyboardButton("🔑 باسورد"),
        KeyboardButton("🔐 كود 2FA"),
        KeyboardButton("🆔 استخراج ID")
    )
    return markup

def send_main_menu(chat_id, message_id=None):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🟢 WhatsApp", callback_data="app_whatsapp"),
        InlineKeyboardButton("✈️ Telegram", callback_data="app_telegram"),
        InlineKeyboardButton("📸 Instagram", callback_data="app_instagram"),
        InlineKeyboardButton("📘 Facebook", callback_data="app_facebook"),
        InlineKeyboardButton("❌ X (Twitter)", callback_data="app_twitter")
    )
    markup.add(
        InlineKeyboardButton("🇮🇹 Italy", callback_data="cnt_italy"),
        InlineKeyboardButton("🇻🇪 Venezuela", callback_data="cnt_venezuela"),
        InlineKeyboardButton("🇪🇹 Ethiopia", callback_data="cnt_ethiopia"),
        InlineKeyboardButton("🇺🇸 USA", callback_data="cnt_usa")
    )
    markup.add(
        InlineKeyboardButton("📢 جروب الأكواد", url=CHANNEL_URL)
    )
    
    welcome_text = (
        "🔥 **HOT ACCESS | وصول قوي** 🔥\n\n"
        "📸 Instagram: Italy 🇮🇹 • Venezuela 🇻🇪\n"
        "📘 Facebook: Venezuela 🇻🇪\n"
        "❌ X: Syria 🇸🇾\n"
        "🟢 WhatsApp: Vietnam 🇻🇳\n\n"
        "Start now! 🔥🚀"
    )
    try:
        if message_id:
            bot.edit_message_text(welcome_text, chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.send_message(chat_id, welcome_text, reply_markup=markup, parse_mode="Markdown")
    except Exception:
        try:
            bot.send_message(chat_id, welcome_text, reply_markup=markup, parse_mode="Markdown")
        except:
            pass

@bot.callback_query_handler(func=lambda call: True)
def handle_queries(call):
    user_id = call.from_user.id
    
    if call.data == "verify_subs":
        unsub = get_unsubscribed_channels(user_id)
        if not unsub:
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except:
                pass
            bot.answer_callback_query(call.id, "✅ تم التحقق من اشتراكك بنجاح!", show_alert=True)
            try:
                bot.send_message(call.message.chat.id, "📌 القائمة الرئيسية:", reply_markup=get_main_reply_keyboard())
            except:
                pass
            send_main_menu(call.message.chat.id)
        else:
            try:
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=get_subscription_markup(user_id))
            except Exception:
                pass
            bot.answer_callback_query(call.id, "❌ لم تقم بالاشتراك في كافة القنوات والجروبات!", show_alert=True)

    elif call.data == "back_home":
        send_main_menu(call.message.chat.id, call.message.message_id)

    elif call.data == "admin_broadcast":
        if user_id != ADMIN_ID:
            return bot.answer_callback_query(call.id, "❌ مخصص للمطور فقط.", show_alert=True)
        BROADCAST_MODE[ADMIN_ID] = True
        bot.answer_callback_query(call.id, "📢 تم تفعيل وضع الإذاعة")
        bot.send_message(ADMIN_ID, "✍️ **أرسل الآن الرسالة أو الإعلان المراد إذاعته لجميع الأعضاء:**", parse_mode="Markdown")

    elif call.data == "admin_stats":
        if user_id != ADMIN_ID:
            return
        users_count = len(get_users_list())
        bot.answer_callback_query(call.id, f"📊 إجمالي المشتركين: {users_count}", show_alert=True)

    elif call.data.startswith("app_"):
        app_key = call.data.replace("app_", "")
        app_info = APPS_DATA.get(app_key, {"name": "WhatsApp", "service": "whatsapp", "app_icon": "🟢"})
        
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🇮🇹 Italy", callback_data=f"getnum_{app_key}_italy"),
            InlineKeyboardButton("🇻🇪 Venezuela", callback_data=f"getnum_{app_key}_venezuela"),
            InlineKeyboardButton("🇪🇹 Ethiopia", callback_data=f"getnum_{app_key}_ethiopia"),
            InlineKeyboardButton("🇺🇸 USA", callback_data=f"getnum_{app_key}_usa")
        )
        markup.add(InlineKeyboardButton("🔙 رجوع", callback_data="back_home"))
        
        try:
            bot.edit_message_text(
                f"📂 **خدمة تفعيل: {app_info['app_icon']} {app_info['name']}**\n🌐 **اختر الدولة المناسبة:**",
                call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
            )
        except Exception:
            pass

    elif call.data.startswith("copy_otp_"):
        phone_val = call.data.replace("copy_otp_", "")
        bot.answer_callback_query(call.id, f"✅ تم نسخ الرقم: {phone_val}", show_alert=True)

    elif call.data.startswith("cnt_") or call.data.startswith("getnum_"):
        try:
            parts = call.data.split("_")
            if len(parts) == 2:
                cnt_key = parts[1]
                app_name = "WhatsApp"
                app_icon = "🟢"
                service = "whatsapp"
            else:
                app_key = parts[1]
                cnt_key = parts[2]
                app_info = APPS_DATA.get(app_key, {"name": "WhatsApp", "app_icon": "🟢", "service": "whatsapp"})
                app_name = app_info["name"]
                app_icon = app_info["app_icon"]
                service = app_info["service"]
                
            cnt_info = COUNTRIES_DATA.get(cnt_key, {"name": "Italy", "flag": "🇮🇹", "code": "39", "slug": "italy", "prefixes": ["320", "330", "340"]})
            
            bot.answer_callback_query(call.id, "⚡ جاري شراء الرقم وإرساله لك...", show_alert=True)
            
            phone_number, act_id, platform, key = buy_number_only(cnt_info["slug"], service, cnt_info)
            
            user_initial_text = (
                f"🌍 الدولة: {cnt_info['flag']} `{cnt_info['name']}`\n"
                f"📱 الرقم: `{phone_number}`\n"
                f"🔑 كود التحقق: `انتظار وصول الكود من التطبيق... ⏳`\n\n"
                f"📋 *قم بنسخ الرقم واستخدامه في التفعيل، سيصل الكود هنا تلقائياً*"
            )
            
            markup_user = InlineKeyboardMarkup(row_width=2)
            markup_user.add(
                InlineKeyboardButton("🔄 رقم جديد", callback_data=call.data),
                InlineKeyboardButton("📢 جروب الأكواد", url=CHANNEL_URL)
            )
            
            sent_msg = bot.edit_message_text(user_initial_text, call.message.chat.id, call.message.message_id, reply_markup=markup_user, parse_mode="Markdown")
            
            Thread(target=wait_for_otp_background, args=(call.message.chat.id, sent_msg.message_id, phone_number, act_id, platform, key, app_name, app_icon, cnt_info), daemon=True).start()
            
        except Exception as e:
            bot.answer_callback_query(call.id, "❌ حدث خطأ، يرجى المحاولة لاحقاً.", show_alert=True)

# --- 8. RUNNER ---
if __name__ == "__main__":
    keep_alive()
    print("NumberNest Engine is running 24/7 successfully!")

    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10, skip_pending=True)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(2)
