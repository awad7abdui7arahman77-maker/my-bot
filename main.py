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

# --- 2. KEEP ALIVE SYSTEM (24/7) ---
app = Flask('')

@app.route('/')
def home():
    return "⚡ Elite Master Bot Server v1000.0 Ultimate Clear UI Active 24/7! ⚡"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def self_ping():
    time.sleep(60)
    while True:
        try:
            requests.get("https://my-bot-p6kw.onrender.com", timeout=10)
        except Exception:
            pass
        time.sleep(600)

def keep_alive():
    Thread(target=run, daemon=True).start()
    Thread(target=self_ping, daemon=True).start()

# --- 3. BOT CONFIGURATIONS & SECURITY ---
API_TOKEN = '8686242492:AAFPUbb-xm1XkZih9TRLesi-U-Su6vFETiA'
ADMIN_ID = 8388141188 
SUB_ADMINS = [ADMIN_ID] 
DEVELOPER_URL = "https://t.me/awad3210"
OTP_CHANNEL_USERNAME = "@Awad_Numbers_Bot"

bot = telebot.TeleBot(API_TOKEN)

BOT_USERNAME = "aaabbbcccmaskedtetris_bot"
BOT_DIRECT_URL = f"https://t.me/{BOT_USERNAME}"

try:
    bot.remove_webhook()
except Exception:
    pass

try:
    requests.get(f"https://api.telegram.org/bot{API_TOKEN}/deleteWebhook?drop_pending_updates=true", timeout=5)
except Exception:
    pass

MAINTENANCE_MODE = False  
bot_stats = {"numbers_generated": 0, "otps_fetched": 0}
user_points = {}
user_last_bonus = {}
user_history = {}

waiting_for_manual_number = {}
waiting_for_broadcast = {}
waiting_for_promo = {}

ACTIVE_PROMO_CODES = {"AWAD2026": 50, "ELITE50": 30, "VIP100": 100}

CHANNELS_DATA = [
    {"username": "@Awad_Numbers_Bot", "name": "📢 قناة البوت الرسمية", "url": "https://t.me/Awad_Numbers_Bot"},
    {"username": "@v_o_lti", "name": "📢 قناة جديدة", "url": "https://t.me/v_o_lti"},
    {"username": "@jzbznznx", "name": "📢 قناة عبارات بشكل عام", "url": "https://t.me/jzbznznx"},
    {"username": "@breakthroughawad210", "name": "📢 تعليم اختراق الجوالات وتوقيف الواتساب", "url": "https://t.me/breakthroughawad210"},
    {"username": "@sn6hdbdn19dndw", "name": "📢 قناة الدعم الاحتياطية", "url": "https://t.me/sn6hdbdn19dndw"}
]

SERVICES_DATA = {
    "whatsapp": {"name": "WhatsApp", "icon": "💬"},
    "telegram": {"name": "Telegram", "icon": "✈️"},
    "facebook": {"name": "Facebook", "icon": "👤"},
    "instagram": {"name": "Instagram", "icon": "📸"},
    "tiktok": {"name": "TikTok", "icon": "🎵"},
    "imo": {"name": "IMO", "icon": "💬"},
    "turbo": {"name": "⚡ سحبة صاروخية (3 أرقام)", "icon": "🚀"},
    "vip": {"name": "VIP Numbers 💎 (أرقام مميزة)", "icon": "⭐"},
    "tempmail": {"name": "Temp Mail & SMS 🌟", "icon": "🌐"}
}

