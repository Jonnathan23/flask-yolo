from flask import Blueprint, render_template


routerHtml = Blueprint("htmlRoutes",__name__)

@routerHtml.route('/', endpoint='index')
def index():
    return render_template('index.html')


@routerHtml.route('/sift')
def sift():
    return render_template('sift.html')