from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.pagedown import PageDown
from flask.ext.login import LoginManager

db = SQLAlchemy()

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'accounts.login'
