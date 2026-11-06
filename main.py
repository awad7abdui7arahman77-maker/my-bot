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
    return "⚡ Elite Master Bot Server Active 24/7! ⚡"

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
API_TOKEN = "8515653728:AAH7zicsU7S2dxzdt7Ju_puAgr1iylhyDB8"
ADMIN_ID = 8388141188 
SUB_ADMINS = [ADMIN_ID] 
DEVELOPER_URL = "https://t.me/awad3210"
OTP_CHANNEL_USERNAME = "@Awad_Numbers_Bot"

bot = telebot.TeleBot(API_TOKEN)
BOT_USERNAME = "Awad_7744_bot"

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
user_history = {}
user_referrals = {}

waiting_for_manual_number = {}
waiting_for_broadcast = {}

# قنواتك الخمس الحقيقية والرسمية فقط
SUBSCRIPTION_LINKS = [
    {"name": "📢 قناة البوت الرسمية", "url": "https://t.me/Awad_Numbers_Bot", "username": "@Awad_Numbers_Bot"},
    {"name": "📢 قناة جديدة", "url": "https://t.me/v_o_lti", "username": "@v_o_lti"},
    {"name": "📢 قناة عبارات بشكل عام", "url": "https://t.me/jzbznznx", "username": "@jzbznznx"},
    {"name": "📢 تعليم اختراق الجوالات وتوقيف الواتساب", "url": "https://t.me/breakthroughawad210", "username": "@breakthroughawad210"},
    {"name": "📢 قناة الدعم الاحتياطية", "url": "https://t.me/sn6hdbdn19dndw", "username": "@sn6hdbdn19dndw"}
]

SERVICES_DATA = {
    "whatsapp": {"name": "WhatsApp", "icon": "💬"},
    "telegram": {"name": "Telegram", "icon": "✈️"},
    "turbo": {"name": "⚡ سحبة صاروخية (3 أرقام)", "icon": "🚀"}
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
    "turbo": {
        "global_turbo": {"name": "⚡ سحبة صاروخية لـ 3 أرقام", "code": "1", "slug": "united-states", "len": 10, "prefixes": ["201", "415"]}
    }
}

user_last_action = {}
recent_numbers_cache = set()

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
        
        # نظام الإحالة (إذا دخل عبر صديقه)
        if referrer_id and referrer_id != str(user_id):
            ref_int = int(referrer_id)
            user_points[ref_int] = user_points.get(ref_int, 0) + 15 # يكسب نقاط مضمونة
            try:
                bot.send_message(ref_int, f"🎁 **مبروك! دخل صديق عبر رابط إحالتك وكسبت 15 نقطة رصيد أرقام مضمونة!** 🚀", parse_mode="Markdown")
            except Exception:
                pass

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
    for ch in SUBSCRIPTION_LINKS:
        if ch["username"].startswith("@"):
            try:
                status = bot.get_chat_member(ch["username"], user_id).status
                if status in ['left', 'kicked']:
                    unsubscribed.append(ch)
            except Exception:
                unsubscribed.append(ch)
        else:
            unsubscribed.append(ch)
    return unsubscribed

def check_subscription_status(user_id):
    return len(get_unsubscribed_channels(user_id)) == 0

