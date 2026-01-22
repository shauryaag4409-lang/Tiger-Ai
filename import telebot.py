import telebot
import google.generativeai as genai

# CONFIGURATION
TELEGRAM_TOKEN = "8205626911:AAHeAvMTuA82M2CbKht7LVne2n6Ya-p8xjo"
GEMINI_API_KEY = "AIzaSyBsMW-0vRjD_2XIntuf3fZyCW4HvvgFN_Q"

# Initialize AI and Bot
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# The "Ultra Elite" Brain Instructions
SYSTEM_PROMPT = """
You are the Ultra_Elite_AI_Trading_Analysis_and_Simulation_System v2.0.
Strictly analyze 5m and 15m timeframes only. 
Never give financial advice. 
If an image is sent, analyze patterns like Hammer, Engulfing, or W/M patterns.
Provide Confidence Scores (0-100%).
"""

@bot.message_handler(content_types=['text', 'photo'])
def handle_message(message):
    try:
        if message.content_type == 'text':
            response = model.generate_content(f"{SYSTEM_PROMPT}\nUser Input: {message.text}")
            bot.reply_to(message, response.text)
        
        elif message.content_type == 'photo':
            # Download the image
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            # Analyze image with AI
            img_data = [{'mime_type': 'image/jpeg', 'data': downloaded_file}]
            response = model.generate_content([SYSTEM_PROMPT, img_data[0]])
            bot.reply_to(message, response.text)
            
    except Exception as e:
        bot.reply_to(message, "Error processing analysis. Ensure timeframe is 5m or 15m.")

bot.infinity_polling()