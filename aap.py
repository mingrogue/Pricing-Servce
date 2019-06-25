import os
from flask import Flask, render_template
from common.database import Database
from views.storees import store_blueprint
from views.alerts import alert_blueprint
from views.users import user_blueprint


app = Flask(__name__)
app.secret_key = 'arnab'
app.config.update(
    ADMIN=os.environ.get('ADMIN')
)

@app.route('/')
def home():
    return render_template('home.html')

app.register_blueprint(alert_blueprint)#, url_prefix='/alerts')
app.register_blueprint(store_blueprint)#,url_prefix='/stores')
app.register_blueprint(user_blueprint)#, url_prefix='/users')
Database.initialize()


if __name__ == '__main__':
    app.run(debug=True)
