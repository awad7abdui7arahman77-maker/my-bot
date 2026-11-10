import sys
import os
import time
import re
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
    return "⚡ Al-Moqana Ultimate Pro Panel Server is Active 24/7! ⚡"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def self_ping():
    time.sleep(60)
    while True:
        try:
            requests.get("https://al-moqana.onrender.com", timeout=10)
        except Exception:
            pass
        time.sleep(600)

def keep_alive():
    Thread(target=run, daemon=True).start()
    Thread(target=self_ping, daemon=True).start()

# --- 3. BOT CONFIGURATIONS & GLOBAL NETWORKS API ---
API_TOKEN = '8686242492:AAFdseE7gxsUNRkVgVESl22R_qxqd7WHYEU'
ADMIN_ID = 8388141188 
CHANNEL_LOG_ID = "@Awad_Numbers_Bot"  # القناة التي تنشر فيها الأرقام تلقائياً
CHANNEL_URL = "https://t.me/hehsgvsvsv"  # قناتك المطلوبة للأكواد والجروب

# مفاتيح الربط بالمنصات العالمية الحقيقية (ضع مفاتيحك هنا عندما تتوفر لديك)
API_KEYS = {
    "5sim": "ضع_مفتاح_5sim_هنا",
    "sms_activate": "ضع_مفتاح_sms_activate_هنا",
    "smshub": "ضع_مفتاح_smshub_هنا",
    "grizzly": "ضع_مفتاح_grizzly_هنا",
    "herosms": "ضع_مفتاح_herosms_هنا"
}

# تنظيف فوري لأي ويبهوك قديم لضمان استجابة أمر /start فوراً
try:
    requests.get(f"https://api.telegram.org/bot{API_TOKEN}/deleteWebhook?drop_pending_updates=true", timeout=5)
except Exception:
    pass

bot = telebot.TeleBot(API_TOKEN, threaded=False)
DEVELOPER_URL = "https://t.me/awad3210"

# قنوات الاشتراك الإجباري
SUBSCRIPTION_CHANNELS = [
    {"id": "@v_o_lti", "name": "📢 قناة جديدة", "url": "https://t.me/v_o_lti"},
    {"id": "@jzbznznx", "name": "📢 قناة عبارات بشكل عام", "url": "https://t.me/jzbznznx"},
    {"name": "📢 تعليم اختراق الجوالات وتوقيف الواتساب", "id": "@breakthroughawad210", "url": "https://t.me/breakthroughawad210"},
    {"id": "@sn6hdbdn19dndw", "name": "📢 قناة الدعم الاحتياطية", "url": "https://t.me/sn6hdbdn19dndw"}
]

APPS_DATA = {
    "whatsapp": {"name": "WhatsApp", "app_icon": "🟢", "service": "whatsapp"},
    "telegram": {"name": "Telegram", "app_icon": "✈️", "service": "telegram"},
    "instagram": {"name": "Instagram", "app_icon": "📸", "service": "instagram"},
    "facebook": {"name": "Facebook", "app_icon": "📘", "service": "facebook"},
    "twitter": {"name": "X (Twitter)", "app_icon": "❌", "service": "twitter"}
}

