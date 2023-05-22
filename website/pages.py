from flask import Blueprint, render_template, request
from alpaca import MarketOrder, MainFig, pos_table
import config

pages = Blueprint('pages', __name__)

@ pages.route('/', methods=['GET', 'POST'])
def index():

    main_fig = MainFig()
    main_table = pos_table()

    if request.method == 'POST':
        ticker = request.form.get('ticker')
        qty = request.form.get('qty')
        order_type = request.form.get('order_type')
        order_side = request.form.get('side')
        
        if order_type == 'market':
            order = MarketOrder(ticker, qty, order_side, order_type)
            print(order.data)
            order.place_order()
            return render_template('index.html', graphJSON=main_fig, main_table=main_table)
        elif order_type == 'limit':
            return render_template('index.html', graphJSON=main_fig, main_table=main_table)
        else:
            print("error: didn't match an order_type")

    return render_template('index.html', graphJSON=main_fig, main_table=main_table)