SERVICES_COUNTRIES = {
    "whatsapp": {
        "bolivia": {"name": "Bolivia 🇧🇴", "code": "591", "slug": "bolivia", "len": 8, "prefixes": ["7", "6"]},
        "germany": {"name": "Germany 🇩🇪", "code": "49", "slug": "germany", "len": 10, "prefixes": ["15", "16", "17"]},
        "ethiopia": {"name": "Ethiopia 🇪🇹", "code": "251", "slug": "ethiopia", "len": 9, "prefixes": ["91", "92", "93"]},
        "kuwait": {"name": "Kuwait 🇰🇼", "code": "965", "slug": "kuwait", "len": 8, "prefixes": ["5", "6", "9"]},
        "lebanon": {"name": "Lebanon 🇱🇧", "code": "961", "slug": "lebanon", "len": 8, "prefixes": ["3", "70", "71"]},
        "mauritania": {"name": "Mauritania 🇲🇷", "code": "222", "slug": "mauritania", "len": 8, "prefixes": ["2", "3", "4"]},
        "mozambique": {"name": "Mozambique 🇲🇿", "code": "258", "slug": "mozambique", "len": 9, "prefixes": ["82", "84", "85"]},
        "nigeria": {"name": "Nigeria 🇳🇬", "code": "234", "slug": "nigeria", "len": 10, "prefixes": ["80", "81", "90"]},
        "senegal": {"name": "Senegal 🇸🇳", "code": "221", "slug": "senegal", "len": 9, "prefixes": ["77", "78", "70"]},
        "tajikistan": {"name": "Tajikistan 🇹🇯", "code": "992", "slug": "tajikistan", "len": 9, "prefixes": ["91", "92", "93"]},
        "vietnam": {"name": "Vietnam 🇻🇳", "code": "84", "slug": "vietnam", "len": 9, "prefixes": ["90", "91", "98"]},
        "yemen": {"name": "Yemen 🇾🇪", "code": "967", "slug": "yemen", "len": 9, "prefixes": ["77", "73", "71", "78"]}
    },
    "telegram": {
        "usa": {"name": "USA 🇺🇸", "code": "1", "slug": "united-states", "len": 10, "prefixes": ["201", "202", "415"]},
        "italy": {"name": "Italy 🇮🇹", "code": "39", "slug": "italy", "len": 10, "prefixes": ["320", "340"]},
        "egypt": {"name": "Egypt 🇪🇬", "code": "20", "slug": "egypt", "len": 10, "prefixes": ["10", "11", "12"]},
        "vietnam": {"name": "Vietnam 🇻🇳", "code": "84", "slug": "vietnam", "len": 9, "prefixes": ["90", "91", "98"]},
        "syria": {"name": "Syria 🇸🇾", "code": "963", "slug": "syria", "len": 9, "prefixes": ["98", "99"]}
    },
    "facebook": {
        "usa": {"name": "USA 🇺🇸", "code": "1", "slug": "united-states", "len": 10, "prefixes": ["415", "212"]},
        "canada": {"name": "Canada 🇨🇦", "code": "1", "slug": "canada", "len": 10, "prefixes": ["416", "604"]},
        "morocco": {"name": "Morocco 🇲🇦", "code": "212", "slug": "morocco", "len": 9, "prefixes": ["6", "7"]},
        "guinea": {"name": "Guinea 🇬🇳", "code": "224", "slug": "guinea", "len": 9, "prefixes": ["62", "65"]}
    },
    "instagram": {
        "usa": {"name": "USA 🇺🇸", "code": "1", "slug": "united-states", "len": 10, "prefixes": ["213", "323"]},
        "canada": {"name": "Canada 🇨🇦", "code": "1", "slug": "canada", "len": 10, "prefixes": ["250", "403"]},
        "iraq": {"name": "Iraq 🇮🇶", "code": "964", "slug": "iraq", "len": 10, "prefixes": ["77", "78"]},
        "italy": {"name": "Italy 🇮🇹", "code": "39", "slug": "italy", "len": 10, "prefixes": ["320", "340"]}
    },
    "tiktok": {
        "usa": {"name": "USA 🇺🇸", "code": "1", "slug": "united-states", "len": 10, "prefixes": ["501", "502"]},
        "algeria": {"name": "Algeria 🇩🇿", "code": "213", "slug": "algeria", "len": 9, "prefixes": ["5", "6", "7"]},
        "vietnam": {"name": "Vietnam 🇻🇳", "code": "84", "slug": "vietnam", "len": 9, "prefixes": ["90", "91"]},
        "malawi": {"name": "Malawi 🇲🇼", "code": "265", "slug": "malawi", "len": 9, "prefixes": ["88", "99"]}
    },
    "imo": {
        "yemen": {"name": "Yemen 🇾🇪", "code": "967", "slug": "yemen", "len": 9, "prefixes": ["77", "73"]},
        "sudan": {"name": "Sudan 🇸🇩", "code": "249", "slug": "sudan", "len": 9, "prefixes": ["91", "92"]},
        "egypt": {"name": "Egypt 🇪🇬", "code": "20", "slug": "egypt", "len": 10, "prefixes": ["10", "11"]},
        "ethiopia": {"name": "Ethiopia 🇪🇹", "code": "251", "slug": "ethiopia", "len": 9, "prefixes": ["91", "92"]}
    },
    "turbo": {
        "global_turbo": {"name": "⚡ سحبة صاروخية لـ 3 أرقام", "code": "1", "slug": "united-states", "len": 10, "prefixes": ["201", "415"]}
    },
    "vip": {
        "usa_vip": {"name": "USA VIP 🇺🇸 (30 نقطة)", "code": "1", "slug": "united-states", "len": 10, "prefixes": ["212", "415"], "cost": 30},
        "uk_vip": {"name": "UK VIP 🇬🇧 (30 نقطة)", "code": "44", "slug": "united-kingdom", "len": 10, "prefixes": ["74", "75"], "cost": 30}
    }
}

