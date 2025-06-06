from flask import Flask
import os
import dotenv

# TODO - при сохранении с общего -> обновляется и в деталях, и в общем
# при сохранении с деталей -> обновляется у обоих, но потом резко в исходное

# TODO - удаление выдает ошибку джсона, но все равно вакансия удаляется при обновлении

def create_app() -> Flask:
    dotenv.load_dotenv()

    app = Flask(__name__, 
                template_folder="./templates", 
                static_folder="./static"
                )
    app.secret_key = os.getenv("FLASK_SECRET_KEY")
    
    from routes import main, vacancies
    app.register_blueprint(main.bp)
    app.register_blueprint(vacancies.bp)

    return app
