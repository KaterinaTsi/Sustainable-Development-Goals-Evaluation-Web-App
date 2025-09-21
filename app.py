from flask import Flask, render_template
from views import sdg_indicators, views

app = Flask(__name__)
app.register_blueprint(views)

@app.route('/')
def index():
    return render_template('add_sdg.html', sdg_indicators=sdg_indicators)

if __name__ == '__main__': 
    app.run(debug=True, port=8000)