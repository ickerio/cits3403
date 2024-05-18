from flask import Flask
from config import DeploymentConfig
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)
migrate = Migrate(render_as_batch=True)
login_manager = LoginManager()
bcrypt = Bcrypt()
csrf = CSRFProtect()

def create_app(config_class=DeploymentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.session_protection = "strong"
    login_manager.login_view = "login"
    login_manager.login_message_category = "info"

    with app.app_context():
        from app import routes, models, forms
    
    return app
