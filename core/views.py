from django.shortcuts import render, redirect,get_object_or_404
from member.models import *
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages #import messages
from .decorators import allowed_users, admin_only
from django.db.models import Q
# Create your views here.

def is_valid_queryparam(param):
    return param != '' and param is not None

@login_required(login_url='login')
@admin_only
def home(request):
    
    member_contains_query = request.GET.get('member_contains')
    qs = Member.objects.all()
    feetypes = Offering.objects.all()
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    name = request.GET.get('name')
    feetype = request.GET.get('feetype')
    paid_all = request.GET.get('paid_all')
    not_paid_all = request.GET.get('not_paid_all')
    
    if is_valid_queryparam(member_contains_query):
        qs = qs.filter(name__icontains=member_contains_query)
    
    if is_valid_queryparam(date_min):
        qs = qs.filter(created_at__gte=date_min)
        
    if is_valid_queryparam(date_max):
        qs = qs.filter(created_at__lt=date_max)
        
    if is_valid_queryparam(feetype) and feetype != 'Choose...':
        qs= qs.filter(feetype__name=feetype)
        
        
    if is_valid_queryparam(name) and name != 'Choose...':
        qs= qs.filter(name=name)
        
    if paid_all == 'on':
        qs = qs.filter(paid=True)

    elif not_paid_all == 'on':
        qs = qs.filter(paid=False)
    
    total_members = qs.count()
    total_payments = Payment.objects.aggregate(sum=Sum('payment'))['sum']
    total_zaka = Zaka.objects.aggregate(sum=Sum('payment'))['sum']
    
    context = {
        'qs': qs,
        'members':members,
        'feetypes': feetypes,
        'feetype':feetype,
        'total_members': total_members,
        'total_payments': total_payments,
        'total_zaka':total_zaka
    }
    return render(request, 'home.html', context)

@login_required(login_url='login')
@admin_only
def member(request, pk):
    member = get_object_or_404(Member,id=pk)
    offerings = member.offerings.all()
    # Calculate total amount, total payments, and total remaining for all offerings
    total_amount_all_offerings = sum(offerings.values_list('amount', flat=True))
    total_payments_all_offerings = sum(payment.payment for payment in Payment.objects.filter(offering__in=offerings))
    total_remaining_all_offerings = total_amount_all_offerings - total_payments_all_offerings
    total_zaka_payment = Zaka.objects.filter(member=member).aggregate(total_payment=models.Sum('payment'))['total_payment'] or 0
    

    context = {
        'member': member,
        'offerings': offerings,
        'total_amount_all_offerings': total_amount_all_offerings,
        'total_payments_all_offerings': total_payments_all_offerings,
        'total_remaining_all_offerings': total_remaining_all_offerings,
        'total_zaka_payment':total_zaka_payment,
        
    }
    return render(request, 'member_detail.html', context)

@login_required(login_url='login')
@admin_only
def members(request):
    query = request.GET.get('query', '')
    members = Member.objects.filter(Q(name__icontains=query) | Q(namba_ya_zaka__icontains=query)).order_by('-created_at')
    # members = Member.objects.all()
    
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
    member = request.user.member  # Assuming the user has a OneToOneField to the Member model
    offerings = Offering.objects.filter(member=member)
    total_zaka_payment = Zaka.objects.filter(member=member).aggregate(total_zaka=Sum('payment'))['total_zaka'] or 0

    # Calculate overall total offering amount, total payment, and total remaining
    overall_total_amount = offerings.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    overall_total_payment = Payment.objects.filter(offering__member=member).aggregate(total_payment=Sum('payment'))['total_payment'] or 0
    overall_total_remaining = overall_total_amount - overall_total_payment
    payments = Payment.objects.filter(offering__member=member)

    context = {
        'member': member,
        'offerings': offerings,
        'total_zaka_payment':total_zaka_payment,
        'overall_total_amount': overall_total_amount,
        'overall_total_payment': overall_total_payment,
        'overall_total_remaining': overall_total_remaining,
        'payments':payments
    }
    # Calculate total zaka payment for the member
    

    return render(request, 'userpage.html', context)

@login_required(login_url='login')
@admin_only
def report(request):
    # Calculate total amount, total payments, and total remaining for all offerings
    total_amount_all_offerings = Offering.objects.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    total_payments_all_offerings = Payment.objects.aggregate(total_payment=Sum('payment'))['total_payment'] or 0
    total_remaining_all_offerings = total_amount_all_offerings - total_payments_all_offerings

    # Calculate total zaka payment for all members
    total_zaka_payment = Zaka.objects.aggregate(total_payment=Sum('payment'))['total_payment'] or 0

    # Calculate total remaining for each offering for all members
    total_remaining_per_offering = {}
    offerings = Offering.objects.all()
    for offering in offerings:
        total_remaining_per_offering[offering] = offering.amount - offering.payments.aggregate(total_payment=Sum('payment'))['total_payment'] or 0

    # Calculate total amount, total payments, and total remaining for each offering
    offerings_totals = []
    for offering in offerings:
        total_amount = offering.amount
        total_payments = offering.payments.aggregate(total_payment=Sum('payment'))['total_payment'] or 0
        total_remaining = total_amount - total_payments
        offerings_totals.append((offering, total_amount, total_payments, total_remaining))

    context = {
        'total_amount_all_offerings': total_amount_all_offerings,
        'total_payments_all_offerings': total_payments_all_offerings,
        'total_remaining_all_offerings': total_remaining_all_offerings,
        'total_zaka_payment': total_zaka_payment,
        'total_remaining_per_offering': total_remaining_per_offering,
        'offerings_totals': offerings_totals,
    }
    return render(request, 'report.html', context)