from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import ZakatCalculation
from django.http import HttpResponse

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def faq(request):
    return render(request, 'faq.html')

def terms(request):
    return render(request, 'terms.html')

@login_required
def dashboard(request):
    history = ZakatCalculation.objects.filter(user=request.user).order_by('-date')
    return render(request, 'dashboard.html', {'history': history})

@login_required
def calculator(request):
    rates = {'USD': 1, 'PKR': 278, 'INR': 83, 'SAR': 3.75}
    
    if request.method == 'POST':
        # 1. Get currency and rate
        curr = request.POST.get('currency', 'USD')
        rate = rates.get(curr, 1)

        # 2. Get data from form (added 'or 0' to prevent crashes on empty fields)
        try:
            cash = float(request.POST.get('cash') or 0)
            inventory = float(request.POST.get('inventory') or 0)
            receivables = float(request.POST.get('receivables') or 0)
            liabilities = float(request.POST.get('liabilities') or 0)
        except ValueError:
            # Handle cases where user types letters instead of numbers
            return render(request, 'calculator.html', {'error': 'Please enter valid numbers.'})

        # 3. Calculate math
        net_wealth = (cash + inventory + receivables) - liabilities
        nisab_usd = 6450
        
        zakat_due = 0
        if net_wealth >= (nisab_usd * rate):
            zakat_due = net_wealth * 0.025
        
        # 4. Save to database (Make sure these field names match your models.py)
        ZakatCalculation.objects.create(
            user=request.user,
            cash=cash,
            inventory=inventory,
            receivables=receivables,
            liabilities=liabilities,
            currency=curr,
            zakat_amount=zakat_due
        )

        # 5. Return results to the page (This fixes the "null" output)
        context = {
            'zakat_amount': round(zakat_due, 2),
            'net_wealth': round(net_wealth, 2),
            'currency': curr,
            'success': True
        }
        return render(request, 'calculator.html', context)

    return render(request, 'calculator.html')

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')