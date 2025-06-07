from flask import Flask
import os
import dotenv

from routes import home

def create_app() -> Flask:
    dotenv.load_dotenv()

    app = Flask(__name__, 
                template_folder="./templates", 
                static_folder="./static"
                )
    app.secret_key = os.getenv("FLASK_SECRET_KEY")
    
    from routes import home, vacancies, top_bar
    app.register_blueprint(home.bp)
    app.register_blueprint(vacancies.bp)
    app.register_blueprint(top_bar.bp)

    return app
