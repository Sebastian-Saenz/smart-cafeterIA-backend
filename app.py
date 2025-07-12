from flask import Flask, jsonify
from config import Config
from extensions import test_PostgreSQL, test_Elasticsearch, test_Pool
from routes.client import client_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(client_bp, url_prefix="/client")

    @app.route("/")
    def index():
        return jsonify({"status": "Backend is running..."})

    return app


if __name__ == "__main__":
    app = create_app()
    # Testeando conexiones al iniciar app
    config = Config()
    test_PostgreSQL()
    test_Elasticsearch()
    test_Pool()
    app.run(host="0.0.0.0", port=8080)
