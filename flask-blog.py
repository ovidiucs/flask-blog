import os
import imghdr
from flask import Flask, render_template, request, session
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, FileField, ValidationError
from wtforms.validators import Required, Length


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'

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

@app.route('/')
def hello_world():
    return render_template('index.html')


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


@app.route('/session')
def index5():
    if 'count' not in session:
        session['count'] = 1
    else:
        session['count'] += 1
    return render_template('session.html', count=session['count'])

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)
