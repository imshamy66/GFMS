import os
from random import randint
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages,auth
from django.core.mail import send_mail
from .models import *

def homePage(request):
    return render(request,'index.html')

def signUp(request):
    if(request.method=='POST'):
        ud = UserDetail()
        ud.name = request.POST.get('name')
        ud.username = request.POST.get('username')
        ud.phone = request.POST.get('phone')
        ud.email = request.POST.get('email')
        ud.pincode = request.POST.get('pincode')
        ud.city = request.POST.get('city')
        ud.state = request.POST.get('state')
        ud.address = request.POST.get('address')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        if(password == cpassword):
            try:
                user = User.objects.create_user(username=ud.username, password=password, email=ud.email)
                user.save()
                ud.save()
                return HttpResponseRedirect("/login/")
            except:
                messages.error(request,"User Name Already Taken")
                return render(request, "signup.html")
        else:
            messages.error(request,"Confirm Password does not matched Please Enter Correct Password")
    return render(request,'signup.html')

def loginPage(request):
    try:
        if(request.method=='POST'):
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username,password=password)
            if(user is not None):
                auth.login(request,user)
                if(user.is_superuser):
                    return HttpResponseRedirect("/admin/")
                else:
                    return HttpResponseRedirect("/welcome/")
            else:
                 messages.error(request,"Invalid User Name or Password")
    except:
        return render(request,'login.html')
    return render(request,'login.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")

@login_required(login_url='/login/')
def profilePage(request):
    user = User.objects.get(username=request.user)
    if(user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        user = UserDetail.objects.get(username=request.user)
        funds = Fund.objects.filter(username=user)
        funds = funds[::-1]
        return render(request,'profile.html',{"User":user,"Funds":funds})

@login_required(login_url='/login/')
def updatePage(request):
    user = User.objects.get(username=request.user)
    if(user.is_superuser):
        return HttpResponseRedirect("/admin/")
    else:
        user = UserDetail.objects.get(username=request.user)
        if(request.method=='POST'):
            user.name = request.POST.get('name')
            user.phone = request.POST.get('phone')
            user.email = request.POST.get('email')
            user.city = request.POST.get('city')
            user.pincode = request.POST.get('pincode')
            user.state = request.POST.get('state')
            user.address = request.POST.get('address')
            if(request.FILES.get("pic")):
                if(user.pic):
                    # os.remove("media/"+str(user.pic))
                    os.remove(str(user.pic))
                user.pic=request.FILES.get('pic')
            user.save()
            return HttpResponseRedirect("/profile/")
    return render(request,'updateprofile.html',{"User": user})

def aboutUs(request):
    return render(request,'about.html')


@login_required(login_url='/login/')
def welcomePage(request):
    state = State.objects.all()
    if(request.method=="POST"):
        active = True
        search = request.POST.get("search")
        state = State.objects.filter(Q(name__icontains=search))
        return render(request,'welcome.html',{"State":state,"Active":active})
    active = False
    return render(request,'welcome.html',{"State":state,"Active":active})

@login_required(login_url='/login/')
def addFund(request):
    state = State.objects.all()
    if(request.method=='POST'):
        f = Fund()
        f.fund_title = request.POST.get("fund_title")
        f.state = State.objects.get(name=request.POST.get("state"))
        f.username = UserDetail.objects.get(username=request.user)
        f.fund_description = request.POST.get('fund_description')
        f.date = request.POST.get('date')
        if(request.FILES.get("pic")):
                if(f.pic):
                    os.remove("media/"+str(f.pic))
                f.pic=request.FILES.get('pic')
        f.save()
        subject = 'New Funds Allocated : Team GFMS'
        message = """
                    Hey !!!
                    New Fund Allocated By the Government
                    Have You Checked ? 
                    http://localhost:8000/fund-details/%d
                    """%(f.id)
        email_from = settings.EMAIL_HOST_USER
        subscriber = NewsLatter.objects.all()
        recipient_list = subscriber
        send_mail( subject, message, email_from, recipient_list )
        
        return HttpResponseRedirect("/profile/")
    return render(request,'addfund.html',{"State": state})


@login_required(login_url='/login/')
def editFund(request,num):
    state = State.objects.all()
    f = Fund.objects.get(id=num)
    if(request.method=='POST'):
        f.fund_title = request.POST.get("fund_title")
        f.state = State.objects.get(name=request.POST.get("state"))
        f.username = UserDetail.objects.get(username=request.user)
        f.fund_description = request.POST.get('fund_description')
        f.date = request.POST.get('date')
        if(request.FILES.get("pic")):
                if(f.pic):
                    os.remove("media/"+str(f.pic))
                f.pic=request.FILES.get('pic')
        f.save()
        return HttpResponseRedirect("/profile/")
    return render(request,'editfund.html',{"Funds": f,"State": state})



@login_required(login_url='/login/')
def stateFundList(request,num):
    state = State.objects.get(id=num)
    fund = Fund.objects.filter(state=state)
    return render(request,'statefunds.html',{"Funds":fund,"State":state})

@login_required(login_url='/login/')
def fundDetails(request,num):
    fund = Fund.objects.get(id=num)
    return render(request,'fundsdetails.html',{"Funds":fund})

def contactUs(request):
    if(request.method=="POST"):
        c = Contact()
        c.name = request.POST.get("name")
        c.phone = request.POST.get("phone")
        c.email = request.POST.get("email")
        c.subject = request.POST.get("subject")
        c.message = request.POST.get("message")
        c.save()
        subject = 'Query Has Been Submitted | Team Government Fund Monitoring System'
        message = """
                    Thanks to Share Your Query with US
                    Our Team Will Contact You Soon
                    Keep Visiting With US
                    http://localhost:8000"""
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [c.email, ]
        send_mail( subject, message, email_from, recipient_list )
        messages.success(request,"Your Query has been Submitted !!!!! Our Team Will Contat You Soon")
    return render(request,"contact.html")

def forgetUsername(request):
    if(request.method=="POST"):
        username = request.POST.get("username")
        user = User.objects.get(username=username)
        if(user is not None):
            user = UserDetail.objects.get(username=username)
            num = randint(100000,999999)
            request.session['otp'] = num
            request.session['user'] = username
            subject = 'OTP for Rest Password : Team Government Fund Monitoring System'
            message = """
                    OTP: %d
                    Keep Visiting With US
                    http://localhost:8000
                    """%num

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list )
            return HttpResponseRedirect("/forget-otp/")
        else:
            messages.error(request,"Username Not Found")
    return render(request,"forget_username.html")

def forgetOtp(request):
    if(request.method=="POST"):
        otp = int(request.POST.get("otp"))
        sesionOTP = request.session.get('otp',None)
        if(otp==sesionOTP):
            return HttpResponseRedirect("/forget-password/")
        else:
            messages.error(request,"Invalid OTP, Please Enter Correct OTP ")
    return render(request,"forget_otp.html")


def forgetPassword(request):
    if(request.method=="POST"):
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        if(password==cpassword):
            user = User.objects.get(username=request.session.get("user"))
            user.set_password(password)
            user.save()
            return HttpResponseRedirect("/login/")
        else:
            messages.error(request,"Password and Confirm Password Does't Matched, Please Enter Correct")
    return render(request,"forget_password.html")
