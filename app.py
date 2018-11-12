from flask import Flask, render_template, request, redirect
import requests
from iexfinance import Stock
import datetime
app = Flask(__name__)

@app.route('/')
def hello_world():
    author = "Me"
    name = "You"
    return render_template('index.html', author=author, name=name)

@app.route('/stockcalc', methods = ['POST'])
def stockcalc():
    ticker_symbol = request.form['Ticker Symbol']
    allotment = request.form['Allotment']
    final_share_price = request.form['Final Share Price']
    sell_commission = request.form['Sell Commission']
    initial_share_price = request.form['Initial Share Price']
    buy_commission = request.form['Buy Commission']
    capital_gain_tax = request.form['Capital Gain Tax Rate']

    print(allotment,final_share_price,sell_commission,initial_share_price,buy_commission,capital_gain_tax)

    proceeds = float(allotment)*float(final_share_price)
    cost_part_1 = float(allotment) * float(initial_share_price) + float(buy_commission) + float(sell_commission) 
    capital_gain = (proceeds-cost_part_1)*(float(capital_gain_tax)/100) 
    purchase_price = float(allotment) * float(initial_share_price)
    
    cost = cost_part_1 + capital_gain
    net_profit = proceeds - cost

    return_on_investment = (net_profit/cost)*100
    return_on_investment = round(return_on_investment,2)
    final_share_price = float(cost_part_1/100)

    return render_template('result.html', proceeds=proceeds, cost=cost, purchase_price=purchase_price, capital_gain=capital_gain, net_profit=net_profit, return_on_investment=return_on_investment, final_share_price=final_share_price)

@app.route('/getstocks', methods = ['POST'])
def getstocks():
    symbol = request.form['symbol']
    now = datetime.datetime.now()
    current_datetime = str(now.month)+" "+str(now.day)+" "+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+" "+str(now.year)
    stock_infor = requests.get('https://api.iextrading.com/1.0/stock/'+symbol+'/quote')

    if stock_infor.status_code==200:

        json_data = stock_infor.json()
        company = json_data['companyName']
        latestPrice = json_data['latestPrice']
        change = json_data['change']
        changePercent = json_data['changePercent']

        stockPrice = str(latestPrice)+" "+str(change)+ " "+str(changePercent*100)+"%"
        return render_template('result_stock.html',current_datetime=current_datetime, company=company, stockPrice=stockPrice)

    else:
        return render_template('result_stock.html',current_datetime="N/A", company="N/A", stockPrice="N/A")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)