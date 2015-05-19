from flask import render_template, request, url_for, redirect
from flask.ext.login import login_required, login_user, logout_user
from ..models import User
from . import main
from .forms import LoginForm

"""
POST request > wtf run all the validators and if
they validate they get in the if body
ser.query.filter_by(username=form.username.data)
--if user is None
1 or None (user is valid, user invalid return None
Never get more than one. Username is unique

--user.verify_password(form.password.data):
    we need to let the user try again, redirect to login page
    a redirect to itself
--login_user(user, form.remember_me.data)
    function that comes with flask.login,
    login the user pass the user object and tell it if
    we want it that it should be a user to be remembered
--return redirect(request.args.get('next') or url_for('index'))
    redirect to home page or protected page while being logged out
    intercepted and sent to the login
--request.args
    python dictionary will have all the elements
    next is used in arguments if user tried to access restricted page
    if user will login ok then it will use the next parameter, which in
    turn it will go to protected page
--args.get('next'
    none > redirect to index page or protected page
--
"""


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first
        if user is None or not user.verify_password(form.password.data):
            return redirect(url_for('main.login', **request.args))
        login_user(user, form.remember_me.data)
        return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/protected')
@login_required
def protected():
    return render_template('protected.html')


@app.route('/')
def hello_world():
    return render_template('index.html')
