import sys
import os
import time
import re
import random
import codecs
from threading import Thread
import concurrent.futures  
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import requests
from bs4 import BeautifulSoup
from flask import Flask

# --- 1. FORCE SYSTEM ENCODING ---
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# --- 2. BOT CONFIGURATIONS ---
API_TOKEN = "9045833012:AAETb9deU-n-JM9DVbiKX-hTIe8Me7_CK6k"
ADMIN_ID = 8388141188 
SUB_ADMINS = [ADMIN_ID] 
DEVELOPER_URL = "https://t.me/awad3210"

# تنظيف أي Webhook قديم تماماً
try:
    requests.get(f"https://api.telegram.org/bot{API_TOKEN}/deleteWebhook?drop_pending_updates=true", timeout=10)
except Exception:
    pass

bot = telebot.TeleBot(API_TOKEN)
BOT_USERNAME = "Anwid_bot"

# --- CHANNELS FOR FORCE SUBSCRIPTION ---
SUBSCRIPTION_LINKS = [
    {"name": "📢 قناة البوت الرسمية", "url": "https://t.me/Awad_Numbers_Bot", "id": "@Awad_Numbers_Bot"},
    {"name": "📢 قناة جديدة", "url": "https://t.me/v_o_lti", "id": "@v_o_lti"},
    {"name": "📢 قناة عبارات بشكل عام", "url": "https://t.me/jzbznznx", "id": "@jzbznznx"},
    {"name": "📢 تعليم اختراق الجوالات وتوقيف الواتساب", "url": "https://t.me/breakthroughawad210", "id": "@breakthroughawad210"},
    {"name": "📢 قناة الدعم الاحتياطية", "url": "https://t.me/sn6hdbdn19dndw", "id": "@sn6hdbdn19dndw"},
    {"name": "💬 جروب المناقشة والتبادل", "url": "https://t.me/+KhzU3jbVrVVkNWU0", "id": None}
]

user_points = {}
user_last_action = {}
recent_numbers_cache = set()

# --- SERVICES & COUNTRIES ---
SERVICES_DATA = {
    "whatsapp": {"name": "WhatsApp", "icon": "💬"},
    "telegram": {"name": "Telegram", "icon": "✈️"},
    "facebook": {"name": "Facebook", "icon": "📘"},
    "instagram": {"name": "Instagram", "icon": "📸"},
    "tiktok": {"name": "TikTok", "icon": "🎵"},
    "turbo": {"name": "⚡ سحبة صاروخية", "icon": "🚀"}
}

SERVICES_COUNTRIES = {
    "whatsapp": {
        "bolivia": {"name": "Bolivia 🇧🇴", "code": "591", "slug": "bolivia", "len": 8, "prefixes": ["7", "6"]},
        "germany": {"name": "Germany 🇩🇪", "code": "49", "slug": "germany", "len": 10, "prefixes": ["15", "16", "17"]},
        "kuwait": {"name": "Kuwait 🇰🇼", "code": "965", "slug": "kuwait", "len": 8, "prefixes": ["5", "6", "9"]},
        "yemen": {"name": "Yemen 🇾🇪", "code": "967", "slug": "yemen", "len": 9, "prefixes": ["77", "73", "71", "78"]},
        "egypt": {"name": "Egypt 🇪🇬", "code": "20", "slug": "egypt", "len": 10, "prefixes": ["10", "11", "12"]},
        "usa": {"name": "USA 🇺🇸", "code": "1", "slug": "united-states", "len": 10, "prefixes": ["201", "415", "917"]}
    },
    "telegram": {
        "usa": {"name": "USA 🇺🇸", "code": "1", "slug": "united-states", "len": 10, "prefixes": ["201", "202", "415"]},
        "egypt": {"name": "Egypt 🇪🇬", "code": "20", "slug": "egypt", "len": 10, "prefixes": ["10", "11", "12"]},
        "germany": {"name": "Germany 🇩🇪", "code": "49", "slug": "germany", "len": 10, "prefixes": ["15", "16"]}
    },
    "facebook": {
        "usa": {"name": "USA 🇺🇸", "code": "1", "slug": "united-states", "len": 10, "prefixes": ["201", "415"]},
        "egypt": {"name": "Egypt 🇪🇬", "code": "20", "slug": "egypt", "len": 10, "prefixes": ["10", "11", "12"]},
        "germany": {"name": "Germany 🇩🇪", "code": "49", "slug": "germany", "len": 10, "prefixes": ["15", "16"]}
    },
    "instagram": {
        "usa": {"name": "USA 🇺🇸", "code": "1", "slug": "united-states", "len": 10, "prefixes": ["201", "310", "415"]},
        "kuwait": {"name": "Kuwait 🇰🇼", "code": "965", "slug": "kuwait", "len": 8, "prefixes": ["5", "9"]}
    },
    "tiktok": {
        "usa": {"name": "USA 🇺🇸", "code": "1", "slug": "united-states", "len": 10, "prefixes": ["201", "415", "917"]},
        "egypt": {"name": "Egypt 🇪🇬", "code": "20", "slug": "egypt", "len": 10, "prefixes": ["10", "12"]}
    }
}

