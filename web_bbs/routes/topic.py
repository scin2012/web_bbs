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
from models.board import Board

from utils import log

from routes import current_user

main = Blueprint('topic', __name__)

import uuid
csrf_token = dict()

@main.route('/')
def index():
    board_id = int(request.args.get('board_id',-1))

    if board_id == -1:
        m = Topic.all()
    else:
        m = Topic.find_all(board_id = board_id)

    u = current_user()
    token = str(uuid.uuid4())
    csrf_token[token] = u.id
    bs = Board.all()

    if u.role == 1:
        current = "管理员"
    else:
        current = "普通用户"

    return render_template('topic/index.html',ms = m,token = token,bs = bs,current = current)


@main.route("/new")
def new():
    bs = Board.all()
    return render_template("topic/new.html",bs = bs)

#新增话题
@main.route('/add',methods=['POST'])
def add():
    form = request.form
    log('topic form:',form)

    u = current_user()

    t=Topic.new(form,user_id = u.id)
    t.board_id=int(t.board_id)

    log('新增话题属于模版--', t.board_id)
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
    t = Topic.get(id)
    b_id = t.board_id
    b = Board.find_by(id = b_id)
    user_id = t.user_id
    auther = User.find(user_id)

    return render_template('topic/detail.html',topic = t,b_title = b.title,auther = auther.username)







