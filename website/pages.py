from flask import Blueprint, render_template, request
from alpaca import create_market_order, MarketOrder


pages = Blueprint('pages', __name__)

@ pages.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        
        ticker = request.form.get('ticker')
        qty = request.form.get('qty')
        order_type = request.form.get('order_type')
        order_side = request.form.get('side')
        # print(ticker)
        # print(qty)
        # print(order_type)

        # if order_type == 'Market':
        #     order = MarketOrder()
        if order_type == 'market':
            order = MarketOrder(ticker, qty, order_side, order_type)
            print(order.data)
            order.place_order()
            # create_market_order(ticker, qty, order_side, order_type)
            return render_template('index.html')
        elif order_type == 'limit':
            return render_template('index.html')
        else:
            print("error: didn't match an order_type")

    return render_template('index.html')