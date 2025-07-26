from flask import Flask
from .routes.routesHtml import routerHtml
from .routes.routes import router

def create_app():
    app = Flask(__name__)    

    # Registrar blueprint de rutas
    app.register_blueprint(routerHtml)
    app.register_blueprint(router)
    return app