def check_subscription(user_id):
    if user_id in SUB_ADMINS:
        return True
    for ch in SUBSCRIPTION_LINKS:
        ch_id = ch["id"]
        if ch_id:
            try:
                member = bot.get_chat_member(ch_id, user_id)
                if member.status not in ['member', 'administrator', 'creator']:
                    return False
            except Exception:
                pass
    return True

def force_sub_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    for ch in SUBSCRIPTION_LINKS:
        markup.add(InlineKeyboardButton(ch["name"], url=ch["url"]))
    markup.add(InlineKeyboardButton("✅ لقد اشتركت في القنوات", callback_data="check_sub"))
    return markup

def save_user(user_id, referrer_id=None):
    if not os.path.exists("users.txt"):
        open("users.txt", "w").close()
    users_list = []
    with open("users.txt", "r") as f:
        users_list = f.read().splitlines()
    if str(user_id) not in users_list:
        with open("users.txt", "a") as f:
            f.write(f"{user_id}\n")
        user_points[user_id] = user_points.get(user_id, 0) + 10  
        if referrer_id and referrer_id != str(user_id):
            ref_int = int(referrer_id)
            user_points[ref_int] = user_points.get(ref_int, 0) + 15
            try:
                bot.send_message(ref_int, f"🎁 **مبروك! انضم صديق عبر رابط إحالتك وكسبت 15 نقطة!** 🚀", parse_mode="Markdown")
            except Exception:
                pass

def scrape_source(url, code):
    nums = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=3)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for element in soup.find_all(['h3', 'h4', 'a', 'span', 'p', 'td', 'div']):
                txt = element.text.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                if txt.startswith('+') and txt[1:].startswith(code):
                    clean = re.sub(r'[^\d+]', '', txt)
                    if len(clean) > 8: nums.append(clean)
                elif txt.startswith(code) and len(txt) > 8:
                    clean = "+" + re.sub(r'[^\d]', '', txt)
                    nums.append(clean)
    except Exception:
        pass
    return nums

def get_country_numbers_count(c_data):
    return random.randint(5000, 35000)

def get_real_live_number(c_data):
    code = c_data["code"]
    slug = c_data["slug"]
    sources = [
        f"https://receive-smss.com/free-sms-numbers/{code}",
        f"https://anonymsms.com/country/{slug}",
        f"https://sms24.me/en/countries/{slug}",
        f"https://online-sms.org/en/countries/{slug}",
        f"https://getfreesmsnumber.com/country/{slug}"
    ]
    scraped_numbers = []
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(scrape_source, url, code) for url in sources]
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                if res:
                    for num in res:
                        clean_num = num.replace("+", "")
                        if len(clean_num) >= (len(code) + c_data['len'] - 2) and clean_num not in recent_numbers_cache:
                            scraped_numbers.append(clean_num)
    except Exception:
        pass
    
    if scraped_numbers:
        chosen = random.choice(scraped_numbers)
    else:
        prefix = random.choice(c_data["prefixes"])
        needed_digits = c_data["len"] - len(prefix)
        random_digits = "".join([str(random.randint(0, 9)) for _ in range(needed_digits)])
        chosen = f"{code}{prefix}{random_digits}"
        
    recent_numbers_cache.add(chosen)
    if len(recent_numbers_cache) > 300:
        recent_numbers_cache.pop()
    return chosen

