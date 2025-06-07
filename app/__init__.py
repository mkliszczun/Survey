from flask import Flask
from .config import Config
from .extensions import login_manager
from .models import User
from .database import db
from flask_migrate import Migrate


def create_app(config_class=Config):
    app = Flask(__name__, template_folder='../templates', static_folder='../static' )
    app.config.from_object(config_class)

    # Inicjalizacja rozszerzeń
    db.init_app(app)
    login_manager.init_app(app)

    from .models import User, Answer
    migrate = Migrate (app,db)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Rejestracja blueprintów
    from app.routes import auth, main, survey, admin, survey_list, question_list, rating
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(survey.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(survey_list.bp)
    app.register_blueprint(question_list.bp)
    app.register_blueprint(rating.bp)



    return app