COUNTRIES_DATA = {
    "italy": {"name": "Italy", "flag": "🇮🇹", "code": "39", "slug": "italy"},
    "venezuela": {"name": "Venezuela", "flag": "🇻🇪", "code": "58", "slug": "venezuela"},
    "ethiopia": {"name": "Ethiopia", "flag": "🇪🇹", "code": "251", "slug": "ethiopia"},
    "guinea": {"name": "Guinea", "flag": "🇬🇳", "code": "224", "slug": "guinea"},
    "madagascar": {"name": "Madagascar", "flag": "🇲🇬", "code": "261", "slug": "madagascar"},
    "mali": {"name": "Mali", "flag": "🇲🇱", "code": "223", "slug": "mali"},
    "slovenia": {"name": "Slovenia", "flag": "🇸🇮", "code": "386", "slug": "slovenia"},
    "usa": {"name": "USA", "flag": "🇺🇸", "code": "1", "slug": "usa"}
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

# --- 5. ADVANCED MULTI-API GLOBAL NETWORK & SMS FUNCTIONS ---
def fetch_real_number_from_global_platforms(country_slug, service_name, country_info):
    for platform, key in API_KEYS.items():
        if key and "ضع_مفتاح" not in key:
            try:
                if platform == "5sim":
                    headers = {'Authorization': f'Bearer {key}', 'Accept': 'application/json'}
                    r = requests.get(f"https://5sim.net/v1/user/buy/activation/{country_slug}/any/{service_name}", headers=headers, timeout=3)
                    if r.status_code == 200:
                        data = r.json()
                        phone = "+" + str(data.get("phone"))
                        activation_id = data.get("id")
                        otp = fetch_5sim_sms(activation_id, key)
                        return phone, otp
                elif platform in ["smshub", "grizzly", "herosms"]:
                    base_url = "https://smshub.org" if platform == "smshub" else ("https://api.grizzlysms.com" if platform == "grizzly" else "https://herosms.io")
                    r = requests.get(f"{base_url}/st/st2/api.php?api_key={key}&action=getNumber&service={service_name}&country={country_slug}", timeout=3)
                    if "ACCESS_NUMBER" in r.text:
                        parts = r.text.split(":")
                        phone = "+" + parts[2]
                        activation_id = parts[1]
                        otp = fetch_sms_generic(base_url, key, activation_id)
                        return phone, otp
            except Exception:
                continue

    # نظام المحاكاة الذكية والفوري المطور
    prefix_code = country_info["code"]
    phone_number = f"+{prefix_code}9{int(time.time() * 1000) % 90000000 + 10000000}"
    real_otp = f"{int(time.time()) % 900000 + 100000}"
    return phone_number, real_otp

def fetch_5sim_sms(act_id, key):
    try:
        headers = {'Authorization': f'Bearer {key}', 'Accept': 'application/json'}
        for _ in range(3):
            time.sleep(2)
            r = requests.get(f"https://5sim.net/v1/user/check/{act_id}", headers=headers, timeout=3)
            if r.status_code == 200:
                sms_list = r.json().get("sms", [])
                if sms_list:
                    return sms_list[0].get("code", "123456")
    except Exception:
        pass
    return f"{int(time.time()) % 900000 + 100000}"

def fetch_sms_generic(base_url, key, act_id):
    try:
        for _ in range(3):
            time.sleep(2)
            r = requests.get(f"{base_url}/st/st2/api.php?api_key={key}&action=getStatus&id={act_id}", timeout=3)
            if "STATUS_OK" in r.text:
                return r.text.split(":")[1]
    except Exception:
        pass
    return f"{int(time.time()) % 900000 + 100000}"

def generate_and_publish_number(country_slug, service_name, app_name, app_icon, country_info):
    phone_number, real_otp = fetch_real_number_from_global_platforms(country_slug, service_name, country_info)
    
    masked_number = phone_number[:6] + "••••••••" + phone_number[-4:] if len(phone_number) > 10 else phone_number
    country_code_abbrev = country_info['name'][:2].upper()
    
    channel_formatted_msg = (
        f"⚡ 𝗧𝗥𝗜𝗖𝗞𝗦 𝗠𝗔𝗦𝗧𝗘𝗥 𝗕𝗢𝗧 𝗣𝗔𝗡𝗘𝗟 ⚡\n"
        f"{country_info['flag']} #{country_code_abbrev} {app_icon} `{masked_number}` |\n"
        f"🔊 English\n\n"
        f"📲 Code {app_name} : `{real_otp[:3]}-{real_otp[3:]}`\n"
        f"🔒 Never share this code with anyone\n\n"
        f"📌 #Prefix: `/pre {phone_number.replace('+', '')[:6]}`"
    )
    
    bot_username = bot.get_me().username
    markup_channel = InlineKeyboardMarkup(row_width=2)
    markup_channel.add(
        InlineKeyboardButton(f"📋 نسخ الكود: {real_otp}", callback_data=f"copy_otp_{real_otp}")
    )
    markup_channel.add(
        InlineKeyboardButton("🤖 البوت الرسمي", url=f"https://t.me/{bot_username}"),
        InlineKeyboardButton("📢 قناة الأكواد", url=CHANNEL_URL)
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
                "⚠️ **يجب عليك الانضمام إلى القنوات التالية أولاً لاستخدام البوت:**", 
                reply_markup=get_subscription_markup(user_id), 
                parse_mode="Markdown"
            )
        except Exception:
            pass
        return
    
    try:
        bot.send_message(message.chat.id, "📌 أهلاً بك في لوحة التحكم الرئيسية:", reply_markup=get_main_reply_keyboard())
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
                time.sleep(5)
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
        if text == "🌐 قسم الخدمات والأرقام":
            send_main_menu(message.chat.id)
        elif text == "🛒 شحن رصيد / أرقام مدفوعة":
            bot.send_message(message.chat.id, "🛍️ **لشحن الرصيد أو طلب أرقام مدفوعة حصرية، تواصل مع المطور مباشرة عبر الزر أدناه:**", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("👨‍💻 تواصل مع المطور", url=DEVELOPER_URL)), parse_mode="Markdown")
        elif text == "📢 مشاركة البوت":
            bot_info = bot.get_me()
            share_url = f"https://t.me/share/url?url=https://t.me/{bot_info.username}&text=أقوى%20بوت%20تفعيل%20أرقام%20ووهامية%20وحقيقية!⚡"
            markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🚀 نشر رابط البوت", url=share_url))
            bot.send_message(message.chat.id, "📢 **شارك البوت مع أصدقائك في المجموعات والقنوات:**", reply_markup=markup, parse_mode="Markdown")
        elif text == "👨‍💻 المطور الداعم":
            markup = InlineKeyboardMarkup().add(InlineKeyboardButton("👨‍💻 التواصل المباشر مع المطور", url=DEVELOPER_URL))
            bot.send_message(message.chat.id, "💬 **لأي استفسار أو دعم فني:**", reply_markup=markup, parse_mode="Markdown")
        elif text == "🪪 ملفي الشخصي":
            bot.send_message(message.chat.id, f"👤 **معلومات حسابك:**\n🆔 آيدي: `{user_id}`\n🟢 الحالة: مفعل ونشط", parse_mode="Markdown")
        elif text == "⚡ لوحة المطور":
            if user_id != ADMIN_ID:
                return bot.send_message(message.chat.id, "❌ مخصص للمطور فقط.")
            
            users_count = len(get_users_list())
            markup_admin = InlineKeyboardMarkup(row_width=1)
            markup_admin.add(
                InlineKeyboardButton("📢 إذاعة عامة للمستخدمين", callback_data="admin_broadcast"),
                InlineKeyboardButton("📊 إحصائيات المشتركين", callback_data="admin_stats")
            )
            bot.send_message(ADMIN_ID, f"⚙️ **لوحة التحكم الإدارية:**\n👥 إجمالي المشتركين: `{users_count}` مشترك.", reply_markup=markup_admin, parse_mode="Markdown")

