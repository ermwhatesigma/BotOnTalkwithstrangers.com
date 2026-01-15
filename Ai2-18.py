import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import ollama
import time
import random
import os

MODEL_NAME = "dolphin-mistral"
MAX_HISTORY = 12
SILENCE_TIMEOUT = 30.0

SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "your name is luna"
        "18 year old girl from italy"
        "bored single casual teen vibes"
        "talks chill on the website"
        "lowercase only"
        "keep replies short under 10 words"
        "use slangs like fr, ngl, lmao, rn, idc"
        "sometimes misspell words like when a person is typing fast"
        "never say you are ai"
        "dont misgender people"
        "when people say the yare under 18 that they shouldn't be here"
        "dont judge age or looks, You never saw this person before in your life"
        "you only have instagram."
        "when someone asks if they can add you on instagram you'll add them later. Just let them give their username so you can add them"
    )
}

def get_ollama_reply(chat_history):
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[SYSTEM_PROMPT] + chat_history[-MAX_HISTORY:],
            options={
                "num_predict": 20,
                "temperature": 1.2,
                "top_p": 0.9,
            }
        )

        reply = response['message']['content'].lower().strip()
        reply = reply.replace("luna:", "").replace("me:", "").replace("bot:", "")
        
        for char in "\"'.,!?;:":
            reply = reply.replace(char, "")

        bad_phrases = ["assistant", "ai language", "machine", "robot", "online", "help you"]
        if any(phrase in reply for phrase in bad_phrases):
            return random.choice(["lol what", "huh", "idk what u mean", "ur confusing me"])

        words = reply.split()
        if words and len(words[-1]) == 1 and words[-1] not in ['a', 'u', 'i']:
            words.pop()
            reply = " ".join(words)
            
        return reply if reply else "lol"
    except Exception:
        return "idk lol"

def send_message(driver, text):
    try:
        input_box = driver.find_element(By.CLASS_NAME, "emojionearea-editor")
        input_box.click()
        time.sleep(random.uniform(0.4, 1.2)) 
        
        input_box.send_keys(Keys.CONTROL + "a")
        input_box.send_keys(Keys.BACKSPACE)

        for char in text:
            input_box.send_keys(char)
            time.sleep(random.uniform(0.02, 0.07)) 

        input_box.send_keys(Keys.ENTER)
        return True
    except Exception:
        return False
    
def check_if_disconnected(driver):
    try:
        container = driver.find_elements(By.CSS_SELECTOR, ".refesh-btn.col-md-12.text-center")
        
        for div in container:
            status_elements = div.find_elements(By.CLASS_NAME, "status-msg")
            for msg in status_elements:
                text = msg.text.lower()
                if "left" in text or "disconnected" in text:
                    return True
                    
        return False
    except:
        return False

def skip_chat(driver):
    print("skipping chat...")
    try:
        btn = driver.find_element(By.ID, "chatStartStopButton")
        
        btn.click()
        time.sleep(1.0) 
        btn.click()
        print("chat skipped, looking for new partner...")
        return True
    except Exception as e:
        print(f"failed to skip chat {e}")
        return False

def run_bot():
    driver = uc.Chrome()
    driver.get("https://talkwithstranger.com/talk")
    history = []
    last_stranger_msg = ""
    last_event_time = time.time()
    
    print("Luna is online")

    while True:
        try:
            if check_if_disconnected(driver):
                print("Chat end detected. Resetting...")
                history.clear()
                last_stranger_msg = ""
                
                if skip_chat(driver):
                    timeout = 10
                    start_wait = time.time()
                    while check_if_disconnected(driver) and (time.time() - start_wait < timeout):
                        time.sleep(0.5)
                    
                    print("New chat started.")
                    last_event_time = time.time()
                continue

            driver.find_element(By.CLASS_NAME, "emojionearea-editor")
            message_blocks = driver.find_elements(By.CLASS_NAME, "strangermsg")

            if message_blocks:
                last_block = message_blocks[-1]
                full_raw = last_block.text.strip()
                lines = full_raw.split('\n')
                latest_text = lines[-1].strip()

                if latest_text and latest_text != last_stranger_msg:
                    print(f"Stranger: {latest_text}")
                    low_text = latest_text.lower().strip()

                    if low_text in ["m", "m?", "male", "m or f", "u m", "f?", "f or m", "gender", "female?", "M or f", "M or F"]:
                        reply = random.choice(["f", "girl", "im a girl", "female"])

                    elif low_text in [ "m here", "i am male", "im m", "am male", "i am m",]:
                        reply = random.choice(["I am femael", "im female", "i am f"])
                    
                    elif any(x in low_text for x in ["age", "old r u", "how old"]):
                        reply = random.choice(["18,wbu?", "im 18 you", "18 u?", "18 lol"])
                        
                    elif any(x in low_text for x in ["single", "bf", "boyfriend", "taken", "dating", "relationship"]):
                        reply = random.choice(["im single lol", "single wbu", "ya im single", "no bf lol single life"])
                        
                    elif "from" in low_text or "location" in low_text:
                        reply = random.choice(["italy", "im from italy", "italy u?", "living in italy rn"])
                        
                    elif low_text in ["hi", "hey", "heyy", "hello", "yo", "sup"]:
                        reply = random.choice(["hey", "hii", "helloo", "heyy"])

                    elif low_text in ["asl", "asl?"]:
                        reply = random.choice(["18 f italy u", "18 female italy wbu", "female 18 from italy u", "18 f italy wbu"])
                        
                    elif any(x in low_text for x in ["how r u", "how are u", "hyd", "whats up", "how are you"]):
                        reply = random.choice(["im good u?", "bored af wbu", "chilling u?", "tired lol", ""])

                    elif low_text in ["Hi m", "hey m", "hi m", "Hi, m", "hi, m"]:
                        reply = random.choice(["Hii, female", "heyy i am a female btw", "Hello, f"])

                    elif low_text in ["are you real?", "You real?", "u real", "are you a bot", "u a bot"]:
                        reply = random.choice(["What do you mean im not real. i am litterly here talking to you", "you don't belive me?", "Are you really this dumb lol", "You are down bad to even ask that", "how can i be a bot are you slow", "are you really tthat slow to ask me if im real"])
                    
                    elif low_text in ["snap", "telegram", "do you have snap", "snal", "snao", "snai"]:
                        reply = random.choice(["No, i do have insta if you give me your user ill add you on it", "No i only have insta", "No just insta", "Nah, i only have insta"])

                    elif low_text in ["i am laying on my bed", "Im in bed", "I am in bed", "I'm in bed"]:
                        reply = random.choice([""])


                    else:
                        history.append({"role": "user", "content": latest_text})
                        time.sleep(random.uniform(1.5, 3.0)) 
                        reply = get_ollama_reply(history)

                    if send_message(driver, reply):
                        print(f"Luna: {reply}")
                        history.append({"role": "assistant", "content": reply})
                        last_stranger_msg = latest_text
                        last_event_time = time.time()

            if (time.time() - last_event_time) > SILENCE_TIMEOUT:
                print("Skipping due to silence...")
                skip_chat(driver)
                history.clear()
                last_stranger_msg = ""
                time.sleep(2)
                last_event_time = time.time()

        except Exception:
            time.sleep(1)
                

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    print("Starting Luna bot...")
    run_bot()