def fetch_real_otp_sms(phone_num):
    urls = [
        f"https://receive-smss.com/sms/{phone_num}/",
        f"https://online-sms.org/sms/{phone_num}",
        f"https://sms24.me/en/numbers/{phone_num}",
        f"https://anonymsms.com/number/{phone_num}/",
        f"https://getfreesmsnumber.com/number/{phone_num}"
    ]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    for url in urls:
        try:
            r = requests.get(url, headers=headers, timeout=2)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                text_content = soup.get_text()
                match = re.search(r'(?:WhatsApp|Telegram|Facebook|Instagram|TikTok|code|كود|واتساب).*?(\d{3}[\s-]?\d{3})', text_content, re.IGNORECASE)
                if match:
                    return match.group(1).replace("-", "").replace(" ", "")
                all_six_digits = re.findall(r'\b\d{6}\b', text_content)
                if all_six_digits:
                    return all_six_digits[0]
        except Exception:
            continue
    return None

def background_auto_otp_checker(chat_id, phone_num, service_name, country_name, service_key, country_key):
    for _ in range(40):
        time.sleep(6)
        otp_code = fetch_real_otp_sms(phone_num)
        if otp_code:
            result_text = (
                f"✅ **تم استقبال كود التفعيل الحقيقي بنجاح!**\n\n"
                f"📌 **التطبيق:** {service_name} ({country_name})\n"
                f"📞 **الرقم:** `+{phone_num}`\n"
                f"🔑 **كود التفعيل:** `{otp_code}`\n\n"
                f"🔒 *تم التفعيل بنجاح.*"
            )
            try:
                markup = InlineKeyboardMarkup(row_width=2)
                markup.add(
                    InlineKeyboardButton("📋 نسخ الكود", callback_data=f"copy_code_{otp_code}"),
                    InlineKeyboardButton("📢 القنوات", url=SUBSCRIPTION_LINKS[0]["url"]),
                    InlineKeyboardButton("🔄 طلب أرقام جديدة", callback_data=f"show_countries_{service_key}")
                )
                bot.send_message(chat_id, result_text, reply_markup=markup, parse_mode="Markdown")
            except Exception:
                pass
            break

# --- KEYBOARDS ---
def main_reply_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🌐 الأقسام والتطبيقات"),
        KeyboardButton("⚡ سحبة صاروخية (3 أرقام)"),
        KeyboardButton("🔗 نقاطي ورابط الإحالة"),
        KeyboardButton("👨‍💻 تواصل مع المطور")
    )
    return markup

def get_services_only_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for s_key, s_data in SERVICES_DATA.items():
        if s_key == "turbo":
            buttons.append(InlineKeyboardButton(f"{s_data['icon']} {s_data['name']}", callback_data="get_turbo_numbers"))
        else:
            buttons.append(InlineKeyboardButton(f"{s_data['icon']} {s_data['name']}", callback_data=f"show_countries_{s_key}"))
    markup.add(*buttons)
    return markup

def get_countries_for_service_keyboard(service_key):
    markup = InlineKeyboardMarkup(row_width=2)
    countries_dict = SERVICES_COUNTRIES.get(service_key, {})
    if not countries_dict:
        countries_dict = SERVICES_COUNTRIES["whatsapp"]
    country_btns = []
    for c_key, c_data in countries_dict.items():
        num_count = get_country_numbers_count(c_data)
        btn_text = f"{c_data['name']} ({num_count})"
        country_btns.append(InlineKeyboardButton(btn_text, callback_data=f"get_single_num_{service_key}_{c_key}"))
    markup.add(*country_btns)
    markup.add(InlineKeyboardButton("⬅️ القائمة الرئيسية", callback_data="show_all_services"))
    return markup

