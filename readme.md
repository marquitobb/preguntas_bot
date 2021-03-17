# Preguntas Bot

### tareas🔨

- [x]  crear una DB en clever-cloud (modo dev para mysql free)
- [x]  crear las tablas que usaran junto con sus campos
    - [x]  encuesta
        - [x]  pregunta
        - [x]  respuesta_cerrada (bolean)
        - [x]  respuesta a)
        - [x]  respuesta b)
        - [x]  respuesta c)
- [x]  crear un registrar preguntas
    - [x]  usar un template de bootstrap
- [x]  crear y conectar el bot de telegram para hacer pruebas


### como usar🤔

1. debemos mandar un mensaje **/start** para activar la conversacion con telegram al bot `@preguntados_prueba_bot`
2. si queremos crear mas preguntas ir al [https://preguntasbot.herokuapp.com/preguntas](https://preguntasbot.herokuapp.com/preguntas)
3. para activar las preguntas solo es escribir **Preguntame** al bot
4. te hara la pregunta la cual tu debes de escribir la respuesta que pienses que es la correcta

### bugs 🐞

- dure mucho tiempo configurando el webhook
- comence hasta que me desocupe y me falto dedicarle mas
- utilize varias librerias pero justo esta fallando sqlAlchemy en la version mayor a 1.4
- para no durar mas de 3 horas solo agregue preguntas cerradas y no de opcion multiple