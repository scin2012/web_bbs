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
from models.topic import Topic
from models.reply import Reply
from utils import log

from routes import current_user

main = Blueprint('reply', __name__)

@main.route('/add',methods = ['POST'])
def add():
    form = request.form
    u=current_user()
    r=Reply.new(form,user_id = u.id)
    return redirect(url_for('topic.detail',id = r.topic_id))



