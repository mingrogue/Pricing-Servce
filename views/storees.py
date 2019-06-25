import json
from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect
from models.store import Store
from models.user import requires_admin, requires_login


store_blueprint = Blueprint('stores', __name__)


@store_blueprint.route('/stores')
@requires_login
def index():
    stores = Store.all()
    return render_template('stores/store_index.html', stores=stores)


@store_blueprint.route('/stores/new', methods=['Get', 'POST'])
@requires_admin
def new_store():
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['URL_Prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['HTML_Query'])
        url_prefix = Store.convert_url(url_prefix)
        store = Store(name, url_prefix, tag_name, query)
        store.save_to_mongo()
        text = "Store has been created enter the details again and press create to add another store"
        return render_template('stores/new_stores.html', text=text)
    return render_template('stores/new_stores.html')


@store_blueprint.route('/stores/edit<string:store_id>', methods=['GET', 'POST'])
@requires_admin
def edit_store(store_id):
    store = Store.get_by_id(store_id)
    print(store)
    print(store_id)
    if request.method == 'POST':
        name = request.form['name']
        #url_prefix = request.form['URL_Prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['HTML_Query'])

        for st in store:
            st.name = name
            #store.url_prefix = url_prefix
            st.tag_name = tag_name
            st.query = query
            st.update_to_mongo()
            text = "Store has been successfully edited"
            return redirect(url_for('.index', text=text, store=st))
    return render_template('stores/edit_stores.html', store=store)


@store_blueprint.route('/stores/delete<string:store_id>')
@requires_admin
def delete_store(store_id):
    store = Store.get_by_id(store_id)
    print(store_id)
    print(store)
    for a in store:
        a.remove_from_mongo()
    store = Store.all()
    return render_template('stores/store_index.html', stores=store)


