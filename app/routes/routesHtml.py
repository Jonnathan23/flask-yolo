from flask import Blueprint, render_template


routerHtml = Blueprint("main",__name__)

@routerHtml.route('/', endpoint='index')
def index():
    return render_template('index.html')