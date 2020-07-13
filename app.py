from flask import Flask, request, render_template
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import re
import random

app = Flask(__name__)
bot = ChatBot('KarlMarx', storage_adapter="chatterbot.storage.SQLStorageAdapter", logic_adapters=[
        'chatterbot.logic.BestMatch',
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter'
    ])
# trainer = ListTrainer(bot)
# quotes = [re.findall(r'\d\.\s\“(.+)\”\s', line) for line in open('quotes_to_parse.txt')]
with open('quotes_to_parse.txt') as f:
    quotes = re.findall(r'\d\.\s\“(.+)\”\s', f.read())
# with open('transitional')

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
    random_quote = random.choice(quotes)
    lower_quote = random_quote[0].lower() + random_quote[1:]
    return f"{str(bot.get_response(user_input))}  By the way, {lower_quote}"


if __name__ == '__main__':
    app.run()
