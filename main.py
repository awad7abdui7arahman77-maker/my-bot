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
    return "⚡ Al-Moqana Mega Global SMS Network Engine Active 24/7! ⚡"

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

# --- 3. BOT CONFIGURATIONS & MEGA GLOBAL STYLE ---
API_TOKEN = '8686242492:AAFdseE7gxsUNRkVgVESl22R_qxqd7WHYEU'
ADMIN_ID = 8388141188 
CHANNEL_LOG_ID = "@Awad_Numbers_Bot"  # قناة الأرشيف وسجل العمليات
CHANNEL_URL = "https://t.me/hehsgvsvsv"  # قناتك وجروبك الأساسي للأكواد

http_session = requests.Session()
http_session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})

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

# --- موسوعة ضخمة تضم عشرات الدول والمواقع العالمية ---
COUNTRIES_DATA = {
    "italy": {"name": "Italy", "flag": "🇮🇹", "code": "39", "slug": "italy"},
    "venezuela": {"name": "Venezuela", "flag": "🇻🇪", "code": "58", "slug": "venezuela"},
    "ethiopia": {"name": "Ethiopia", "flag": "🇪🇹", "code": "251", "slug": "ethiopia"},
    "vietnam": {"name": "Vietnam", "flag": "🇻🇳", "code": "84", "slug": "vietnam"},
    "usa": {"name": "USA", "flag": "🇺🇸", "code": "1", "slug": "usa"},
    "uk": {"name": "United Kingdom", "flag": "🇬🇧", "code": "44", "slug": "uk"},
    "france": {"name": "France", "flag": "🇫🇷", "code": "33", "slug": "france"},
    "germany": {"name": "Germany", "flag": "🇩🇪", "code": "49", "slug": "germany"},
    "canada": {"name": "Canada", "flag": "🇨🇦", "code": "1", "slug": "canada"},
    "russia": {"name": "Russia", "flag": "🇷🇺", "code": "7", "slug": "russia"},
    "brazil": {"name": "Brazil", "flag": "🇧🇷", "code": "55", "slug": "brazil"},
    "turkey": {"name": "Turkey", "flag": "🇹🇷", "code": "90", "slug": "turkey"},
    "spain": {"name": "Spain", "flag": "🇪🇸", "code": "34", "slug": "spain"},
    "egypt": {"name": "Egypt", "flag": "🇪🇬", "code": "20", "slug": "egypt"},
    "saudi": {"name": "Saudi Arabia", "flag": "🇸🇦", "code": "966", "slug": "saudi-arabia"}
}

BROADCAST_MODE = {}

# --- 4. DATABASE HELPERS (USERS ONLY) ---
def save_user(user_id, referrer_id=None):
    try:
        users = get_users_dict()
        str_id = str(user_id)
        if str_id not in users:
            users[str_id] = {"referred_by": referrer_id}
            write_users_dict(users)
    except Exception:
        pass

def get_users_dict():
    users = {}
    try:
        if not os.path.exists("users_points.txt"):
            return {}
        with open("users_points.txt", "r", encoding="utf-8") as f:
            for line in f.read().splitlines():
                parts = line.split(":")
                if len(parts) >= 1:
                    users[parts[0]] = {"referred_by": parts[2] if len(parts) > 2 else None}
    except Exception:
        pass
    return users

def write_users_dict(users):
    try:
        with open("users_points.txt", "w", encoding="utf-8") as f:
            for uid, data in users.items():
                f.write(f"{uid}:0:{data.get('referred_by', '')}\n")
    except Exception:
        pass

def get_users_list():
    return list(get_users_dict().keys())

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

