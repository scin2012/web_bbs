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

main = Blueprint('board', __name__)

@main.route('/admin')
def index():
    u = current_user()
    bs = Board.all()
    if u.role == 1:
        return render_template('board/admin_index.html',bs = bs)
    else:
        abort(404)

@main.route('/add',methods = ['POST'])
def add():
    form = request.form
    b = Board.new(form)
    return redirect(url_for('topic.index'))

@main.route('/delete')
def delete():
    id = int(request.args.get('id',-1))
    log('要删除的board_id=',id)
    b = Board.delete(id)
    return redirect(url_for('.index'))









