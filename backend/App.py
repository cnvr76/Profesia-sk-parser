from flask import Flask
from flask_cors import CORS
import os
import dotenv

def create_app() -> Flask:
    dotenv.load_dotenv()

    app = Flask(__name__, 
                template_folder="./templates", 
                static_folder="./static"
                )
    app.secret_key = os.getenv("FLASK_SECRET_KEY")
    CORS(app, origins=["http://localhost:3000"])
    
    from routes import home_route, vacancies_route, top_bar_route
    app.register_blueprint(home_route.bp)
    app.register_blueprint(vacancies_route.bp)
    app.register_blueprint(top_bar_route.bp)

    return app