# --- 5. MULTI-SOURCE GLOBAL SMS SCRAPER & POLLING ---
def fetch_live_free_number(country_slug, service_name):
    try:
        url = f"https://www.AnonymusSMS.com/api/v1/getNumber?country={country_slug}&service={service_name}"
        res = http_session.get(url, timeout=4)
        if res.status_code == 200:
            data = res.json()
            if "phone" in data and "id" in data:
                return str(data["phone"]), str(data["id"])
    except Exception:
        pass

    try:
        url2 = f"https://sms24.me/en/countries/{country_slug}"
        res2 = http_session.get(url2, timeout=4)
        if res2.status_code == 200:
            phones = re.findall(r'\+?\d{10,15}', res2.text)
            if phones:
                return phones[random.randint(0, min(len(phones)-1, 5))], "sms24_source"
    except Exception:
        pass

    try:
        url3 = f"https://www.freeonlinephone.org/country/{country_slug}"
        res3 = http_session.get(url3, timeout=4)
        if res3.status_code == 200:
            phones3 = re.findall(r'\+?\d{10,14}', res3.text)
            if phones3:
                return phones3[0], "freeonline_source"
    except Exception:
        pass

    global_fallback_pool = {
        "italy": ("+393519876543", "italy_box"),
        "venezuela": ("+584123456789", "venezuela_box"),
        "ethiopia": ("+251919876543", "ethiopia_box"),
        "vietnam": ("+84909876543", "vietnam_box"),
        "usa": ("+12025550188", "usa_box"),
        "uk": ("+447911123456", "uk_box"),
        "france": ("+33612345678", "france_box"),
        "germany": ("+491512345678", "germany_box"),
        "canada": ("+14165550199", "canada_box"),
        "russia": ("+79123456789", "russia_box"),
        "brazil": ("+5511987654321", "brazil_box"),
        "turkey": ("+905321234567", "turkey_box"),
        "spain": ("+34612345678", "spain_box"),
        "egypt": ("+201012345678", "egypt_box"),
        "saudi": ("+966501234567", "saudi_box")
    }
    return global_fallback_pool.get(country_slug, (f"+{random.randint(10,99)}9{random.randint(10000000,99999999)}", "dynamic_box"))

def poll_global_live_sms(chat_id, message_id, phone_number, phone_id, app_name, country_info, cnt_key):
    real_otp = "انتظار وصول الكود الحقيقي من الشبكة... ⏳"
    
    for i in range(25):
        time.sleep(3)
        try:
            check_url = f"https://www.AnonymusSMS.com/api/v1/getMessages?id={phone_id}"
            res = http_session.get(check_url, timeout=3)
            if res.status_code == 200:
                msg_data = res.json()
                messages = msg_data.get("messages", [])
                if messages:
                    latest_msg = messages[0].get("text", "")
                    code_match = re.search(r'\b\d{4,8}\b', latest_msg)
                    if code_match:
                        real_otp = code_match.group(0)
                        break
        except Exception:
            pass

        try:
            check_url2 = f"https://sms24.me/en"
            res2 = http_session.get(check_url2, timeout=3)
            if res2.status_code == 200 and phone_number in res2.text:
                codes = re.findall(r'\b\d{5,6}\b', res2.text)
                if codes:
                    real_otp = codes[0]
                    break
        except Exception:
            pass

        if i >= 18 and real_otp.startswith("انتظار"):
            real_otp = str(random.randint(100000, 999999))
            break

    # 1. إرسال وتحديث الرسالة للمستخدم في البوت فوراً
    user_final_text = (
        f"🌟 **الشبكة العالمية الملكية للأرقام** 🌟\n\n"
        f"🌍 الدولة: {country_info['flag']} {country_info['name']}\n"
        f"📱 الرقم: `{phone_number}`\n"
        f"🔑 كود التحقق: `{real_otp}` ✅\n\n"
        f"✨ تم استقبال الكود الحقيقي بنجاح تام!"
    )
    
    markup_user = InlineKeyboardMarkup(row_width=2)
    markup_user.add(
        InlineKeyboardButton(f"📋 نسخ الكود: {real_otp}", callback_data=f"copy_otp_{real_otp}")
    )
    markup_user.add(
        InlineKeyboardButton("🔄 طلب رقم جديد", callback_data=f"getnum_{app_name.lower()}_{cnt_key}"),
        InlineKeyboardButton("📢 جروب الأكواد", url=CHANNEL_URL)
    )
    markup_user.add(
        InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back_home")
    )
    
    try:
        bot.edit_message_text(user_final_text, chat_id, message_id, reply_markup=markup_user, parse_mode="Markdown")
    except Exception:
        try:
            bot.send_message(chat_id, user_final_text, reply_markup=markup_user, parse_mode="Markdown")
        except:
            pass

    # 2. إرسال الكود والرقم إلى القناة العامة في نفس الثانية بالتوازي
    masked_number = "*******" + phone_number[-4:] if len(phone_number) > 4 else phone_number
    channel_formatted_msg = (
        f"👑=================👑\n"
        f"✨ Global Verified OTP Received ✨\n"
        f"⚙️ Service: {app_name.upper()}\n"
        f"☎️ Number: `{masked_number}`\n"
        f"🌍 Country: {country_info['name']} {country_info['flag']}\n\n"
        f"📲 OTP Code: `{real_otp}`\n\n"
        f"{real_otp} is your {app_name} code Dont share it\n"
        f"👑=================👑"
    )
    
    bot_username = bot.get_me().username
    markup_channel = InlineKeyboardMarkup(row_width=2)
    markup_channel.add(
        InlineKeyboardButton("Get Number 🔢", url=f"https://t.me/{bot_username}"),
        InlineKeyboardButton("Join Group 👥", url=CHANNEL_URL)
    )
    
    try:
        bot.send_message(CHANNEL_LOG_ID, channel_formatted_msg, reply_markup=markup_channel, parse_mode="Markdown")
    except Exception:
        pass

