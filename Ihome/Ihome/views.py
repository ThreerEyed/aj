from flask import render_template, Blueprint

user = Blueprint('user', __name__)


@user.route('/register/', methods=['GET'])
def register():
    return render_template('register.html')


@user.route('/register/', methods=['POST'])
def register_count():
    pass


@user.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')



