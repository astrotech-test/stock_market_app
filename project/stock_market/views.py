from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserSignUpForm
from .models import Stocks, Queries
import pandas as pd
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.template.loader import get_template
from django.template import Context
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def insert_into_db(request):
    df = pd.read_csv("/mnt/c/ml_projects/assignment_planify/backend/project/stock_market/stock_data/stocks.csv")
    
    for row in df.iterrows():
        stock = Stocks()
        print("Inserting into DB", row)
        stock.security_code = row[1][0]
        stock.security_name = row[1][1]
        stock.close = row[1][2]
        stock.market_cap = row[1][3]
        stock.save()
    print("Inserted into database")
    return redirect("index")

# Create your views here.
page_count = 5
def index(request):
    stock_records = Stocks.objects.all()
    page = request.GET.get("page", 1)
    global page_count
    paginator = Paginator(stock_records, page_count)
    page_count += 5
    try:
        stocks = paginator.page(page)
    except PageNotAnInteger:
        stocks = paginator.page(1)
    except EmptyPage:
        stocks = paginator.page(paginator.num_pages)
    return render(request, "stock_market/index.html", {"title": "Stock Market", "stock_records": stocks})

def signup(request):
    global page_count
    page_count = 5
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            print("Form is valid")
            messages.success(request, f"Account created for {username}")
            return redirect("signin")
    else:
        form = UserSignUpForm()
    return render(request, "stock_market/signup.html", {"title": "Signup", "form": form})    

def signin(request):
    global page_count
    page_count = 5
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f'Welcome {username} !!')
            return redirect("index")
        else:
            messages.info(request, f'Invalid username or password')
    form = AuthenticationForm()
    return render(request, "stock_market/signin.html", {"title": "Signin", "form": form})

def search(request):
    global page_count
    page_count = 5
    if request.method == 'POST':      
        stock_name =  request.POST.getlist('search')   
        print(stock_name) 
        try:
            stock_records = Stocks.objects.filter(security_name__contains=stock_name[0])
            #Add_prod class contains a column called 'bookname'
        except stock_records.DoesNotExist:
            stock_records = None
            
        page = request.GET.get("page", 1)
        paginator = Paginator(stock_records, page_count)
        page_count += 5
        try:
            stocks = paginator.page(page)
        except PageNotAnInteger:
            stocks = paginator.page(1)
        except EmptyPage:
            stocks = paginator.page(paginator.num_pages)
            
        return render(request, "stock_market/index.html", {"stock_records": stocks})
    else:
        return redirect("index")

def stock_details(request, slug_name):
    global page_count
    page_count = 5
    
    return render(request, "stock_market/stock_details.html", {"title": slug_name})

def submit_query(request, stock_id):
    global page_count
    page_count = 5
    row = Stocks.objects.get(id=stock_id)
    
    
    print("Query Added")
    if request.method == "POST":
        query = Queries()
        query.security_code = row.security_code
        query.security_name = row.security_name
        query.close = row.close
        query.market_cap = row.market_cap
        query.query = request.POST.get("query")
        query.stock_id = row.id
        query.save()
    else:
        return redirect("index")
    return redirect("index")
    # return render(request, "stock_market/submit_query.html")
