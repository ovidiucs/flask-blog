import os
import imghdr
from datetime import datetime
from flask import Flask, render_template, request, session, g, \
    make_response, jsonify, url_for, redirect
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, FileField, ValidationError
from wtforms.validators import Required, Length
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)

# The SECRET_KEY field in the app config is used by WTForms to create CSRF tokens.
# It is also used by itsdangerous (included in Flask) to sign cookies and other data.

app.config['SECRET_KEY'] = 'top secret!'
# where the db is
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
db = SQLAlchemy(app)
# initialize extension
bootstrap = Bootstrap(app)


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required(),
                                                         Length(1, 16)])
    submit = SubmitField('Submit')


class UploadForm(Form):
    image_file = FileField('Image file')
    submit = SubmitField('Submit')

    def validate_image_file(self, field):
        if field.data.filename.rsplit('.', 1)[1] != 'jpg':
            raise ValidationError('Invalid file extension')
        if imghdr.what(field.data) != 'jpeg':
            raise ValidationError('Invalid image format')


# Define a class that represents our users in the database
# This class inherits from  a base model classes
# Models > Classes > Associated with entities within a database.
# The hardest part was finding the right SQLAlchemy data types and picking a
# length for our String fields in the database. Using our models is also extremely
# simple, thanks to the SQLAlchemy query syntax

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), index=True, unique=True)

    username = db.Column(db.String(16), index=True, unique=True)
    password_hash = db.Column(db.String(64))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def register(username, password):
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user


    def __repr__(self):
        return '<User {0}>'.format(self.name)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/text')
def text():
    return render_template('text.txt'), 200, {'Content-Type': 'text/plain'}


@app.route('/xml')
def xml():
    return '<h1>this is shown as <b>XML</b> in the browser</h1>', 200, \
           {'Content-Type': 'application/xml'}


@app.route('/json')
def json():
    return jsonify({'first_name': 'john', 'last_name': 'Smith'})


@app.route('/redirect')
def redir():
    return redirect(url_for('text'))


@app.route('/cookie')
def cookie():
    resp = redirect(url_for('index'))
    resp.set_cookie('cookie', 'Hello, im a cookie')
    return resp


@app.route('/error')
def error():
    return 'Bad Request', 400


@app.route('/response')
def response():
    resp = make_response(render_template('text.txt'))
    resp.headers['Content-Type'] = 'text/plain'
    return resp


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.route('/loop')
def index():
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
    weather = {
        'January': {'min': 38, 'max': 47, 'rain': 6.14},
        'February': {'min': 38, 'max': 51, 'rain': 4.79},
        'March': {'min': 41, 'max': 56, 'rain': 4.5},
        'April': {'min': 44, 'max': 61, 'rain': 3.4},
        'May': {'min': 49, 'max': 67, 'rain': 2.55},
        'June': {'min': 53, 'max': 73, 'rain': 1.69},
        'July': {'min': 57, 'max': 80, 'rain': 0.59},
        'August': {'min': 58, 'max': 80, 'rain': 0.71},
        'September': {'min': 54, 'max': 75, 'rain': 1.54},
        'October': {'min': 48, 'max': 63, 'rain': 3.42},
        'November': {'min': 41, 'max': 52, 'rain': 6.74},
        'December': {'min': 36, 'max': 45, 'rain': 6.94}
    }

    highlight = {'min': 40, 'max': 80, 'rain': 5}

    return render_template('weather-average.html', city='Portland, OR',
                           months=months, weather=weather, highlight=highlight)


@app.route('/form', methods=['GET', 'POST'])
def findex():
    name = None
    if request.method == 'POST' and 'name' in request.form:
        name = request.form['name']
    return render_template('form.html', name=name)


@app.route('/form2', methods=['GET', 'POST'])
def index3():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('form2.html', form=form, name=name)


@app.route('/upload', methods=['GET', 'POST'])
def index4():
    image = None
    form = UploadForm()
    if form.validate_on_submit():
        image = 'uploads/' + form.image_file.data.filename
        form.image_file.data.save(os.path.join(app.static_folder, image))
    return render_template('upload.html', form=form, image=image)


@app.before_request
def before_request():
    if not 'count' in session:
        session['count'] = 1
    else:
        session['count'] += 1
    g.when = datetime.now().strftime('%H:%M:%S')


@app.route('/session')
def index5():
    return render_template('session.html', count=session['count'], when=g.when)


@app.route('/other')
def index6():
    return render_template('other.html', count=session['count'], when=g.when)


@app.route('/sql', methods=['GET', 'POST'])
def sqla():
    name = None
    new = False

    form = NameForm()

    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        if User.query.filter_by(name=name).first() is None:
            db.session.add(User(name=name))
            db.session.commit()
            new = True
    return render_template('sqla.html', form=form, name=name, new=new)


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
