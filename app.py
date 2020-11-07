import os
from logging.handlers import RotatingFileHandler

from flask import Flask, request, render_template
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import re
from logging.config import dictConfig
import random, logging

from logging.config import dictConfig

# dictConfig({
#     'version': 1,
#     'formatters': {'default': {
#         'format': '[%(asctime)s] %(levelname)s in %(module)s.%(funcName)s Line %(lineno)s: %(message)s',
#     }},
#     'handlers': {
#         'file': {
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': 'logs/admin.log',
#             'formatter': 'default',
#             'maxBytes': 10000,
#             'backupCount': 10,
#         },
#         'console': {
#             # 'level': 'INFO',
#             'formatter': 'default',
#             'class': 'logging.StreamHandler',
#             'stream': 'ext://sys.stdout',  # Default is stderr
#         },
#         'critical_mail_handler': {
#             'level': 'CRITICAL',
#             'formatter': 'default',
#             'class': 'logging.handlers.SMTPHandler',
#             'mailhost': ('mail.karlmarxindustries.com', 26),
#             'fromaddr': 'marxbot@karlmarxindustries.com',
#             'toaddrs': ['5042021062karlmarx@gmail.com'],
#             'credentials': ('marxbot@karlmarxindustries.com', 'LoggingHandler'),
#             'subject': 'Critical error with application name'
#         }
#     },
#     'root': {
#         'level': 'DEBUG',
#         'handlers': ['file', 'console', 'critical_mail_handler']
#     }
#
# })

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


if __name__ == '__main__':
    # handler = RotatingFileHandler('error.log', maxBytes=1000, backupCount=20)
    # formatter = logging.Formatter('%(asctime)s [%(levelname)s:%(lineno)d] %(name)s: %(message)s')
    # handler.setFormatter(formatter)
    # handler.setLevel(logging.DEBUG)
    # app.logger.addHandler(handler)
    # log = logging.getLogger('werkzeug')
    # log.setLevel(logging.DEBUG)
    # log.addHandler(handler)
    #
    app.run()