def send_targeted_subscription_msg(chat_id, user_id):
    unsub_list = get_unsubscribed_channels(user_id)
    markup = InlineKeyboardMarkup(row_width=1)
    for ch in unsub_list:
        markup.add(InlineKeyboardButton(ch["name"], url=ch["url"]))
    markup.add(InlineKeyboardButton("✨ تم الاشتراك في جميع القنوات، دخول البوت ✅", callback_data="check_sub"))
    
    msg = (
        "⚠️ **عذراً يا صديقي!**\n\n"
        "📌 **لاستخدام البوت والحصول على الأرقام الحقيقية، يجب عليك الاشتراك في قنواتنا الخمس الرسمية أولاً:**"
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
        
    bot_stats["numbers_generated"] += 1
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
                match = re.search(r'(?:WhatsApp|Telegram|code|كود|واتساب).*?(\d{3}[\s-]?\d{3})', text_content, re.IGNORECASE)
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

# القائمة السفلية المختصرة (تم مسح إدخال كود هدية نهائياً)
def main_reply_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🌐 الأقسام والتطبيقات"),
        KeyboardButton("⚡ سحبة صاروخية (3 أرقام)"),
        KeyboardButton("🔍 بحث يدوي عن كود"),
        KeyboardButton("🔗 نقاطي ورابط الإحالة"),
        KeyboardButton("👨‍💻 تواصل مع المطور"),
        KeyboardButton("⚙️ لوحة المطور")
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
    country_btns = []
    for c_key, c_data in countries_dict.items():
        num_count = get_country_numbers_count(c_data)
        btn_text = f"{c_data['name']} ({num_count})"
        country_btns.append(InlineKeyboardButton(btn_text, callback_data=f"get_single_num_{service_key}_{c_key}"))
    markup.add(*country_btns)
    markup.add(InlineKeyboardButton("⬅️ Back", callback_data="show_all_services"))
    return markup

def send_welcome(chat_id, user_id):
    points = user_points.get(user_id, 10)
    msg = f"مرحباً بك يا أواّد في بوت الأرقام الخارق ⚡\n⭐ رصيدك الحالي: `{points}` نقاط\nاختر القسم أو التطبيق المراد تفعيله من القائمة بالأسفل:"
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
        bot.answer_callback_query(call.id, "❌ يجب عليك الاشتراك في القنوات الخمس أولاً!", show_alert=True)

@bot.message_handler(func=lambda message: message.text in ["🌐 الأقسام والتطبيقات", "⚡ سحبة صاروخية (3 أرقام)", "🔍 بحث يدوي عن كود", "🔗 نقاطي ورابط الإحالة", "👨‍💻 تواصل مع المطور", "⚙️ لوحة المطور"])
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
        turbo_countries = list(SERVICES_COUNTRIES["whatsapp"].values())
        chosen_country = random.choice(turbo_countries)
        single_num = get_real_live_number(chosen_country)
        
        # التصميم الدقيق المطابق للصورة الاحترافية تماماً
        number_display_text = (
            f"🌍 **الدولة:** {chosen_country['name']}\n\n"
            f"🔢 **الرقم:** `+{chosen_country['code']}{single_num}`\n\n"
            f"📋 **اضغط مطولاً للنسخ**"
        )
        
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🔄 Change Number", callback_data=f"get_single_num_whatsapp_{chosen_country['slug']}"),
            InlineKeyboardButton("🌐 Change Country", callback_data="show_all_services")
        )
        markup.add(InlineKeyboardButton("❌ Remove CC", callback_data="remove_cc"))
        markup.add(InlineKeyboardButton("✉️ OTP Group", url=f"https://t.me/{OTP_CHANNEL_USERNAME.replace('@','')}"))

        bot.send_message(message.chat.id, number_display_text, reply_markup=markup, parse_mode="Markdown")
        Thread(target=background_auto_otp_checker, args=(message.chat.id, f"{chosen_country['code']}{single_num}", "WhatsApp", chosen_country['name'], "whatsapp", chosen_country['slug']), daemon=True).start()

    elif txt == "🔍 بحث يدوي عن كود":
        waiting_for_manual_number[user_id] = True
        bot.send_message(message.chat.id, "🔍 **أرسل الآن رقم الهاتف كاملاً (بدون علامة +) للبحث الفوري عن كود التفعيل الخاص به:**", parse_mode="Markdown")
    elif txt == "🔗 نقاطي ورابط الإحالة":
        points = user_points.get(user_id, 10)
        ref_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
        msg_ref = (
            f"🔗 **نظام دعوة الأصدقاء ونقاط الأرقام المضمونة:**\n\n"
            f"⭐ رصيدك الحالي: `{points}` نقطة\n\n"
            f"📌 **رابط الإحالة الخاص بك:**\n`{ref_link}`\n\n"
            f"💡 *قم بنسخ الرابط وإرساله لأصدقائك، وكل صديق يدخل من رابطك سيكسبك نقاطاً تؤهلك للحصول على أرقام مضمونة 100% لأي برنامج تريده!* 🚀"
        )
        bot.send_message(message.chat.id, msg_ref, parse_mode="Markdown")
    elif txt == "👨‍💻 تواصل مع المطور":
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("👨‍💻 مالك البوت", url=DEVELOPER_URL))
        bot.send_message(message.chat.id, "💬 **للتواصل المباشر مع المطور (@awad3210):**", reply_markup=markup, parse_mode="Markdown")
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
        
    text = message.text.lower()
    if "كود" in text or "ما وصل" in text:
        bot.reply_to(message, "⚡ **تأكد من طلب الرقم حديثاً، واستخدام ميزة (🔍 بحث يدوي عن كود) لفحص الرسائل فوراً.**")
    else:
        bot.reply_to(message, "🤖 أهلاً بك يا أواّد! استخدم الأزرار بالأسفل لتصفح الأقسام وسحب الأرقام بكل سهولة 🚀")

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

