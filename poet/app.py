# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, jsonify
from flask_cors import CORS
from marshmallow.exceptions import ValidationError

from poet import commands, public, models
from poet.errors import APIException, NotFound
from poet.extensions import bcrypt, cache, db, login_manager, migrate
from poet.locales import Errors
from poet.settings import ProdConfig


def create_app(config_object=ProdConfig):
    """An application factory.

    as explained here: http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    CORS(app, origins=[r'.*\.diagramcenter\.org'])
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    from poet.api.v1.users.api import blueprint as users_v1
    app.register_blueprint(users_v1)
    from poet.api.v1.uploads.api import blueprint as uploads_v1
    app.register_blueprint(uploads_v1)
    from poet.api.v1.emails.api import blueprint as emails_v1
    app.register_blueprint(emails_v1)
    from poet.api.v1.annotations.api import blueprint as annotations_v1
    app.register_blueprint(annotations_v1)
    return None


def register_errorhandlers(app):
    """Register error handlers."""
    @app.errorhandler(APIException)
    def handle_api_error(err):
        """Handle an APIException."""
        return jsonify(err.to_dict()), err.status_code

    @app.errorhandler(404)
    def handle_api_not_found(err):
        """Handle a generic 404 abort."""
        err = NotFound(Errors.RESOURCE_NOT_FOUND, status_code=404)
        return jsonify(err.to_dict()), 404
        raise NotFound(Errors.RESOURCE_NOT_FOUND)

    @app.errorhandler(500)
    def handle_internal_error(err):
        """Handle a generic 500 abort."""
        err = APIException(Errors.UNKNOWN_ERROR, status_code=500)
        return jsonify(err.to_dict()), 500

    @app.errorhandler(422)
    def handle_unprocessable_entity(err):
        # webargs attaches additional metadata to the `data` attribute
        exc = getattr(err, 'exc')
        if exc:
            # Get validations from the ValidationError object
            messages = exc.messages
        else:
            messages = ['Invalid request']
        return jsonify({
            'messages': messages,
        }), 422

    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation_error(ex):
        response = jsonify(error_code="data-validation-error",
                           error_message=ex.messages)
        response.status_code = 422
        return response

    return None


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'model': models
        }

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
