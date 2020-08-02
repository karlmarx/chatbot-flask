from flask import Flask, request, render_template
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import re
import logging
import random

app = Flask(__name__)
app.config["DEBUG"] = True
logging.basicConfig(level=logging.INFO, format='%(asctime)s =%(levelname)s - %(message)s', handlers=[
    logging.FileHandler("log.log")
])
bot = ChatBot('KarlMarx', storage_adapter="chatterbot.storage.SQLStorageAdapter", logic_adapters=[
        'chatterbot.logic.BestMatch'],
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer')
# trainer = ListTrainer(bot)
with open('quotes_to_parse.txt') as f:
    quotes = re.findall(r'\d\.\s\“(.+)\”\s', f.read())
with open('transitional_phrases.txt') as f:
    transitions = f.readlines()

# trainer.train(['What is your name?', 'My name is KarlMarx'])
# trainer.train(['Who are you?', 'I am a communist bot.'])

c_trainer = ChatterBotCorpusTrainer(bot, show_training_progress=False)

c_trainer.train(
    "chatterbot.corpus.english"
)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/get")
def get_response():
    user_input = request.args.get('msg')
    app.logger.info(f"MSG RECEIVED: {user_input} ")

    transition = random.choice(transitions)
    random_quote = random.choice(quotes).strip()
    if not (re.match('^I\s', random_quote)):
        random_quote = random_quote[0].lower() + random_quote[1:]

    bot_response = str(bot.get_response(user_input)).strip()
    if not (re.match(r'.+[.?]', bot_response)):
        bot_response = bot_response + "."

    final_response = f"{bot_response} {transition} {random_quote}"
    app.logger.info(f"FORMATTED RESPONSE: {final_response}")
    return final_response

if __name__ == '__main__':
    app.run()
