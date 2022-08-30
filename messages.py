import random

def gen_text(time):
    if 22 < time or time < 4:
        text = "Wow, you are a night owl :sleeping:"
    elif 3 < time and time < 9:
        text = "Wow, you are an early bird :grinning:"
    else:
        text = "Report your work from here:"
    return text

def message_help():
    text =  ("Post 'b' or 'before' for report BEFORE working at the lab.\n"
             "Post 'a' or 'after' for report AFTER working at the lab.\n"
             "Post 'm' or 'mamber' to know who is in the lab.\n"
             "NOTICE: The time automatically filled in is the time you speak to the bot, so please correct it accordingly.\n"
             "NOTICE: The list of members in the room is based on the information collected by this bot, and may differ from the actual.\n"
             "For more detailes, read iic-lab scrapbox.")
   
    return text

def message_gpu():
    message_list = ["I'm not a gpu-bot.",
                    "gpu-bot is a good guy :sunglasses:",
                    "ask it to gpu-bot.",
                    "Is phoenix really immortal :thinking_face:",
                    "dlbox04 is waiting for your mug.",
                    "Only the chosen ones know what dlbox03 looks like.",
                    "*PHOENIX ONLY LIVE TWICE*"]

    num = random.randint(0, len(message_list)-1)
    return message_list[num]

def message_other():
    message_list = ["What are you talking about?",
                    "What the hell are you talking about?",
                    "Do not use difficult word.",
                    "Use words I can understand!",
                    "Sorry, I cannot understand.",
                    "I can only understand some word or galactic basic standard.",
                    "Sounds good, but this is not a form for a free-form haiku.",
                    "I think I'm getting used to this job."]

    num = random.randint(0, len(message_list)-1)
    return message_list[num]

def message_random():
    message_list = ["Hello again:exclamation:",
                    ":robot_face:Hi there:exclamation:",
                    ":robot_face::zzz::zzz:",
                    ":robot_face::zzz:",
                    ":zzz:",
                    "See you again:wave:",
                    "Hahaha...:rolling_on_the_floor_laughing:"]

    num = random.randint(0, len(message_list)-1)
    return message_list[num]

