from werkzeug.utils import redirect

from common.database import Database
from models.alert import Alert
from flask import Blueprint, render_template, request, url_for, session
from models.item import Item
from models.store import Store
from models.user import requires_login

alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route('/alerts/index')
@requires_login
def index():
    alerts = Alert.find_many_by('user_email', session['email'])
    return render_template('alerts/index.html', alerts=alerts)


@alert_blueprint.route('/alerts/new', methods=['GET', 'POST'])
@requires_login
def new_alert():
    if request.method == 'POST':
        item_name = request.form['item_name']
        item_url = request.form['item_url']
        user_email = session['email']
        price_limit = float(request.form['price_limit'])
        store = Store.get_by_url_self_made(item_url)
        print(store)
        if len(store) is 0:
            text1 = "The store doesnot exist in our database, please contact develpoers to add store."
            return render_template('alerts/new_alert.html', text=text1)
        else:
            for s in store:
                item = Item(item_url, s.tag_name, s.query)
            item.load_price()
            item.save_to_mongo()
            Alert(item_name, item._id, user_email, price_limit, item_url).save_to_mongo()
            text1 = "The alert has been saved to the database, if you want to save another item fill details and click button."
            return render_template('alerts/new_alert.html', text=text1)
    return render_template('alerts/new_alert.html')


@alert_blueprint.route('/alerts/edit/<string:alert_id>', methods=['GET', 'POST'])
@requires_login
def edit_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    if request.method == 'POST':
        for a in alert:
            if a.user_email == session['email']:
                Price_limit = request.form['price_limit']

                a.Price_limit = Price_limit
                a.get_item_url()
                print(a.item_url)
                print(a.name)
                a.update_to_mongo()
                text = "alert has been successfully edited"
                return redirect(url_for('.index', text=text))
    print(alert)
    return render_template('alerts/edit_alert.html', alert=alert)


@alert_blueprint.route('/alerts/delete/<string:alert_id>')
@requires_login
def delete_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    d = Database
    print(alert)
    for a in alert:
        if a.user_email == session['email']:
            item_id = a.item_id
            a.remove_from_mongo()
            d.remove('items', {"_id": item_id})
    alert = Alert.all()
    return render_template('alerts/index.html', alerts=alert)


# @alert_blueprint.route('alerts/item_check.html')
# @requires_login
# def check_alerts():
#     email_id = session['email']
#     alerts = Alert.find_many_by('user_email', email_id)
#
#     return render_template('alerts/check_alert.html', alerts=alerts)