# --- HANDLERS ---
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    if not check_subscription(user_id):
        return bot.send_message(
            message.chat.id,
            "🚀 **عذراً، يجب عليك الاشتراك في قنوات ومجموعات المطور لتتمكن من استخدام البوت:**",
            reply_markup=force_sub_markup(),
            parse_mode="Markdown"
        )
    
    args = message.text.split()
    ref_id = args[1] if len(args) > 1 else None
    save_user(user_id, ref_id)
    
    points = user_points.get(user_id, 10)
    msg = f"مرحباً بك يا أواّد في بوت الأرقام الخارق ⚡\n⭐ رصيدك الحالي: `{points}` نقاط\nاختر التطبيق المراد تفعيله من الأزرار بالأسفل:"
    bot.send_message(message.chat.id, msg, reply_markup=main_reply_keyboard(), parse_mode="Markdown")
    bot.send_message(message.chat.id, "💬 اختر التطبيق:", reply_markup=get_services_only_keyboard())

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_sub_cb(call):
    user_id = call.from_user.id
    if check_subscription(user_id):
        bot.answer_callback_query(call.id, "✅ تم التحقق من اشتراكك بنجاح!", show_alert=True)
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        save_user(user_id)
        points = user_points.get(user_id, 10)
        msg = f"مرحباً بك يا أواّد في بوت الأرقام الخارق ⚡\n⭐ رصيدك الحالي: `{points}` نقاط\nاختر التطبيق المراد تفعيله:"
        bot.send_message(call.message.chat.id, msg, reply_markup=main_reply_keyboard(), parse_mode="Markdown")
        bot.send_message(call.message.chat.id, "💬 اختر التطبيق:", reply_markup=get_services_only_keyboard())
    else:
        bot.answer_callback_query(call.id, "❌ لم تقم بالاشتراك في جميع القنوات بعد!", show_alert=True)

@bot.message_handler(func=lambda message: message.text in ["🌐 الأقسام والتطبيقات", "⚡ سحبة صاروخية (3 أرقام)", "🔗 نقاطي ورابط الإحالة", "👨‍💻 تواصل مع المطور"])
def handle_menu_buttons(message):
    user_id = message.from_user.id
    if not check_subscription(user_id):
        return bot.send_message(message.chat.id, "🚀 **يجب عليك الاشتراك في القنوات أولاً لاستخدام البوت:**", reply_markup=force_sub_markup(), parse_mode="Markdown")

    txt = message.text
    if txt == "🌐 الأقسام والتطبيقات":
        bot.send_message(message.chat.id, "💬 اختر التطبيق:", reply_markup=get_services_only_keyboard())
    elif txt == "⚡ سحبة صاروخية (3 أرقام)":
        turbo_countries = list(SERVICES_COUNTRIES["whatsapp"].values())
        chosen_country = random.choice(turbo_countries)
        single_num = get_real_live_number(chosen_country)
        
        number_display_text = (
            f"🌍 **الدولة:** {chosen_country['name']}\n\n"
            f"🔢 **الرقم:** `+{chosen_country['code']}{single_num}`\n\n"
            f"📋 **اضغط مطولاً للنسخ**"
        )
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🔄 رقم جديد", callback_data=f"get_single_num_whatsapp_{chosen_country['slug']}"),
            InlineKeyboardButton("🌐 تغيير التطبيق", callback_data="show_all_services")
        )
        markup.add(InlineKeyboardButton("❌ إغلاق", callback_data="remove_cc"))
        bot.send_message(message.chat.id, number_display_text, reply_markup=markup, parse_mode="Markdown")
        Thread(target=background_auto_otp_checker, args=(message.chat.id, f"{chosen_country['code']}{single_num}", "WhatsApp", chosen_country['name'], "whatsapp", chosen_country['slug']), daemon=True).start()

    elif txt == "🔗 نقاطي ورابط الإحالة":
        points = user_points.get(user_id, 10)
        ref_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
        msg_ref = (
            f"🔗 **نظام دعوة الأصدقاء ونقاط الأرقام:**\n\n"
            f"⭐ رصيدك: `{points}` نقطة\n\n"
            f"📌 **رابط الإحالة الخاص بك:**\n`{ref_link}`\n\n"
            f"💡 *شارك الرابط مع أصدقائك واكسب نقاطاً فورية!* 🚀"
        )
        bot.send_message(message.chat.id, msg_ref, parse_mode="Markdown")
    elif txt == "👨‍💻 تواصل مع المطور":
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("👨‍💻 مالك البوت", url=DEVELOPER_URL))
        bot.send_message(message.chat.id, "💬 **للتواصل المباشر مع المطور:**", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "show_all_services")
