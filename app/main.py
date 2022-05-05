from flask import Blueprint, render_template, request, current_app, redirect, send_file, url_for
from flask_login import login_required, current_user
from .models import Tab
from functools import wraps
from pathlib import Path
from werkzeug.utils import secure_filename
import os

main = Blueprint('main', __name__)

def getTabs():
    return Tab.query.filter(Tab.req_auth_level>=(1 if not current_user.is_authenticated else current_user.auth_level)).all()

def auth_level_required(level):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if level >= current_user.auth_level:
                return func(*args, **kwargs)
            else:
                return current_app.login_manager.unauthorized()
        return wrapper
    return decorator

@main.route('/')
def index():
    return render_template("index.html", tabs=getTabs())


@main.route('/profile')
@login_required
def profile():
    return render_template("profile.html", username=current_user.username, tabs=getTabs())

@main.route("/win")
def win():
    print("---------")
    print(Tab.query.filter_by(name="Windows").first().data.all())
    return render_template("datapage.html", tabs=getTabs(), data=Tab.query.filter_by(name="Windows").first().data)

@main.route("/linux")
def linux():
    return render_template("datapage.html", tabs=getTabs(), data=Tab.query.filter_by(name="Linux").first().data)

@main.route("/textbooks")
def tbooks():
    return render_template("tbooks.html", tabs=getTabs(), t=Path("app/static/tbooks").read_text())

@main.route("/d/<string:s>")
def d(s: str):
    return send_file((Path("d/") / s))

@main.route("/nsadmin")
@login_required
@auth_level_required(0)
def admin():
    return render_template("admin.html", tabs=getTabs(), filelist=[*["templates/" + x for x in os.listdir("app/templates")],*["static/" + x for x in os.listdir("app/static")]])

@main.route("/nsadmin/file", methods=['GET'])
@login_required
@auth_level_required(0)
def getFile():
    f = (Path.cwd() / "app" / request.args.get('f')).resolve()
    if f.parent in [Path.cwd() / "app" / "templates", Path.cwd() / "app" / "static"]:
        return f.read_text()
    return "", 403
    
@main.route("/nsadmin/file", methods=['POST'])
@login_required
@auth_level_required(0)
def writeFile():
    f = (Path.cwd() / "app" / request.args.get('f')).resolve()
    if f.parent in [Path.cwd() / "app" / "templates", Path.cwd() / "app" / "static"]:
        f.write_text(request.form.get("data"))
        return redirect(url_for('main.admin'))
    return redirect(url_for('main.admin')), 403

@main.route("/nsadmin/del")
@login_required
@auth_level_required(0)
def delFile():
    f = (Path.cwd() / "app" / request.args.get('f')).resolve()
    if f.parent in [Path.cwd() / "app" / "templates", Path.cwd() / "app" / "static"]:
        f.unlink()
        return redirect(url_for('main.admin'))
    return redirect(url_for('main.admin')), 403