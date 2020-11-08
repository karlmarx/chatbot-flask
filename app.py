import os
from logging.handlers import RotatingFileHandler

import google.cloud.logging
from flask import Flask, request, render_template
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import re
from logging.config import dictConfig
import random, logging
from google.cloud.logging.handlers import CloudLoggingHandler

from logging.config import dictConfig

client = google.cloud.logging.Client()
handler = CloudLoggingHandler(client)
cloud_logger = logging.getLogger()
cloud_logger.addHandler(handler)

app = Flask(__name__)
# app.config["DEBUG"] = True

# logging.basicConfig(level=logging.INFO, format=, handlers=[
#     logging.FileHandler("log.log")
# ])
db_user = os.environ["DB_USER"]
db_pass = os.environ["DB_PASS"]
db_name = os.environ["DB_NAME"]
db_host = os.environ["DB_HOST"]

db = f"mongodb+srv://{db_user}:{db_pass}@{db_host}/{db_name}?retryWrites=true&w=majority"
bot = ChatBot('KarlMarx', storage_adapter="chatterbot.storage.MongoDatabaseAdapter", logic_adapters=[
    'chatterbot.logic.BestMatch'],
              # trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
              database_uri=db)
# trainer = ListTrainer(bot)
with open('quotes_to_parse.txt') as f:
    quotes = re.findall(r'\d\.\s\“(.+)\”\s', f.read())
with open('transitional_phrases.txt') as f:
    transitions = f.readlines()


# trainer.train(['What is your name?', 'My name is KarlMarx'])
# trainer.train(['Who are you?', 'I am a communist bot.'])

# c_trainer = ChatterBotCorpusTrainer(bot, show_training_progress=False)
#
# c_trainer.train(
#     "chatterbot.corpus.english"
# )

@app.route('/')
def index():
    return render_template("index.html")


@app.route("/get")
def get_response():
    user_input = request.args.get('msg')
    app.logger.info(f"MSG RECEIVED: {user_input} ")
    cloud_logger.info(f"test MSG RECEIVED: {user_input} ")
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


@app.route("/error")
def error():
    app.logger.critical('testing')
    return "ok", 200


# if __name__ == '__main__':
#     # handler = RotatingFileHandler('error.log', maxBytes=1000, backupCount=20)
#     # formatter = logging.Formatter('%(asctime)s [%(levelname)s:%(lineno)d] %(name)s: %(message)s')
#     # handler.setFormatter(formatter)
#     # handler.setLevel(logging.DEBUG)
#     # app.logger.addHandler(handler)
#     # log = logging.getLogger('werkzeug')
#     # log.setLevel(logging.DEBUG)
#     # log.addHandler(handler)
#     #
#     app.run()

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