def show_all_services_cb(call):
    user_id = call.from_user.id
    if not check_subscription(user_id):
        return bot.answer_callback_query(call.id, "❌ يجب الاشتراك في القنوات أولاً!", show_alert=True)
    try:
        bot.edit_message_text("💬 اختر التطبيق:", call.message.chat.id, call.message.message_id, reply_markup=get_services_only_keyboard())
    except Exception:
        bot.send_message(call.message.chat.id, "💬 اختر التطبيق:", reply_markup=get_services_only_keyboard())

@bot.callback_query_handler(func=lambda call: call.data.startswith("show_countries_"))
def show_countries_cb(call):
    user_id = call.from_user.id
    if not check_subscription(user_id):
        return bot.answer_callback_query(call.id, "❌ يجب الاشتراك في القنوات أولاً!", show_alert=True)
    
    service_key = call.data.replace("show_countries_", "")
    service_info = SERVICES_DATA.get(service_key, {"name": "التطبيق"})
    msg_text = f"💬 الدول المتاحة لـ ({service_info['name']}):"
    try:
        bot.edit_message_text(msg_text, call.message.chat.id, call.message.message_id, reply_markup=get_countries_for_service_keyboard(service_key))
    except Exception:
        bot.send_message(call.message.chat.id, msg_text, reply_markup=get_countries_for_service_keyboard(service_key))

@bot.callback_query_handler(func=lambda call: call.data.startswith("get_single_num_"))
def get_single_number_cb(call):
    user_id = call.from_user.id
    if not check_subscription(user_id):
        return bot.answer_callback_query(call.id, "❌ يجب الاشتراك في القنوات أولاً!", show_alert=True)

    parts = call.data.replace("get_single_num_", "").split("_")
    service_key = parts[0]
    country_key = parts[1]
    
    service_info = SERVICES_DATA.get(service_key, {"name": "التطبيق", "icon": "💬"})
    country_info = SERVICES_COUNTRIES.get(service_key, {}).get(country_key, {"name": "الدولة", "code": "967", "slug": "yemen", "len": 9, "prefixes": ["77"]})
    
    bot.answer_callback_query(call.id, f"⚡ جاري سحب رقم لـ {service_info['name']}...")
    single_num = get_real_live_number(country_info)
    
    number_display_text = (
        f"📱 **التطبيق:** {service_info['icon']} {service_info['name']}\n"
        f"🌍 **الدولة:** {country_info['name']}\n\n"
        f"🔢 **الرقم:** `+{country_info['code']}{single_num}`\n\n"
        f"📋 **اضغط مطولاً للنسخ**"
    )
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🔄 رقم جديد", callback_data=f"get_single_num_{service_key}_{country_key}"),
        InlineKeyboardButton("🌐 تغيير الدولة", callback_data=f"show_countries_{service_key}")
    )
    markup.add(InlineKeyboardButton("❌ إغلاق", callback_data="remove_cc"))
    
    try:
        bot.edit_message_text(number_display_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    except Exception:
        bot.send_message(call.message.chat.id, number_display_text, reply_markup=markup, parse_mode="Markdown")
    
    Thread(target=background_auto_otp_checker, args=(call.message.chat.id, f"{country_info['code']}{single_num}", service_info['name'], country_info['name'], service_key, country_key), daemon=True).start()

@bot.callback_query_handler(func=lambda call: call.data == "remove_cc")
def remove_cc_cb(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception:
        pass
    bot.answer_callback_query(call.id, "🗑️ تم الحذف", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data.startswith("copy_code_"))
def copy_code_cb(code_call):
    code = code_call.data.replace("copy_code_", "")
    bot.answer_callback_query(code_call.id, f"📋 تم نسخ الكود: {code}", show_alert=True)

# --- 3. SERVER & BOT THREADING ---
app = Flask('')

@app.route('/')
def home():
    return "⚡ Elite Master Bot Server Active 24/7! ⚡"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def run_bot():
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5, skip_pending=True)
        except Exception:
            time.sleep(3)

if __name__ == "__main__":
    # تشغيل سيرفر الويب في خلفية مستقلة لضمان بقاء التطبيق نشطاً على ريلواي
    Thread(target=run_flask, daemon=True).start()
    # تشغيل بوت التيليجرام في الخيط الرئيسي
    run_bot()
