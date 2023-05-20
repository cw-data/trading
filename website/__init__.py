from flask import Flask

def createApp():
    app = Flask(__name__)

    from .pages import pages
    app.register_blueprint(pages)

    return app