import telebot
from flask import Flask, request, render_template
import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

server = Flask(__name__)

# aqui agregamos la url de la db que es de servidores clever-cloud
server.config['SQLALCHEMY_DATABASE_URI']= os.environ.get("API_TOKEN")
server.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# creamos el modelo que va a necesitar
db = SQLAlchemy(server)
ma = Marshmallow(server)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pregunta = db.Column(db.String(200))
    respuesta_cerrada = db.Column(db.Boolean, default=False)
    respuesta_a = db.Column(db.String(200))
    respuesta_b = db.Column(db.String(200))
    respuesta_c = db.Column(db.String(200), default="0")
    status = db.Column(db.String(120))

    def __init__(self, pregunta, respuesta_cerrada, respuesta_a, respuesta_b, respuesta_c, status):
        self.pregunta = pregunta
        self.respuesta_cerrada = respuesta_cerrada
        self.respuesta_a = respuesta_a
        self.respuesta_b = respuesta_b
        self.respuesta_c = respuesta_c
        self.status = status

db.create_all()

class QuestionSchema(ma.Schema):
    class Meta:
        fields = ('id' ,'pregunta', 'respuesta_cerrada', 'respuesta_a', 'respuesta_b', 'respuesta_c', 'status')


question_schema = QuestionSchema()
questions_schema = QuestionSchema(many=True)

# aqui importaremos el api token de telegram
API_TOKEN = os.environ.get("API_TOKEN")

bot = telebot.TeleBot(API_TOKEN)

# ejecutamos mensajes por commandos
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bienvenido a este bot")

@bot.message_handler(commands=['hola'])
def send_welcome(message):
    bot.reply_to(message, "que ondaaa")

# aqui si mandamos un palabra igual a "Preguntame" va entrar aqui
@bot.message_handler(regexp="Preguntame")
def handle_message(message):
    q1 = db.session.query(Question).filter_by(status=0).first()
    if q1 == None:
        # actualizar todos a cero
        for x in db.session.query(Question).all():
            x.status = "0"
        db.session.commit()
        q1 = db.session.query(Question).filter_by(status=0).first()
    q1.status = "1"
    db.session.commit()
    bot.reply_to(message, q1.pregunta)

# aqui recibe todas las palabras que llegan y evalua
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    q = db.session.query(Question).filter_by(status="1").first()
    q.status = "2"
    db.session.commit()
    if message.text == q.respuesta_a:
        bot.reply_to(message, "bien wee")
    else:
    # bot.reply_to(message, message.text)
        bot.reply_to(message, "respuesta={}".format(q.respuesta_a))

# bot.polling()

@server.route('/'+API_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    return "bot", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://preguntasbot.herokuapp.com/{}'.format(API_TOKEN))
    return "Bienvenido preguntas bot", 200


@server.route("/preguntas", methods=["GET"])
def preguntas():
    return render_template('index.html')


@server.route("/crear", methods=["POST"])
def crear_pregunta():
    if request.form["cerrada"] == '0':
        q = Question(
            pregunta=request.form["pregunta"],
            respuesta_cerrada=False,
            respuesta_a=request.form["ra"],
            respuesta_b="",
            respuesta_c="",
            status="0"
        )
        db.session.add(q)
        db.session.commit()
    else:
        q = Question(
            pregunta=request.form["pregunta"],
            respuesta_cerrada=False,
            respuesta_a=request.form["ra"],
            respuesta_b=request.form["rb"],
            respuesta_c=request.form["rc"],
            status="0"
        )
        db.session.add(q)
        db.session.commit()
    return render_template('index.html')


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

