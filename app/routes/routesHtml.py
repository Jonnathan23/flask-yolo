from flask import Blueprint, render_template
import socket

routerHtml = Blueprint("htmlRoutes",__name__)

def getLocalIp(): 
    import socket;
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM); 
    s.connect(('8.8.8.8',80)); 
    ip=s.getsockname()[0]; 
    s.close();
    return ip


@routerHtml.route('/', endpoint='index')
def index():
    return render_template('index.html', localIp=getLocalIp())


@routerHtml.route('/sift')
def sift():
    return render_template('sift.html', localIp=getLocalIp())

