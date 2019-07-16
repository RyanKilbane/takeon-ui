from flask import Flask

from flask_jwt_extended import JWTManager

# from app.eureka_config import eureka_config
from app.kubernetes_discovery import kubernetes_config

from app import settings

# eureka_configuration = eureka_config.EurekaConfig(mocking=settings.MOCKING)
discovery_service = kubernetes_config.KubernetesConfig("take-on", mocking=settings.MOCKING )


def create_app(setting_overrides=None):
    # Define the WSGI application object
    application = Flask(__name__, static_url_path='/s', static_folder='./static')

    # Configurations
    application.config.from_object(settings)
    application.config['JWT_TOKEN_LOCATION'] = ['cookies']  # store token in cookies
    # application.config['JWT_COOKIE_SECURE'] = True  # cookies can only be sent over https
    application.config['JWT_ACCESS_COOKIE_PATH'] = ''
    # application.config['JWT_SECRET_KEY'] = settings.SECRET_KEY using default secret key
    jwt = JWTManager(application)  # pylint: disable=W0612
    application.config['CORS_HEADERS'] = 'Content-Type'

    if setting_overrides:
        application.config.update(setting_overrides)

    add_blueprints(application)

    # eureka_client_registration(application)
    # eureka_configuration.eureka_client_registration(application)

    return application


def add_blueprints(application):
    from app.forms.contributor_search.contributor_search_form import contributor_search_blueprint
    application.register_blueprint(contributor_search_blueprint)
    contributor_search_blueprint.config = application.config.copy()

    from app.forms.view_form.view_form import view_form_blueprint
    application.register_blueprint(view_form_blueprint)
    view_form_blueprint.config = application.config.copy()

    from app.forms.search_screen_choice.search_screen_choice import search_screen_choice_blueprint
    application.register_blueprint(search_screen_choice_blueprint)
    search_screen_choice_blueprint.config = application.config.copy()

    from app.forms.edit_form.edit_form import edit_form_blueprint
    application.register_blueprint(edit_form_blueprint)
    edit_form_blueprint.config = application.config.copy()

    from app.forms.login_form.login_form import login_form_blueprint
    application.register_blueprint(login_form_blueprint)
    login_form_blueprint.config = application.config.copy()