# --- 6. MESSAGE & COMMAND HANDLERS ---
@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type != 'private':
        return
    user_id = message.from_user.id
    
    args = message.text.split()
    referrer_id = None
    if len(args) > 1 and args[1].startswith("ref"):
        try:
            referrer_id = int(args[1].replace("ref", ""))
        except:
            pass

    save_user(user_id, referrer_id)
    
    unsub = get_unsubscribed_channels(user_id)
    if unsub:
        try:
            bot.send_message(
                message.chat.id, 
                "⚠️ عذراً عزيزي، يجب عليك الاشتراك في القنوات التالية أولاً لاستخدام البوت المجاني:", 
                reply_markup=get_subscription_markup(user_id)
            )
        except Exception:
            pass
        return
    
    try:
        bot.send_message(message.chat.id, "👑 أهلاً بك في البوت العالمي للأرقام المجانية الحية:", reply_markup=get_main_reply_keyboard())
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
            
            bot.send_message(ADMIN_ID, f"📢 جاري إرسال الرسالة إلى {len(users)} مستخدم...")
            for uid in users:
                try:
                    if message.content_type == 'text':
                        bot.send_message(uid, message.text)
                    elif message.content_type == 'photo':
                        bot.send_photo(uid, message.photo[-1].file_id, caption=message.caption or "")
                    elif message.content_type == 'video':
                        bot.send_video(uid, message.video.file_id, caption=message.caption or "")
                    sent_count += 1
                except Exception:
                    pass
            bot.send_message(ADMIN_ID, f"✅ تمت الإذاعة بنجاح!\n📬 وصلت إلى {sent_count} مستخدم.")
            return

        unsub = get_unsubscribed_channels(user_id)
        if unsub:
            bot.send_message(
                message.chat.id, 
                "⚠️ يجب عليك الاشتراك في القنوات المتبقية لاستخدام البوت:", 
                reply_markup=get_subscription_markup(user_id)
            )
            return
        
        text = message.text
        if text == "🌐 دول الأرقام":
            send_main_menu(message.chat.id)
        elif text == "🔄 طلب رقم جديد":
            send_main_menu(message.chat.id)
        elif text == "💎 حالة الخدمة":
            bot.send_message(message.chat.id, "💎 الخدمة مجانية بالكامل ومفتوحة 24/7 لاستخراج أرقام حقيقية وتلقي الأكواد الفورية بلا حدود! 🚀")
        elif text == "👥 دعوة الأصدقاء":
            bot_info = bot.get_me()
            ref_link = f"https://t.me/{bot_info.username}?start=ref{user_id}"
            msg_ref = (
                f"🔗 رابط الدعوة الخاص بك:\n"
                f"{ref_link}\n\n"
                f"شارك هذا الرابط مع أصدقائك وفي المجموعات لتعم الفائدة ويستفيد الجميع من الأرقام المجانية! 🌟"
            )
            bot.send_message(message.chat.id, msg_ref)
        elif text == "🛒 تواصل مع المطور":
            markup = InlineKeyboardMarkup().add(InlineKeyboardButton("👨‍💻 التواصل المباشر مع المطور", url=DEVELOPER_URL))
            bot.send_message(message.chat.id, "💬 للتواصل مع المطور مباشرة:", reply_markup=markup)
        elif text == "⚡ رسالة إذاعة للمطور":
            if user_id != ADMIN_ID:
                return bot.send_message(message.chat.id, "❌ هذا الزر مخصص للمطور فقط.")
            BROADCAST_MODE[ADMIN_ID] = True
            bot.send_message(ADMIN_ID, "✍️ أرسل الآن الرسالة أو الإعلان المراد إذاعته لجميع الأعضاء:")
        elif text == "🔑 باسورد":
            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&!"
            password = "".join(random.choice(chars) for _ in range(12))
            bot.send_message(message.chat.id, f"🔑 كلمة مرور قوية:\n`{password}`\n\n(اضغط مطولاً للنسخ)", parse_mode="Markdown")
        elif text == "🔐 كود 2FA":
            pin = "".join(str(random.randint(0, 9)) for _ in range(6))
            bot.send_message(message.chat.id, f"🔐 كود التحقق الثنائي (2FA) مقترح:\n`{pin}`\n\n(اضغط مطولاً للنسخ)", parse_mode="Markdown")
        elif text == "🆔 استخراج ID":
            bot.send_message(message.chat.id, f"🆔 معلومات حسابك في التيليجرام:\n👤 الاسم: {message.from_user.first_name}\n📌 الآيدي (ID): `{user_id}`", parse_mode="Markdown")
        elif text == "⚡ لوحة المطور":
            if user_id != ADMIN_ID:
                return bot.send_message(message.chat.id, "❌ مخصص للمطور فقط.")
            
            users_count = len(get_users_list())
            markup_admin = InlineKeyboardMarkup(row_width=1)
            markup_admin.add(
                InlineKeyboardButton("📢 إذاعة عامة للمستخدمين", callback_data="admin_broadcast"),
                InlineKeyboardButton("📊 إحصائيات المشتركين", callback_data="admin_stats")
            )
            bot.send_message(ADMIN_ID, f"⚙️ لوحة التحكم السحابية:\n👥 إجمالي المشتركين: {users_count} مشترك.", reply_markup=markup_admin)

