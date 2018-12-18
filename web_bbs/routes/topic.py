from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    abort
)

from models.user import User
from models.topic import Topic
from models.reply import Reply

from utils import log

from routes import current_user

main = Blueprint('topic', __name__)

import uuid
csrf_token = dict()

@main.route('/')
def index():
    m = Topic.all()
    u = current_user()
    token = str(uuid.uuid4())
    csrf_token[token] = u.id
    return render_template('topic/index.html',ms = m,token = token)


@main.route("/new")
def new():
    return render_template("topic/new.html")

#新增话题
@main.route('/add',methods=['POST'])
def add():
    form = request.form
    log('add topic form: ',form)
    u = current_user()
    t=Topic.new(form,user_id = u.id)
    log('添加话题成功')
    return redirect(url_for('.detail',id=t.id))

#删除话题
@main.route('/delete')
def delete():
    id = int(request.args.get('id'))
    token = request.args.get('token')
    u = current_user()

    if token in csrf_token and csrf_token[token] == u.id :
        csrf_token.pop(token)
        if u is not None:
            Topic.delete(id)
            return redirect(url_for('.index'))
        else:
            abort(404)
    else:
        abort(403)

@main.route('/<int:id>')
def detail(id):
    t=Topic.get(id)
    log('添加的新话题：',t)
    return render_template('topic/detail.html',topic = t)


