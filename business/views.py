from business import sendEmailpass
from . import sendEmail

import time
from user import models as user_models
from django.http import HttpResponse, response
from django.shortcuts import render, redirect
from django.conf import settings
from . import models
from . import encryption_api
from . import decryption_api
from myadmin import models as myadmin_models

media_url = settings.MEDIA_URL

# middleware to check session for business routes


def sessioncheck_middleware(get_response):
    def middleware(request):
        if request.path == '' or request.path == '/about/' or request.path == '/contact/' or request.path == '/register/' or request.path == '/login/':
            request.session['sunm'] = None
            request.session['srole'] = None

            response = get_response(request)
        else:
            response = get_response(request)
        return response
    return middleware


def home(request):
    clist = myadmin_models.Category.objects.all()
    return render(request, "home.html", {"clist": clist, "media_url": media_url})


def viewsubcategory(request):
    catnm = request.GET.get("catnm")
    clist = myadmin_models.Category.objects.all()
    sclist = myadmin_models. SubCategory.objects.filter(catnm=catnm)
    return render(request, "viewsubcategory.html", {"catnm": catnm, "clist": clist, "sclist": sclist, "media_url": media_url})


def viewproductfilter(request):
    cnm = request.GET.get("cnm")
    scnm = request.GET.get("scnm")
    startprice = request.GET.get("startprice")
    endprice = request.GET.get("endprice")
    if startprice == None:
        plist = user_models.Product.objects.filter(subcategory=scnm)
    else:
        plist = user_models.Product.objects.filter(
            subcategory=scnm, bprice__range=(int(startprice), int(endprice)))

    sclist = myadmin_models.SubCategory.objects.filter(catnm=cnm)
    return render(request, "viewproductfilter.html", {"cnm": cnm, "scnm": scnm, "media_url": media_url, "sclist": sclist, "plist": plist})


def about(request):
    return render(request, "about.html", {})


def contact(request):
    return render(request, "contact.html", {})


def service(request):
    return render(request, "service.html", {})


def register(request):
    if request.method == "GET":
        return render(request, "register.html", {"output": ""})
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        mobile = request.POST.get("mobile")
        gender = request.POST.get("gender")
        city = request.POST.get("city")
        address = request.POST.get("address")
        info = time.asctime()
        # To send verification  link via email
        # sendEmail.mymail(username, password)
        v = models.Register(username=username, password=password, mobile=mobile,gender=gender, city=city, address=address, role="user", status=0, info=info)
        v.save()
        return render(request, "register.html", {"output": "form submitted successfully"})


def checkEmailAvailibility(request):
    alert(hello)
    v = request.GET.get("v")
    res = models.Register.objects.filter(username_startwith=v).exists()
    if res:
        msg = "Email Id Already Exists,please choose new"
    else:
        msg = "Email Id available"
    return HttpResponse(msg)


def verifyuser(request):
    email = request.GET.get("email")
    models.Register.objects.filter(username=email).update(status=1)
    return redirect("/login/")


def login(request):
    cunm = ""
    cpass = ""
    if request.COOKIES.get("cunm") != None:
        cunm = request.COOKIES.get("cunm")
        cencpassword = request.COOKIES.get("cpass")
        l = list(cencpassword)
        l.pop(0)
        l.pop(0)
        l.pop(len(l)-1)
        s = ""
        for x in l:
            s += x
        cencpassword_byte = bytes(s, 'utf-8')
        cpass = decryption_api.decrypt_message(cencpassword_byte)
    if request.method == "GET":
        return render(request, "login.html", {"output": "", "cunm": cunm, "cpass": cpass})
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        userDetails = models.Register.objects.filter(
            username=username, password=password, status=1)

        if len(userDetails) > 0:
            # To store details session
            request.session["sunm"] = userDetails[0].username
            request.session["srole"] = userDetails[0].role
            if userDetails[0].role == "admin":
                response = redirect("/myadmin/")
            else:
                response = redirect("/user/")

            if request.POST.get("chk") == "remember":
                encrypted_message = encryption_api.encrypt_message(
                    userDetails[0].password)
                response.set_cookie("cunm", userDetails[0].username, 3600*24)
                #response.set_cookie("cpass", userDetails[0].password, 3600*24)
                response.set_cookie("cpass", encrypted_message, 3600*24)
            return response
        else:
            return render(request, "login.html", {"output": "Invalid user , please check authentication..."})


def forgetpassword(request):
    if request.method == "GET":
        return render(request, 'forgetpassword.html')
    else:
        username = request.POST.get("username")
        userDetails = models.Register.objects.filter(username=username)
        password = userDetails[0].password
        print(password)
        sendEmailpass.mymail(username, password)
        return render(request, 'forgetpassword.html', {"output": "Password send succssfully"})
