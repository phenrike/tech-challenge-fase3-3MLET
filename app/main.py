from flask import Flask
from presentation.controllers import sensor_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(sensor_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)