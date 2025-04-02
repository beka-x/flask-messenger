from flask import Flask, render_template_string
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app)

# Главная страница, которая будет отображать чат
@app.route('/')
def index():
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Чат</title>
            <script src="https://cdn.socket.io/4.5.0/socket.io.min.js"></script>
            <style>
                body {
                    font-family: Arial, sans-serif;
                }
                #messages {
                    max-height: 400px;
                    overflow-y: scroll;
                    border: 1px solid #ccc;
                    padding: 10px;
                }
                #message_input {
                    width: 80%;
                }
            </style>
        </head>
        <body>
            <h1>Мессенджер</h1>
            <div id="messages"></div>
            <input type="text" id="message_input" placeholder="Введите сообщение..." autocomplete="off">
            <button onclick="sendMessage()">Отправить</button>

            <script>
                // Создаем подключение к серверу
                var socket = io.connect('http://' + document.domain + ':' + location.port);

                // Функция для отображения сообщений
                socket.on('message', function(msg) {
                    var messagesDiv = document.getElementById('messages');
                    var newMessage = document.createElement('div');
                    newMessage.textContent = msg;
                    messagesDiv.appendChild(newMessage);
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                });

                // Функция отправки сообщения
                function sendMessage() {
                    var messageInput = document.getElementById('message_input');
                    var message = messageInput.value;
                    if (message) {
                        socket.send(message);  // Отправка сообщения на сервер
                        messageInput.value = '';  // Очистить поле ввода
                    }
                }
            </script>
        </body>
        </html>
    """)

# Обработчик сообщений, которые будут передаваться всем участникам чата
@socketio.on('message')
def handle_message(msg):
    print('Received message: ' + msg)
    send(msg, broadcast=True)  # Отправить сообщение всем пользователям

# Запускаем сервер
if __name__ == '__main__':
    socketio.run(app, debug=True)
