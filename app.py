from flask import Flask, session
from routes.auth_routes import auth
from routes.task_routes import tasks_bp
from flask_cors import CORS

app = Flask(__name__)

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(tasks_bp, url_prefix='/api')

app.secret_key = "kj12b3i124b0dnas"

CORS(app)

if __name__ == "__main__":
    app.run(debug=True)