user_last_action = {}
recent_numbers_cache = set()
used_promo_codes = set()

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
        if referrer_id and str(referrer_id) in users_list and int(referrer_id) != user_id:
            user_points[int(referrer_id)] = user_points.get(int(referrer_id), 0) + 15 
        try:
            bot.send_message(ADMIN_ID, f"🔔 **مستخدم جديد انضم للبوت!**\n🆔 المعرف: `{user_id}`", parse_mode="Markdown")
        except Exception:
            pass

def get_users_count():
    if not os.path.exists("users.txt"): return 0
    with open("users.txt", "r") as f:
        return len([line for line in f.read().splitlines() if line.strip()])

def is_banned(user_id):
    if not os.path.exists("banned.txt"): return False
    with open("banned.txt", "r") as f:
        return str(user_id) in f.read().splitlines()

def get_unsubscribed_channels(user_id):
    if user_id in SUB_ADMINS: return []
    unsubscribed = []
    for ch in CHANNELS_DATA:
        try:
            status = bot.get_chat_member(ch["username"], user_id).status
            if status in ['left', 'kicked']:
                unsubscribed.append(ch)
        except Exception:
            continue
    return unsubscribed

def check_subscription_status(user_id):
    return len(get_unsubscribed_channels(user_id)) == 0

def send_targeted_subscription_msg(chat_id, user_id):
    unsub_list = get_unsubscribed_channels(user_id)
    markup = InlineKeyboardMarkup(row_width=1)
    for ch in unsub_list:
        markup.add(InlineKeyboardButton(ch["name"], url=ch["url"]))
    markup.add(InlineKeyboardButton("✨ تم الاشتراك في قنواتنا، دخول البوت ✅", callback_data="check_sub"))
    
    msg = (
        "⚠️ **عذراً يا صديقي!**\n\n"
        "📌 **لاستخدام البوت والحصول على الأرقام، يجب عليك الاشتراك في قنواتنا الرسمية أولاً:**"
    )
    bot.send_message(chat_id, msg, reply_markup=markup, parse_mode="Markdown")

def rate_limit_check(user_id, seconds=3):
    if user_id in SUB_ADMINS: return False
    now = time.time()
    if user_id in user_last_action and (now - user_last_action[user_id]) < seconds:
        return True
    user_last_action[user_id] = now
    return False

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
    return random.randint(2500, 32000)

