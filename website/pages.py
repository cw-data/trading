from flask import Blueprint, render_template, request

pages = Blueprint('pages', __name__)

@ pages.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        ticker = request.form.get('ticker')
        qty = request.form.get('qty')
        order_type = request.form.get('order_type')
        print(ticker)
        print(qty)
        print(order_type)

    return render_template('index.html')