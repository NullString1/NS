from app import db, create_app, models
from werkzeug.security import generate_password_hash
from pathlib import Path
import os

os.remove("app/db.sqlite")
a = create_app()
db.create_all(app=a)

with a.app_context():
    w = models.Tab(name="Windows", url="/win")
    l = models.Tab(name="Linux", url="/linux")
    t = models.Tab(name="Textbooks", url="/textbooks")
    ad = models.Tab(name="Admin", url="/nsadmin", req_auth_level=0)
    
    wData1 = models.accData(title="Tools", text=Path("app/static/win-tools").read_text())
    wData2 = models.accData(title="Troubleshooting", text="aaa")
    wData3 = models.accData(title="Activation", text=Path("app/static/win-acti").read_text())
    
    lData1 = models.accData(title="Images", text=Path("app/static/linux-imgs").read_text())
    lData2 = models.accData(title="Useful commands", text=Path("app/static/linux-cmds").read_text())
    
    admin = models.User(username="ns", password=generate_password_hash(
        "1", method='sha256'), auth_level=0)
    
    l.data.extend([lData1, lData2])
    w.data.extend([wData1, wData2, wData3])
    db.session.add_all([ad, admin, w, l, t])
    db.session.commit()