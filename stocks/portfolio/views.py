from django.shortcuts import render, redirect
from .forms import StockForm
from .models import  Stock, Wallet
from django.contrib import messages

# Create your views here.

api_key = 'pk_b9e448af3b0b4a338b9c90aecbd6e9ae'

#Get Live Rates
def quote(request):
    import requests
    import json

    wallet = Wallet.objects.get(pk=1)

    #Make API Request to get Live information
    if request.method == 'POST':
        ticker = request.POST['ticker']
        
        api_request = requests.get('https://cloud.iexapis.com/stable/stock/' + ticker + '/quote?token='+ api_key)

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, 'quote.html', {'api': api})
    else:
        return render(request, 'quote.html', {'ticker': "Enter a ticker symbol", 'wallet': wallet})
    
    return render(request, 'quote.html', {'api': api, 'wallet': wallet})

#Handle Stock Order
def order_stock(request): 
    import requests
    import json

    wallet = Wallet.objects.get(pk=1)
    #On POST
    if request.method == 'POST':
        form = StockForm(request.POST or None)

        #Validate Form and save to DB
        if form.is_valid():
            form.save()
            messages.success(request, ("Stock Added to Portfolio"))
            return redirect('order_stock')

    else:
        #Populate portfolio table with stock infromation
        ticker = Stock.objects.all()
        output =[]
        
        #Iterate through each stock symbol, pull information from API
        for ticker_item in ticker:
            api_request = requests.get('https://cloud.iexapis.com/stable/stock/' + str(ticker_item) + '/quote?token='+ api_key)

            try:
                api = json.loads(api_request.content)
                output.append((ticker_item, api))

                #Debit balance upon purchase of new stock
                debt = ticker_item.quantity * api['latestPrice']
                debit_wallet = wallet.balance - int(debt)
                wallet.balance = debit_wallet
                wallet.save()
                

            except Exception as e:
                api = "Error: Bad API Call"
        
    
        return render(request, 'order_stock.html', {'ticker' : ticker, 'output': output, 'wallet': wallet})

def sell(request, stock_id):
    import requests
    import json

    stock = Stock.objects.get(pk=stock_id)
    wallet = Wallet.objects.get(pk=1)
    
    api_request = requests.get('https://cloud.iexapis.com/stable/stock/' + str(stock.ticker) + '/quote?token='+ api_key)    
    api = json.loads(api_request.content)
    
    credit = api['latestPrice'] * stock.quantity
    new_balance = wallet.balance + int(credit)
    wallet.balance = new_balance
    wallet.save()

    stock.delete()
    messages.success(request, ("Stock Sold"))
    return redirect('sell_stock')

def sell_stock(request):
    ticker = Stock.objects.all()
    wallet = Wallet.objects.get(pk=1)
    return render(request, 'sell_stock.html', {'ticker' : ticker, 'wallet': wallet})


def wallet(request):

    wallet = Wallet.objects.get(pk=1)
    return render(request, 'wallet.html', {'wallet' : wallet})

def deposit(request):

    if request.method == 'GET':
        amount = request.GET.get('amount')
        wallet = Wallet.objects.get(pk=1)
        
        new_balance = wallet.balance + int(amount)
        wallet.balance = new_balance
        wallet.save()
    
    return redirect('../wallet')

def home(response):
    return render(response, 'home.html', {})