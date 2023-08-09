def hello_world():
    return {"id": 4}, 200
from flask import Flask

app = Flask(__name__)
app.add_url_rule("/", view_func=hello_world)


