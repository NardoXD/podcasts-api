from flask import Flask
from database import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