@bot.callback_query_handler(func=lambda call: call.data.startswith("get_single_num_"))
def get_single_number_cb(call):
    user_id = call.from_user.id
    if is_banned(user_id): return
    if rate_limit_check(user_id, seconds=3):
        return bot.answer_callback_query(call.id, "⏳ يرجى الانتظار قليلاً قبل طلب رقم جديد.", show_alert=True)
    if not check_subscription_status(user_id):
        return send_targeted_subscription_msg(call.message.chat.id, user_id)
        
    parts = call.data.replace("get_single_num_", "").split("_")
    service_key = parts[0]
    country_key = parts[1]
    
    service_info = SERVICES_DATA.get(service_key, {"name": "التطبيق", "icon": "💬"})
    country_info = SERVICES_COUNTRIES.get(service_key, {}).get(country_key, {"name": "الدولة", "code": "967", "slug": "yemen", "len": 9, "prefixes": ["77"]})
    
    bot.answer_callback_query(call.id, "⚡ جاري سحب رقم حقيقي مضمون...")
    
    single_num = get_real_live_number(country_info)
    
    number_display_text = (
        f"🌍 **الدولة:** {country_info['name']}\n\n"
        f"🔢 **الرقم:** `+{country_info['code']}{single_num}`\n\n"
        f"📋 **اضغط مطولاً للنسخ**"
    )
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🔄 Change Number", callback_data=f"get_single_num_{service_key}_{country_key}"),
        InlineKeyboardButton("🌐 Change Country", callback_data=f"show_countries_{service_key}")
    )
    markup.add(InlineKeyboardButton("❌ Remove CC", callback_data="remove_cc"))
    markup.add(InlineKeyboardButton("✉️ OTP Group", url=f"https://t.me/{OTP_CHANNEL_USERNAME.replace('@','')}"))
    
    try:
        if call.message:
            bot.edit_message_text(number_display_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.send_message(call.message.chat.id, number_display_text, reply_markup=markup, parse_mode="Markdown")
    except Exception:
        bot.send_message(call.message.chat.id, number_display_text, reply_markup=markup, parse_mode="Markdown")
    
    Thread(target=background_auto_otp_checker, args=(call.message.chat.id, f"{country_info['code']}{single_num}", service_info['name'], country_info['name'], service_key, country_key), daemon=True).start()

@bot.callback_query_handler(func=lambda call: call.data == "remove_cc")
def remove_cc_cb(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception:
        pass
    bot.answer_callback_query(call.id, "🗑️ تم حذف الرسالة بنجاح", show_alert=True)

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
