from flask import Flask
from presentation.controllers import sensor_bp, weather_bp, orchestrator_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(sensor_bp)
    app.register_blueprint(weather_bp)
    app.register_blueprint(orchestrator_bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)