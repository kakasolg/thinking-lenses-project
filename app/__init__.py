from flask import Flask

def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)

    if config is None:
        # Load the default configuration
        app.config.from_mapping(
            SECRET_KEY='dev', # Should be overridden in production
            # Add other default configurations here
        )
    else:
        # Load the passed-in configuration
        app.config.from_mapping(config)

    # Ensure the instance folder exists (if using instance_relative_config)
    try:
        import os
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register Blueprints here (will be added in later steps)
    # from .routes import main_routes, math_routes, bagua_routes, api_routes
    # app.register_blueprint(main_routes.bp)
    # app.register_blueprint(math_routes.bp)
    # ...
    from .routes.main_routes import main_bp
    app.register_blueprint(main_bp)

    from .routes.math_routes import math_bp
    app.register_blueprint(math_bp)

    from .routes.bagua_routes import bagua_bp
    app.register_blueprint(bagua_bp)

    from .routes.api_routes import api_bp
    app.register_blueprint(api_bp)

    @app.route('/hello')
    def hello():
        return 'Hello, World! from App Factory'

    return app
