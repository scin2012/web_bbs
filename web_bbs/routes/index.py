from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
)

from models.user import User

from utils import log

from routes import current_user

from routes import topic

main = Blueprint('index', __name__)

@main.route("/")
def index():
    u = current_user()
    log('current_user:',u)
    return render_template("index.html")


@main.route("/register",methods = ['POST'])
def register():
    form = request.form
    u = User.register(form)
    return redirect(url_for('.index'))


@main.route("/login",methods=['POST'])
def login():
    form=request.form
    log('login....form:',form)

    u = User.validate_login(form)
    if u is None:
        log('登陆失败。。。')
        return redirect(url_for('.index'))
    else:
        log('登陆成功。。。')
        log('设置前  session:', session)
        session['user_id'] = u.id
        session.permanent = True
        log('session:',session)
        return redirect(url_for('topic.index'))

@main.route("/profile")
def profile():
    u=current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template("profile.html",user = u)



