from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from landing import app, db
from landing.models import Message, User
#from landing.mydash import dashapp


@app.route('/', methods=['GET'])
def home():
    try:
        uname = current_user.login
    except:
        uname = False
    return render_template('landingmpage.html', curusr=uname, index=True)


@app.route('/blog', methods=['GET'])
def blog():
    try:
        uname = current_user.login
    except:
        uname = False
    return render_template('blog.html', messages=list(reversed(Message.query.all())), curusr=uname)


@app.route('/blog/<int:id>', methods=['GET'])
def view_post(id):
    post = Message.query.all()
    if id >= len(post):
        return redirect(url_for('blog'))
    return render_template('post.html', tags=post[id].tags, post=post[id].text, postdetail=post[id].details)


@app.route('/feature', methods=['GET'])
def feature():
    return render_template('feature.html')


@app.route('/main', methods=['GET'])
@login_required
def main():
    name = current_user.login
    return render_template('main.html', messages=Message.query.all(), curusr=name)


@app.route('/add_message', methods=['POST'])
@login_required
def add_message():
    text = request.form['text']
    tag = request.form['tag']
    details = request.form['details']
    db.session.add(Message(text, tag, details))
    db.session.commit()
    return redirect(url_for('main'))


@app.route('/landos', methods=['GET'])
def landos_ng_app():
    return render_template('landos/index.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return render_template('landingmpage.html', curusr=user.login)
        else:
            flash('Login or password is not correct')
    else:
        flash('Please fill login and password fields')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
@login_required #for only exist superuser into DB
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if request.method == 'POST':
        if not (login or password or password2):
            flash('Please, fill all fields!')
        elif password != password2:
            flash('Passwords are not equal!')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page'))
    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


##@app.route('/dash')
##def my_dash_app():
##    return dashapp.index()


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)
    return response