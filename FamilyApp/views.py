from datetime import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render

# Create your views here.
from FamilyApp.models import FamilyMembers, Expenses


def reg_fun(request):
    return render(request,'register.html',{'data':''})


def regdata_fun(request):
    email = request.POST['txtEmail']
    password = request.POST['txtPswd']
    username = request.POST['txtUserName']
    if User.objects.filter(username=username).exists():
        return render(request, 'register.html', {'user_available': True})
    elif User.objects.filter(email=email).exists():
        return render(request, 'register.html', {'email_available': True})
    else:
        user = User.objects.create_user(email=email, password=password, username=username)
        user.save()
        return render(request, 'login.html', {'data': ''})


def log_fun(request):
    return render(request,'login.html')


def logdata_fun(request):
    user = authenticate(username=request.POST['txtUserName'], password=request.POST['txtPswd'])
    if user is not None:
        login(request, user)
        return render(request, "home.html")
    else:
        return render(request, 'login.html', {'data': 'failed'})


def go_to_home(request):
    return render(request,'home.html')


def add_family(request):
    return render(request,'addfamilymem.html')



def adding_member(request):
    income = request.POST['txtIncome']
    if income == '':
        context = {
            'null': True
        }
        return render(request, 'addfamilymem.html', context)
    else:
        income = float(income)

    family_mem = FamilyMembers()
    family_mem.firstname = request.POST['txtFirstName']
    family_mem.lastname = request.POST['txtLastName']
    family_mem.income = income
    family_mem.familyLead = request.user
    family_mem.save()
    return render(request, 'addfamilymem.html')


def seefamily(request):
    family_member = FamilyMembers.objects.filter(familyLead=request.user)
    return render(request, 'seefamily.html', {'data': family_member})


def update_family_mem(request,id):
    family_mem = FamilyMembers.objects.get(id=id)
    if request.method == 'POST':
        family_mem.firstname = request.POST['txtFirstName']
        family_mem.lastname = request.POST['txtLastName']
        family_mem.income = float(request.POST['txtIncome'])
        family_mem.save()
        get_all_data = FamilyMembers.objects.filter(familyLead=request.user)
        return render(request,'seefamily.html',{'data':get_all_data})

    return render(request,'update_family.html',{'data':family_mem})


def del_family_mem(request,id):
    family_mem = FamilyMembers.objects.get(id=id)
    family_mem.delete()
    all_updated_data = FamilyMembers.objects.filter(familyLead=request.user)
    return render(request,'seefamily.html',{'data':all_updated_data})


def add_expenses(request):
    redirect_data = FamilyMembers.objects.filter(familyLead=request.user)
    return render(request, 'add_expense.html', {'data': redirect_data})


def save_expense_data(request):
    exp = Expenses()
    exp.familyLead = request.user
    try:
        exp.name = FamilyMembers.objects.get(firstname=request.POST['name'])
    except MultipleObjectsReturned:
        exp.name = FamilyMembers.objects.filter(firstname=request.POST['name']).first()
    exp.purpose = request.POST['purpose']
    exp.expense = float(request.POST['expense'])
    date_from_user = request.POST.get('date')
    exp.date = datetime.strptime(date_from_user, '%Y-%m-%d')
    exp.save()
    return render(request, 'add_expense.html', {'data': FamilyMembers.objects.filter(familyLead=request.user)})




def update_expenses(request,id):
    obj = Expenses.objects.get(id=id)
    redirect_data = FamilyMembers.objects.filter(familyLead=request.user)
    if request.method == "POST":
        obj.familyLead = request.user
        obj.name = (FamilyMembers.objects.get(firstname=request.POST['txtFirstName']))
        obj.purpose = request.POST['purpose']
        obj.expense = float(request.POST['expense'])
        date_user = request.POST.get('date')
        obj.date = datetime.strptime(date_user, '%Y-%m-%d')
        obj.save()
        get_all_data = Expenses.objects.all()
        return render(request,'show_expense.html',{'x':get_all_data})
    return render(request,'update_expense.html',{'x':obj,'data':redirect_data})


def view_expenses(request):
    all_expense = Expenses.objects.filter(familyLead=request.user)
    return render(request,'show_expense.html',{'x':all_expense})


def save_expense_data():
    return None