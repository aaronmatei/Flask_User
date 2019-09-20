from flask import Flask, render_template_string
from flask_mongoengine import MongoEngine
from flask_user import login_required, UserManager, UserMixin
from pymongo.database import _check_name


# class-based application configuration
class ConfigClass(object):
    SECRET_KEY = 'Thisismysecretkey'
    MONGODB_SETTINGS = {
        'db': 'flaskuser',
        'host': 'mongodb://localhost:27017/flaskuser'
    }

    USER_APP_NAME = "Flask-User Mongo-db App"
    USER_ENABLE_EMAIL = False
    USER_ENABLE_USERNAME = True
    USER_REQUIRE_RETYPE_PASSWORD = False
    USER_EMAIL_SENDER_EMAIL = False


def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')

    db = MongoEngine(app)

    class User(db.Document, UserMixin):
        active = db.BooleanField(default=True)

        # information to authenticate the user
        username = db.StringField(default='')
        password = db.StringField()

        # user information
        first_name = db.StringField(default='')
        last_name = db.StringField(default='')

        # Relationships
        roles = db.ListField(db.StringField(), default=[])

    # Setup Flask-User and Specify the User data-model
    user_manager = UserManager(app, db, User)

    @app.route('/')
    def home_page():
            # String-based templates
        return render_template_string("""
                {% extends "flask_user_layout.html" %}
                {% block content %}
                    <h2>Home page</h2>
                    <p><a href={{ url_for('user.register') }}>Register</a></p>
                    <p><a href={{ url_for('user.login') }}>Sign in</a></p>
                    <p><a href={{ url_for('home_page') }}>Home page</a> (accessible to anyone)</p>
                    <p><a href={{ url_for('member_page') }}>Member page</a> (login required)</p>
                    <p><a href={{ url_for('user.logout') }}>Sign out</a></p>
                {% endblock %}                    
                                        
                                        
                                        """)
    # The Members page is only accessible to authenticated users via the @login_required decorator
    @app.route('/members')
    @login_required    # User must be authenticated
    def member_page():
        # String-based templates
        return render_template_string("""
            {% extends "flask_user_layout.html" %}
            {% block content %}
                <h2>Members page</h2>
                <p><a href={{ url_for('user.register') }}>Register</a></p>
                <p><a href={{ url_for('user.login') }}>Sign in</a></p>
                <p><a href={{ url_for('home_page') }}>Home page</a> (accessible to anyone)</p>
                <p><a href={{ url_for('member_page') }}>Member page</a> (login required)</p>
                <p><a href={{ url_for('user.logout') }}>Sign out</a></p>
            {% endblock %}                         
                                      
                                      """)
    return app


# Start development web server
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