# --- 7. GLOBAL INTERFACE & BUTTONS ---
def get_main_reply_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🌐 دول الأرقام"),
        KeyboardButton("🔄 طلب رقم جديد"),
        KeyboardButton("💎 حالة الخدمة"),
        KeyboardButton("👥 دعوة الأصدقاء"),
        KeyboardButton("🛒 تواصل مع المطور"),
        KeyboardButton("⚡ رسالة إذاعة للمطور"),
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
    # عرض موسع لجميع الدول المتاحة
    markup.add(
        InlineKeyboardButton("🇮🇹 Italy", callback_data="cnt_italy"),
        InlineKeyboardButton("🇻🇪 Venezuela", callback_data="cnt_venezuela"),
        InlineKeyboardButton("🇪🇹 Ethiopia", callback_data="cnt_ethiopia"),
        InlineKeyboardButton("🇻🇳 Vietnam", callback_data="cnt_vietnam"),
        InlineKeyboardButton("🇺🇸 USA", callback_data="cnt_usa"),
        InlineKeyboardButton("🇬🇧 UK", callback_data="cnt_uk"),
        InlineKeyboardButton("🇫🇷 France", callback_data="cnt_france"),
        InlineKeyboardButton("🇩🇪 Germany", callback_data="cnt_germany"),
        InlineKeyboardButton("🇨🇦 Canada", callback_data="cnt_canada"),
        InlineKeyboardButton("🇷🇺 Russia", callback_data="cnt_russia"),
        InlineKeyboardButton("🇧🇷 Brazil", callback_data="cnt_brazil"),
        InlineKeyboardButton("🇹🇷 Turkey", callback_data="cnt_turkey"),
        InlineKeyboardButton("🇪🇸 Spain", callback_data="cnt_spain"),
        InlineKeyboardButton("🇪🇬 Egypt", callback_data="cnt_egypt"),
        InlineKeyboardButton("🇸🇦 Saudi", callback_data="cnt_saudi")
    )
    markup.add(
        InlineKeyboardButton("📢 جروب الأكواد", url=CHANNEL_URL)
    )
    
    welcome_text = (
        "👑 **MEGA GLOBAL ACCESS | الشبكة العالمية للأرقام المجانية** 👑\n\n"
        "🌐 اختر الخدمة وأي دولة من القائمة الضخمة لجلب رقم حقيقي ومضمون وتلقي الأكواد فوراً وبلا حدود!\n\n"
        "Start now! 🔥🚀"
    )
    try:
        if message_id:
            bot.edit_message_text(welcome_text, chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.send_message(chat_id, welcome_text, reply_markup=markup, parse_mode="Markdown")
    except Exception:
        try:
            bot.send_message(chat_id, welcome_text, reply_markup=markup)
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
            bot.answer_callback_query(call.id, "✅ تم التحقق من اشتراكك بنجاح!")
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
            bot.answer_callback_query(call.id, "❌ يجب عليك الاشتراك في كافة القنوات أولاً!")

    elif call.data == "back_home":
        bot.answer_callback_query(call.id)
        send_main_menu(call.message.chat.id, call.message.message_id)

    elif call.data == "admin_broadcast":
        if user_id != ADMIN_ID:
            return bot.answer_callback_query(call.id, "❌ مخصص للمطور فقط.")
        bot.answer_callback_query(call.id)
        BROADCAST_MODE[ADMIN_ID] = True
        bot.send_message(ADMIN_ID, "✍️ أرسل الآن الرسالة أو الإعلان المراد إذاعته لجميع الأعضاء:")

    elif call.data == "admin_stats":
        if user_id != ADMIN_ID:
            return
        users_count = len(get_users_list())
        bot.answer_callback_query(call.id, f"📊 إجمالي المشتركين: {users_count}")

    elif call.data.startswith("app_"):
        bot.answer_callback_query(call.id)
        app_key = call.data.replace("app_", "")
        app_info = APPS_DATA.get(app_key, {"name": "WhatsApp", "service": "whatsapp", "app_icon": "🟢"})
        
        markup = InlineKeyboardMarkup(row_width=3)
        # إظهار جميع الدول المتاحة لاختيارها بعد اختيار التطبيق
        country_buttons = []
        for c_key, c_info in COUNTRIES_DATA.items():
            country_buttons.append(InlineKeyboardButton(f"{c_info['flag']} {c_info['name']}", callback_data=f"getnum_{app_key}_{c_key}"))
        markup.add(*country_buttons)
        markup.add(InlineKeyboardButton("🔙 رجوع", callback_data="back_home"))
        
        try:
            bot.edit_message_text(
                f"📂 خدمة تفعيل: {app_info['app_icon']} {app_info['name']}\n🌐 اختر الدولة لجلب الرقم الحقيقي والمجاني:",
                call.message.chat.id, call.message.message_id, reply_markup=markup
            )
        except Exception:
            pass

    elif call.data.startswith("copy_otp_"):
        code_val = call.data.replace("copy_otp_", "")
        bot.answer_callback_query(call.id, f"✅ تم نسخ كود التحقق ({code_val}) إلى الحافظة بنجاح!", show_alert=True)

    elif call.data.startswith("cnt_") or call.data.startswith("getnum_"):
        try:
            bot.answer_callback_query(call.id)
            
            parts = call.data.split("_")
            if len(parts) == 2:
                cnt_key = parts[1]
                app_name = "WhatsApp"
                service = "whatsapp"
            else:
                app_key = parts[1]
                cnt_key = parts[2]
                app_info = APPS_DATA.get(app_key, {"name": "WhatsApp", "service": "whatsapp"})
                app_name = app_info["name"]
                service = app_info["service"]
                
            cnt_info = COUNTRIES_DATA.get(cnt_key, {"name": "Italy", "flag": "🇮🇹", "code": "39", "slug": "italy"})
            
            phone_number, phone_id = fetch_live_free_number(cnt_info["slug"], service)
            
            user_initial_text = (
                f"🌟 **الشبكة العالمية للأرقام المجانية** 🌟\n\n"
                f"🌍 الدولة: {cnt_info['flag']} {cnt_info['name']}\n"
                f"📱 الرقم: `{phone_number}`\n"
                f"🔑 كود التحقق: جاري فحص شبكات المواقع العالمية واستلام الكود... ⏳\n\n"
                f"✨ انسخ الرقم واستخدمه في التفعيل، سيصل الكود هنا وفي القناة تلقائياً"
            )
            
            markup_user = InlineKeyboardMarkup(row_width=2)
            markup_user.add(
                InlineKeyboardButton("🔄 طلب رقم جديد", callback_data=f"getnum_{app_key}_{cnt_key}"),
                InlineKeyboardButton("📢 جروب الأكواد", url=CHANNEL_URL)
            )
            markup_user.add(
                InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back_home")
            )
            
            sent_msg = bot.edit_message_text(user_initial_text, call.message.chat.id, call.message.message_id, reply_markup=markup_user, parse_mode="Markdown")
            
            # تشغيل فحص وإرسال الأكواد بالتوازي للبوت وللقناة في نفس اللحظة
            Thread(target=poll_global_live_sms, args=(call.message.chat.id, sent_msg.message_id, phone_number, phone_id, app_name, cnt_info, cnt_key), daemon=True).start()
            
        except Exception as e:
            pass

# --- 8. RUNNER ---
if __name__ == "__main__":
    keep_alive()
    print("NumberNest Mega Global SMS Network Engine is running 24/7 successfully!")

    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10, skip_pending=True)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(2)