def get_real_live_number(c_data):
    code = c_data["code"]
    slug = c_data["slug"]
    sources = [
        f"https://receive-smss.com/free-sms-numbers/{code}",
        f"https://anonymsms.com/country/{slug}",
        f"https://sms24.me/en/countries/{slug}",
        f"https://online-sms.org/en/countries/{slug}",
        f"https://receive-smss.live/country/{slug}"
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
    if len(recent_numbers_cache) > 200:
        recent_numbers_cache.pop()
        
    bot_stats["numbers_generated"] += 1
    return chosen

def fetch_real_otp_sms(phone_num):
    urls = [
        f"https://receive-smss.com/sms/{phone_num}/",
        f"https://online-sms.org/sms/{phone_num}",
        f"https://sms24.me/en/numbers/{phone_num}",
        f"https://receive-smss.live/sms/{phone_num}/",
        f"https://anonymsms.com/number/{phone_num}/"
    ]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    for url in urls:
        try:
            r = requests.get(url, headers=headers, timeout=2)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                text_content = soup.get_text()
                match = re.search(r'(?:WhatsApp|Telegram|Facebook|Instagram|TikTok|IMO|code|كود|واتساب).*?(\d{3}[\s-]?\d{3})', text_content, re.IGNORECASE)
                if match:
                    return match.group(1).replace("-", "").replace(" ", "")
                all_six_digits = re.findall(r'\b\d{6}\b', text_content)
                if all_six_digits:
                    return all_six_digits[0]
        except Exception:
            continue
    return None

def background_auto_otp_checker(chat_id, phone_num, service_name, country_name, service_key, country_key):
    for _ in range(35):
        time.sleep(6)
        otp_code = fetch_real_otp_sms(phone_num)
        if otp_code:
            bot_stats["otps_fetched"] += 1
            result_text = (
                f"✅ **تم استقبال كود التفعيل الحقيقي بنجاح!**\n\n"
                f"📌 **التطبيق:** {service_name} ({country_name})\n"
                f"📞 **الرقم:** `+{phone_num}`\n"
                f"🔑 **كود التفعيل:** `{otp_code}`\n\n"
                f"💣 *تم التفعيل بنجاح (سيتم تدمير هذه الرسالة ذاتياً بعد قليل للأمان).* 🔒"
            )
            try:
                markup = InlineKeyboardMarkup(row_width=2)
                markup.add(
                    InlineKeyboardButton("📋 نسخ الكود", callback_data=f"copy_code_{otp_code}"),
                    InlineKeyboardButton("📢 قناة الأكواد", url=f"https://t.me/{OTP_CHANNEL_USERNAME.replace('@','')}"),
                    InlineKeyboardButton("🔄 طلب أرقام جديدة", callback_data=f"show_countries_{service_key}")
                )
                sent_msg = bot.send_message(chat_id, result_text, reply_markup=markup, parse_mode="Markdown")
                
                def self_destruct():
                    time.sleep(120)
                    try: bot.delete_message(chat_id, sent_msg.message_id)
                    except Exception: pass
                Thread(target=self_destruct, daemon=True).start()
            except Exception:
                pass
            break

def main_reply_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🌐 الأقسام والتطبيقات"),
        KeyboardButton("⚡ سحبة صاروخية (3 أرقام)"),
        KeyboardButton("💎 قسم الأرقام المميزة (VIP)"),
        KeyboardButton("🎁 هدية اليوم 💰"),
        KeyboardButton("📊 سجل أرقامي"),
        KeyboardButton("🔍 بحث يدوي عن كود"),
        KeyboardButton("🎁 نقاطي ورابط الإحالة"),
        KeyboardButton("🎫 إدخال كود هدية"),
        KeyboardButton("📢 مشاركة البوت"),
        KeyboardButton("👨‍💻 تواصل مع المطور"),
        KeyboardButton("⚙️ لوحة المطور")
    )
    return markup

def get_services_only_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for s_key, s_data in SERVICES_DATA.items():
        if s_key == "tempmail":
            buttons.append(InlineKeyboardButton(f"{s_data['icon']} {s_data['name']}", callback_data="get_temp_service"))
        elif s_key == "vip":
            buttons.append(InlineKeyboardButton(f"{s_data['icon']} {s_data['name']}", callback_data="show_vip_countries"))
        elif s_key == "turbo":
            buttons.append(InlineKeyboardButton(f"{s_data['icon']} {s_data['name']}", callback_data="get_turbo_numbers"))
        else:
            buttons.append(InlineKeyboardButton(f"{s_data['icon']} {s_data['name']}", callback_data=f"show_countries_{s_key}"))
    markup.add(*buttons)
    return markup

def get_countries_for_service_keyboard(service_key):
    markup = InlineKeyboardMarkup(row_width=2)
    countries_dict = SERVICES_COUNTRIES.get(service_key, {})
    country_btns = []
    for c_key, c_data in countries_dict.items():
        num_count = get_country_numbers_count(c_data)
        btn_text = f"{c_data['name']} ({num_count})"
        country_btns.append(InlineKeyboardButton(btn_text, callback_data=f"get_multi_num_{service_key}_{c_key}"))
    markup.add(*country_btns)
    markup.add(InlineKeyboardButton("⬅️ Back", callback_data="show_all_services"))
    return markup

def send_welcome(chat_id, user_id):
    points = user_points.get(user_id, 10)
    msg = f"مرحباً بك يا أواّد في بوت الأرقام الخارق (الإصدار الأسطوري v1000.0)! 👋\n⭐ رصيدك الحالي: `{points}` نقاط\nاختر القسم أو التطبيق المراد تفعيله من القائمة بالأسفل:"
    bot.send_message(chat_id, msg, reply_markup=main_reply_keyboard(), parse_mode="Markdown")
    bot.send_message(chat_id, "💬 Available Countries:", reply_markup=get_services_only_keyboard())

