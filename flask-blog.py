from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

@app.route('/jin2/loop')
def index():
    months = ['January','February','March','April','May','June','July',
              'August','September','October','November','December']

    return render_template('weather-average.html',city='Portland, OR',
                           months=months)

if __name__ == '__main__':
    app.run(debug=True)