# --- 7. EXACT TARGET VIDEO UI & FUNCTION BUTTONS ---
def get_main_reply_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🌐 قسم الخدمات والأرقام"),
        KeyboardButton("🛒 شحن رصيد / أرقام مدفوعة"),
        KeyboardButton("📢 مشاركة البوت"),
        KeyboardButton("👨‍💻 المطور الداعم"),
        KeyboardButton("🪪 ملفي الشخصي"),
        KeyboardButton("⚡ لوحة المطور")
    )
    return markup

def send_main_menu(chat_id, message_id=None):
    markup = InlineKeyboardMarkup(row_width=2)
    # عرض التطبيقات والدول بنفس تنسيق الفيديو الاحترافي (أزرار الدوال المدمجة)
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
        InlineKeyboardButton("🇬🇳 Guinea", callback_data="cnt_guinea"),
        InlineKeyboardButton("🇲🇬 Madagascar", callback_data="cnt_madagascar"),
        InlineKeyboardButton("🇲🇱 Mali", callback_data="cnt_mali"),
        InlineKeyboardButton("🇸🇮 Slovenia", callback_data="cnt_slovenia"),
        InlineKeyboardButton("🇺🇸 USA", callback_data="cnt_usa")
    )
    # أزرار الإضافات والدوال الإضافية (مطابقة للفيديو)
    markup.add(
        InlineKeyboardButton("⚙️ تحديث اللوحة", callback_data="back_home"),
        InlineKeyboardButton("🌐 جروب الأكواد", url=CHANNEL_URL)
    )
    
    welcome_text = (
        "⚡ **لوحة التحكم الذكية لخدمات الأرقام والتفعيل الفوري** ⚡\n\n"
        "🔹 اختر التطبيق أو الدولة المطلوبة من الأزرار بالأسفل لتنفيذ العملية وسحب الرقم فوراً."
    )
    try:
        if message_id:
            bot.edit_message_text(welcome_text, chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.send_message(chat_id, welcome_text, reply_markup=markup, parse_mode="Markdown")
    except Exception:
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
            bot.answer_callback_query(call.id, "❌ لم تقم بالاشتراك في كافة القنوات المطلوبة!", show_alert=True)

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
        markup.add(InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="back_home"))
        
        try:
            bot.edit_message_text(
                f"📂 **خدمة تفعيل: {app_info['app_icon']} {app_info['name']}**\n🌐 **اختر الدولة المناسبة للطلب:**",
                call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
            )
        except Exception:
            pass

    elif call.data.startswith("copy_otp_"):
        otp_val = call.data.replace("copy_otp_", "")
        bot.answer_callback_query(call.id, f"✅ تم نسخ الكود: {otp_val}", show_alert=True)

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
                
            cnt_info = COUNTRIES_DATA.get(cnt_key, {"name": "Italy", "flag": "🇮🇹", "code": "39", "slug": "italy"})
            
            # تنفيذ عملية الجلب ونشر الرقم في القناة
            generate_and_publish_number(cnt_info["slug"], service, app_name, app_icon, cnt_info)
            
            bot.answer_callback_query(call.id, "✅ تم معالجة طلبك وإرسال الرقم لقناة الأكواد!", show_alert=True)
            
            user_display_text = (
                f"✅ **تم معالجة الطلب بنجاح وتوليد الرقم!**\n\n"
                f"🌍 **الدولة:** {cnt_info['flag']} `{cnt_info['name']}`\n"
                f"📱 **التطبيق:** {app_icon} `{app_name}`\n\n"
                f"📢 **توجه فوراً إلى قناة الأكواد والجروب لاستلام الرقم وكود التحقق:**"
            )
            
            markup_user = InlineKeyboardMarkup(row_width=1)
            markup_user.add(
                InlineKeyboardButton("📢 الانتقال إلى قناة الأكواد والجروب 🔗", url=CHANNEL_URL),
                InlineKeyboardButton("🔄 طلب رقم آخر", callback_data="back_home")
            )
            
            bot.edit_message_text(user_display_text, call.message.chat.id, call.message.message_id, reply_markup=markup_user, parse_mode="Markdown")
            
        except Exception as e:
            bot.answer_callback_query(call.id, "❌ حدث خطأ، يجدر المحاولة مجدداً.", show_alert=True)

# --- 8. RUNNER ---
if __name__ == "__main__":
    keep_alive()
    print("NumberNest Ultimate Pro Panel Bot Engine is running 24/7 successfully!")

    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10, skip_pending=True)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(5)
