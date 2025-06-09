from flask import Flask
import os
import dotenv

from routes import home_route, home_route, top_bar_route

def create_app() -> Flask:
    dotenv.load_dotenv()

    app = Flask(__name__, 
                template_folder="./templates", 
                static_folder="./static"
                )
    app.secret_key = os.getenv("FLASK_SECRET_KEY")
    
    from routes import vacancies_route
    app.register_blueprint(home_route.bp)
    app.register_blueprint(vacancies_route.bp)
    app.register_blueprint(top_bar_route.bp)

    return app