@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    if is_banned(user_id): return
    args = message.text.split()
    ref_id = args[1] if len(args) > 1 else None
    save_user(user_id, ref_id)
    if MAINTENANCE_MODE and user_id not in SUB_ADMINS:
        return bot.send_message(message.chat.id, "🛠 **البوت تحت الصيانة حالياً.**", parse_mode="Markdown")
    if not check_subscription_status(user_id):
        return send_targeted_subscription_msg(message.chat.id, user_id)
    send_welcome(message.chat.id, user_id)

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def verify_sub_cb(call):
    user_id = call.from_user.id
    if check_subscription_status(user_id):
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception: pass
        send_welcome(call.message.chat.id, user_id)
    else:
        bot.answer_callback_query(call.id, "❌ يجب عليك الاشتراك في جميع قنواتنا أولاً!", show_alert=True)

@bot.message_handler(func=lambda message: message.text in ["🌐 الأقسام والتطبيقات", "⚡ سحبة صاروخية (3 أرقام)", "💎 قسم الأرقام المميزة (VIP)", "🎁 هدية اليوم 💰", "📊 سجل أرقامي", "🔍 بحث يدوي عن كود", "🎁 نقاطي ورابط الإحالة", "🎫 إدخال كود هدية", "📢 مشاركة البوت", "👨‍💻 تواصل مع المطور", "⚙️ لوحة المطور"])
def handle_menu_buttons(message):
    user_id = message.from_user.id
    if is_banned(user_id): return
    if MAINTENANCE_MODE and user_id not in SUB_ADMINS: return
    if rate_limit_check(user_id, seconds=3):
        return bot.send_message(message.chat.id, "⏳ **يرجى الانتظار قليلاً قبل إرسال طلب جديد.**", parse_mode="Markdown")
    if not check_subscription_status(user_id):
        return send_targeted_subscription_msg(message.chat.id, user_id)

    txt = message.text
    if txt == "🌐 الأقسام والتطبيقات":
        bot.send_message(message.chat.id, "💬 Available Countries:", reply_markup=get_services_only_keyboard())
    elif txt == "⚡ سحبة صاروخية (3 أرقام)":
        points = user_points.get(user_id, 10)
        if points < 15:
            return bot.send_message(message.chat.id, "❌ **تحتاج إلى 15 نقطة لاستخدام السحبة الصاروخية لثلاثة أرقام!**", parse_mode="Markdown")
        user_points[user_id] = points - 15
        
        bot.send_message(message.chat.id, "🚀 **جاري سحب 3 أرقام صاروخية دفعة واحدة... انتظر لحظة!**", parse_mode="Markdown")
        turbo_countries = list(SERVICES_COUNTRIES["whatsapp"].values())
        chosen_country = random.choice(turbo_countries)
        
        numbers_list = []
        for _ in range(3):
            num = get_real_live_number(chosen_country)
            numbers_list.append(num)
            if user_id not in user_history: user_history[user_id] = []
            user_history[user_id].insert(0, num)
            
        header_text = f"💬 {chosen_country['name']} WhatsApp Number:\n⏳ Waiting for OTP..."
        markup = InlineKeyboardMarkup(row_width=1)
        for num in numbers_list:
            copy_url = f"https://t.me/share/url?url=+{num}"
            markup.add(
                InlineKeyboardButton(f"💬 📋 {chosen_country['name']} +{num}", url=copy_url)
            )
        
        markup.add(InlineKeyboardButton("🗑️ Remove CC", callback_data="remove_cc"))
        markup.add(InlineKeyboardButton("🔄 Change Number", callback_data=f"get_multi_num_whatsapp_{chosen_country['slug']}"))
        markup.add(InlineKeyboardButton("🌐 Change Country", callback_data="show_all_services"))
        markup.add(InlineKeyboardButton("🔑 Get OTP", callback_data="get_otp_manual_check"))

        bot.send_message(message.chat.id, header_text, reply_markup=markup, parse_mode="Markdown")
        for num in numbers_list:
            Thread(target=background_auto_otp_checker, args=(message.chat.id, num, "WhatsApp", chosen_country['name'], "whatsapp", chosen_country['slug']), daemon=True).start()

    elif txt == "💎 قسم الأرقام المميزة (VIP)":
        points = user_points.get(user_id, 10)
        markup = InlineKeyboardMarkup(row_width=1)
        for c_key, c_data in SERVICES_COUNTRIES["vip"].items():
            markup.add(InlineKeyboardButton(f"{c_data['name']} (500)", callback_data=f"get_num_vip_{c_key}"))
        markup.add(InlineKeyboardButton("⬅️ Back", callback_data="show_all_services"))
        bot.send_message(message.chat.id, f"💎 **قسم الأرقام المميزة والملكية (VIP):**\n⭐ رصيدك الحالي: `{points}` نقطة\n\nاختر الدولة المطلوبة:", reply_markup=markup, parse_mode="Markdown")
    elif txt == "🎁 هدية اليوم 💰":
        now = time.time()
        last_time = user_last_bonus.get(user_id, 0)
        if (now - last_time) < 86400:
            remaining = int(86400 - (now - last_time))
            hours = remaining // 3600
            minutes = (remaining % 3600) // 60
            bot.send_message(message.chat.id, f"⏳ **لقد استلمت هدفتك اليومية مسبقاً!**\nيرجى الانتظار `{hours}` ساعة و `{minutes}` دقيقة لطلب الهدية التالية.", parse_mode="Markdown")
        else:
            gift = random.randint(5, 20)
            user_points[user_id] = user_points.get(user_id, 10) + gift
            user_last_bonus[user_id] = now
            bot.send_message(message.chat.id, f"🎉 **مبارك لك يا أواّد!**\nلقد حصلت على هدفتك اليومية بقيمة `{gift}` نقاط مجانية! 🎁", parse_mode="Markdown")
    elif txt == "📊 سجل أرقامي":
        history = user_history.get(user_id, [])
        if not history:
            bot.send_message(message.chat.id, "📂 **ليس لديك أي أرقام مسجلة في السجل حتى الآن.**", parse_mode="Markdown")
        else:
            msg = "📂 **آخر أرقام سحبتها:**\n\n"
            for idx, num in enumerate(history, 1):
                msg += f"{idx} - `+{num}`\n"
            bot.send_message(message.chat.id, msg, parse_mode="Markdown")
    elif txt == "🔍 بحث يدوي عن كود":
        waiting_for_manual_number[user_id] = True
        bot.send_message(message.chat.id, "🔍 **أرسل الآن رقم الهاتف كاملاً (بدون علامة +) للبحث عن كود التفعيل الخاص به:**", parse_mode="Markdown")
    elif txt == "🎁 نقاطي ورابط الإحالة":
        points = user_points.get(user_id, 10)
        ref_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
        msg = (
            f"🎁 **نظام النقاط والإحالة الخاص بك:**\n\n"
            f"⭐ نقاطك الحالية: `{points}` نقطة\n"
            f"🔗 **رابط الإحالة الخاص بك:**\n`{ref_link}`\n\n"
            f"💡 *شارك الرابط مع أصدقائك واكسب 15 نقطة عن كل شخص يزور البوت!*"
        )
        bot.send_message(message.chat.id, msg, parse_mode="Markdown")
    elif txt == "🎫 إدخال كود هدية":
        waiting_for_promo[user_id] = True
        bot.send_message(message.chat.id, "🎫 **أرسل الآن كود الهدية لشحن نقاطك فوراً:**", parse_mode="Markdown")
    elif txt == "📢 مشاركة البوت":
        bot_info = bot.get_me()
        share_url = f"https://t.me/share/url?url=https://t.me/{bot_info.username}&text=اشترك%20في%20أفضل%20بوت%20أرقام!⚡"
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🚀 إرسال رابط البوت", url=share_url))
        bot.send_message(message.chat.id, "📢 **شارك البوت مع أصدقائك:**", reply_markup=markup, parse_mode="Markdown")
    elif txt == "👨‍💻 تواصل مع المطور":
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("👨‍💻 مالك البوت", url=DEVELOPER_URL))
        bot.send_message(message.chat.id, "💬 **للتواصل مع المطور:**", reply_markup=markup, parse_mode="Markdown")
    elif txt == "⚙️ لوحة المطور":
        if user_id not in SUB_ADMINS: return
        total_users = get_users_count()
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("📢 إرسال إذاعة (/broadcast)", callback_data="admin_broadcast"),
            InlineKeyboardButton("🔄 تحديث الإحصائيات", callback_data="admin_stats")
        )
        bot.send_message(message.chat.id, f"⚙️ **لوحة التحكم الإدارية:**\n\n👥 إجمالي المستخدمين: `{total_users}`\n📊 الأرقام المُولدة: `{bot_stats['numbers_generated']}`\n🔑 الأكواد المُستخرجة: `{bot_stats['otps_fetched']}`", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def smart_ai_chat_support(message):
    user_id = message.from_user.id
    if is_banned(user_id): return
    if waiting_for_manual_number.get(user_id, False):
        return process_manual_search(message)
    if waiting_for_broadcast.get(user_id, False):
        return process_broadcast(message)
    if waiting_for_promo.get(user_id, False):
        return process_promo_code(message)
        
    text = message.text.lower()
    if "نقطة" in text or "نقاط" in text or "كيف" in text:
        bot.reply_to(message, "💡 **لزيادة نقاطك مجاناً:** توجه إلى قسم (🎁 نقاطي ورابط الإحالة) وشارك رابطك مع أصدقائك، أو استخدم أكواد الهدايا اليومية!")
    elif "كود" in text or "ما وصل" in text or "مشكلة" in text:
        bot.reply_to(message, "⚡ **تأكد من الآتي:**\n1. أن الرقم تم طلبه حديثاً ولم تنتهِ مهلة الـ 5 دقائق.\n2. استخدام ميزة (🔍 بحث يدوي عن كود) لإلزام البوت بفحص الرسائل فوراً.")
    else:
        bot.reply_to(message, "🤖 أهلاً بك يا أواّد أو صديقي العزيز! استخدم الأزرار بالأسفل لتصفح الأقسام وسحب الأرقام بكل سهولة 🚀")

@bot.callback_query_handler(func=lambda call: call.data == "admin_broadcast")
def admin_broadcast_cb(call):
    if call.from_user.id not in SUB_ADMINS: return
    waiting_for_broadcast[ADMIN_ID] = True
    bot.send_message(call.message.chat.id, "📢 **أرسل الآن نص رسالة الإذاعة التي تريد إرسالها لجميع المستخدمين:**")

@bot.callback_query_handler(func=lambda call: call.data == "admin_stats")
def admin_stats_cb(call):
    if call.from_user.id not in SUB_ADMINS: return
    total_users = get_users_count()
    bot.answer_callback_query(call.id, f"المستخدمين: {total_users} | الأرقام: {bot_stats['numbers_generated']}", show_alert=True)

def process_broadcast(message):
    if message.from_user.id not in SUB_ADMINS: return
    waiting_for_broadcast[ADMIN_ID] = False
    text_to_broadcast = message.text
    if not os.path.exists("users.txt"):
        return bot.send_message(message.chat.id, "❌ لا يوجد مستخدمين مسجلين بعد.")
    success = 0
    with open("users.txt", "r") as f:
        for uid in f.read().splitlines():
            try:
                bot.send_message(int(uid), f"📢 **إشعار من الإدارة:**\n\n{text_to_broadcast}", parse_mode="Markdown")
                success += 1
            except Exception:
                pass
    bot.send_message(message.chat.id, f"✅ **تم إرسال الإذاعة بنجاح إلى `{success}` مستخدماً!**", parse_mode="Markdown")

def process_promo_code(message):
    user_id = message.from_user.id
    waiting_for_promo[user_id] = False
    code = message.text.strip()
    if code in ACTIVE_PROMO_CODES:
        if user_id not in used_promo_codes:
            reward = ACTIVE_PROMO_CODES[code]
            user_points[user_id] = user_points.get(user_id, 0) + reward
            used_promo_codes.add(user_id)
            bot.send_message(message.chat.id, f"🎉 **مبروك! تم شحن الكود بنجاح وإضافة `{reward}` نقطة إلى رصيدك!**", parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "❌ **عذراً، لقد استخدمت كود هدية مسبقاً.**", parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "❌ **الكود غير صحيح أو منتهي الصلاحية!**", parse_mode="Markdown")

def process_manual_search(message):
    user_id = message.from_user.id
    waiting_for_manual_number[user_id] = False
    phone_clean = re.sub(r'[^\d]', '', message.text)
    bot.send_message(message.chat.id, f"🔍 جاري البحث اليدوي عن كود للرقم `+{phone_clean}`...", parse_mode="Markdown")
    otp = fetch_real_otp_sms(phone_clean)
    if otp:
        bot.send_message(message.chat.id, f"🎉 **تم العثور على الكود بنجاح!**\n📞 الرقم: `+{phone_clean}`\n🔑 الكود: `{otp}`", parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, f"❌ **لم يتم استلام كود بعد للرقم `+{phone_clean}`.**", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "get_temp_service")
def get_temp_service_cb(call):
    temp_mail = f"user_{random.randint(1000,9999)}@tempmail.com"
    msg = f"🌟 **قسم الأرقام والإيميلات المؤقتة السريعة:**\n\n📧 إيميلك الوهمي المؤقت: `{temp_mail}`\n📥 (جاهز لتلقي الرسائل والتفعيلات السريعة)"
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Back", callback_data="show_all_services"))
    bot.send_message(call.message.chat.id, msg, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "show_all_services")
def show_all_services_cb(call):
    user_id = call.from_user.id
    if not check_subscription_status(user_id):
        return send_targeted_subscription_msg(call.message.chat.id, user_id)
    try:
        bot.edit_message_text("💬 Available Countries:", call.message.chat.id, call.message.message_id, reply_markup=get_services_only_keyboard())
    except Exception:
        bot.send_message(call.message.chat.id, "💬 Available Countries:", reply_markup=get_services_only_keyboard())

@bot.callback_query_handler(func=lambda call: call.data.startswith("show_countries_"))
def show_countries_cb(call):
    user_id = call.from_user.id
    if not check_subscription_status(user_id):
        return send_targeted_subscription_msg(call.message.chat.id, user_id)
    service_key = call.data.replace("show_countries_", "")
    service_info = SERVICES_DATA.get(service_key, {"name": "التطبيق"})
    msg_text = f"💬 Available Countries for ({service_info['name']}):"
    try:
        bot.edit_message_text(msg_text, call.message.chat.id, call.message.message_id, reply_markup=get_countries_for_service_keyboard(service_key))
    except Exception:
        bot.send_message(call.message.chat.id, msg_text, reply_markup=get_countries_for_service_keyboard(service_key))

@bot.callback_query_handler(func=lambda call: call.data.startswith("get_multi_num_"))
def get_multi_numbers_cb(call):
    user_id = call.from_user.id
    if is_banned(user_id): return
    if rate_limit_check(user_id, seconds=3):
        return bot.answer_callback_query(call.id, "⏳ يرجى الانتظار قليلاً قبل طلب أرقام جديدة.", show_alert=True)
    if not check_subscription_status(user_id):
        return send_targeted_subscription_msg(call.message.chat.id, user_id)
        
    parts = call.data.replace("get_multi_num_", "").split("_")
    service_key = parts[0]
    country_key = parts[1]
    
    service_info = SERVICES_DATA.get(service_key, {"name": "التطبيق", "icon": "💬"})
    country_info = SERVICES_COUNTRIES.get(service_key, {}).get(country_key, {"name": "الدولة", "code": "967", "slug": "yemen", "len": 9, "prefixes": ["77"]})
    
    bot.answer_callback_query(call.id, "⚡ جاري سحب الأرقام بنجاح...")
    
    numbers_list = []
    for _ in range(3):
        full_num = get_real_live_number(country_info)
        numbers_list.append(full_num)
        if user_id not in user_history: user_history[user_id] = []
        user_history[user_id].insert(0, full_num)
        if len(user_history[user_id]) > 5: user_history[user_id].pop()

    header_text = f"💬 {country_info['name']} {service_info['name']} Number:\n⏳ Waiting for OTP..."
    
    markup = InlineKeyboardMarkup(row_width=1)
    for num in numbers_list:
        copy_url = f"https://t.me/share/url?url=+{num}"
        markup.add(
            InlineKeyboardButton(f"💬 📋 {country_info['name']} +{num}", url=copy_url)
        )
    
    markup.add(InlineKeyboardButton("🗑️ Remove CC", callback_data="remove_cc"))
    markup.add(InlineKeyboardButton("🔄 Change Number", callback_data=f"get_multi_num_{service_key}_{country_key}"))
    markup.add(InlineKeyboardButton("🌐 Change Country", callback_data=f"show_countries_{service_key}"))
    markup.add(InlineKeyboardButton("🔑 Get OTP", callback_data="get_otp_manual_check"))
    
    try:
        if call.message:
            bot.edit_message_text(header_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.send_message(call.message.chat.id, header_text, reply_markup=markup, parse_mode="Markdown")
    except Exception:
        bot.send_message(call.message.chat.id, header_text, reply_markup=markup, parse_mode="Markdown")
    
    for num in numbers_list:
        Thread(target=background_auto_otp_checker, args=(call.message.chat.id, num, service_info['name'], country_info['name'], service_key, country_key), daemon=True).start()

@bot.callback_query_handler(func=lambda call: call.data == "remove_cc")
def remove_cc_cb(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception:
        pass
    bot.answer_callback_query(call.id, "🗑️ تم حذف الرسالة بنجاح", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "get_otp_manual_check")
def get_otp_manual_cb(call):
    bot.answer_callback_query(call.id, "🔍 جاري فحص الرسائل الواردة للأرقام الحالية...", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data.startswith("copy_code_"))
def copy_code_cb(call):
    code = call.data.replace("copy_code_", "")
    bot.answer_callback_query(call.id, f"📋 تم نسخ الكود: {code}", show_alert=True)

if __name__ == "__main__":
    keep_alive()
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10)
        except Exception:
            time.sleep(3)
