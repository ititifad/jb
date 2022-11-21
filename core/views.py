from django.shortcuts import render, redirect
from member.models import *
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages #import messages
from .decorators import allowed_users, admin_only
# Create your views here.

def is_valid_queryparam(param):
    return param != '' and param is not None

@login_required(login_url='login')
@admin_only
def home(request):
    members = Member.objects.all()
    member_contains_query = request.GET.get('member_contains')
    qs = Payment.objects.filter(paid=True)
    feetypes = FeeType.objects.all()
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    member = request.GET.get('member')
    feetype = request.GET.get('feetype')
    paid_all = request.GET.get('paid_all')
    not_paid_all = request.GET.get('not_paid_all')
    
    if is_valid_queryparam(member_contains_query):
        qs = qs.filter(member__name__icontains=member_contains_query)
    
    if is_valid_queryparam(date_min):
        qs = qs.filter(created_at__gte=date_min)
        
    if is_valid_queryparam(date_max):
        qs = qs.filter(created_at__lt=date_max)
        
    if is_valid_queryparam(feetype) and feetype != 'Choose...':
        qs= qs.filter(feetype__name=feetype)
        
        
    if is_valid_queryparam(member) and member != 'Choose...':
        qs= qs.filter(member__name=member)
        
    if paid_all == 'on':
        qs = qs.filter(paid=True)

    elif not_paid_all == 'on':
        qs = qs.filter(paid=False)
    
    total_members = qs.count()
    total_payments = qs.aggregate(sum=Sum('payment'))['sum']
    
    context = {
        'qs': qs,
        'members':members,
        'feetypes': feetypes,
        'feetype':feetype,
        'total_members': total_members,
        'total_payments': total_payments,
    }
    return render(request, 'home.html', context)

@login_required(login_url='login')
@admin_only
def member(request, pk):
    member = Member.objects.get(id=pk)
    payments = Payment.objects.all()
    
    context = {
        'member': member,
        'payments': payments,
    }

    return render(request, 'member_detail.html', context)

@login_required(login_url='login')
@admin_only
def members(request):
    members = Member.objects.all()
    
    context = {
        'members': members,
    }

    return render(request, 'members.html', context)

@login_required(login_url='login')
@admin_only
def payment(request):
    payments = Payment.objects.filter(paid=True)
    
    context = {
        'payments': payments,
    }

    return render(request, 'payments.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','member'])
def timetable(request):
    timetables = Timetable.objects.all()
    
    context = {
        'timetables': timetables,
    }

    return render(request, 'timetables.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','member'])
def meeting(request):
    meetings = DepartmentMeeting.objects.all()
    
    context = {
        'meetings': meetings,
    }

    return render(request, 'meetings.html', context)


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username Or Password is incorrect')
            
        context={}
        return render(request, 'login.html', context)
    
def Logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['member'])
def UserPage(request):
    payments = request.user.member.member_fee.all()

    paid_fees = payments.aggregate(total_paid_fees=Sum('payment'))['total_paid_fees']

    member_name = request.user.member


    
    context={
        'payments': payments,
        'paid_fees':paid_fees,
        'member_name':member_name


            
            }
    
    return render(request, 'userpage.html', context)