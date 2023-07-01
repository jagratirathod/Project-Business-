
import time
from django.http import HttpResponse

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from myadmin import models as myadmin_models
from . import models
from business import models as business_models
from django.db.models import Q
from django.conf import settings
media_url = settings.MEDIA_URL


def sessioncheckuser_middleware(get_response):
    def middleware(request):
        if request.path == '/user/' or request.path == '/user/addproduct/':
            if request.session['sunm'] == None or request.session['srole'] != "user":
                response = redirect('/login/')
            else:
                response = get_response(request)
        else:
            response = get_response(request)
        return response
    return middleware


def userhome(request):
    return render(request, "userhome.html", {"sunm": request.session["sunm"]})


def addproduct(request):
    clist = myadmin_models.Category.objects.all()
    if request.method == "GET":
        return render(request, "addproduct.html", {"output": "", "clist": clist, "sunm": request.session["sunm"]})
    else:
        title = request.POST.get('title')
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')
        description = request.POST.get('description')
        bprice = request.POST.get('bprice')
        info = time.time()
        file1 = request.FILES['file1']
        fs = FileSystemStorage()
        file1name = fs.save(file1.name, file1)

    p = models.Product(title=title, category=category, subcategory=subcategory, description=description, bprice=bprice,
                       file1=file1name, status=0, uid=request.session['sunm'], info=time.time())
    p.save()
    return render(request, "addproduct.html", {"output": "Product added successfully....", "clist": clist, "sunm": request.session["sunm"]})


def viewproductuser(request):
    paypalURL = "https://www.sandbox.paypal.com/cgi-bin/webscr"
    paypalID = "sb-antlz6228933@business.example.com"
    # sb-azxwm5529177@personal.example.com
    plist = models.Product.objects.filter(uid=request.session["sunm"])
    return render(request, "viewproductuser.html", {"plist": plist, "sunm": request.session["sunm"], "paypalURL": paypalURL, "paypalID": paypalID})


def cancel(request):
    return render(request, "cancel.html", {"sunm": request.session["sunm"]})


def success(request):
    return render(request, "success.html", {"sunm": request.session["sunm"]})


def payment(request):
    pid = request.GET.get("pid")
    uid = request.GET.get("uid")
    amount = request.GET.get("amount")
    info = time.time()
    p = models.Payment(pid=int(pid), uid=uid, amount=int(amount), info=info)
    p.save()

    models.Product.objects.filter(pid=int(pid)).update(status=1, info=info)
    return redirect("/user/success/")


def bidproduct(request):
    plist = models.Product.objects.filter(~Q(uid=request.session["sunm"]))
    pid = plist[0].pid
    print(pid)
    return render(request, "bidproduct.html", {"sunm": request.session["sunm"], "plist": plist, "pid": pid, "media_url": media_url})


def bidproductview(request):
    pid = int(request.GET.get("pid"))
    bprice = int(request.GET.get("bprice"))
    bidlist = models.Bidding.objects.filter(pid=pid)
    if len(bidlist) > 0:
        bidDetails = models.Bidding.objects.filter(pid=pid)
        cprice = bidDetails[len(bidDetails)-1].bidamount
    else:
        cprice = bprice

    pDetails = models. Product.objects.filter(pid=pid)
    if(time.time()-float(pDetails[0].info)) > 172800:
        bstatus = False
    else:
        bstatus = True

    return render(request, "bidproductview.html", {"sunm": request.session["sunm"], "pid": pid, "bprice": bprice, "cprice": cprice, "bstatus": bstatus})


def bidhistory(request):
    pid = request.GET.get("pid")
    print(pid)
    bidDetails = models.Bidding.objects.filter(pid=pid)
    return render(request, "bidhistory.html", {"sunm": request.session["sunm"], "bidDetails": bidDetails})


def mybid(request):
    pid = request.POST.get("pid")
    bprice = request.POST.get("bprice")
    cprice = request.POST.get("cprice")
    bidprice = request.POST.get("bidprice")
    info = time.asctime()
    p = models.Bidding(
        pid=pid, uid=request.session["sunm"], bidamount=bidprice, info=info)
    p.save()
    return redirect("/user/bidproductview/?pid="+str(pid)+"&bprice="+str(bprice))


def cpuser(request):
    if request.method == "GET":
        return render(request, "cpuser.html", {"sunm": request.session["sunm"]})
    else:
        opass = request.POST.get("opass")
        npass = request.POST.get("npass")
        cnpass = request.POST.get("cnpass")
        res = business_models.Register.objects.filter(
            username=request.session["sunm"], password=opass).exists()
        if res:
            if npass == cnpass:
                business_models.Register.objects.filter(
                    username=request.session["sunm"], password=opass).update(password=cnpass)
                return render(request, "cpmyadmin.html", {"sunm": request.session["sunm"], "output": "Password Change Successfully,please login again"})
            else:
                return render(request, "cpuser.html", {"sunm": request.session["sunm"], "output": "new and conform new password mismatch,please try again"})
        else:
            return render(request, "cpuser.html", {"sunm": request.session["sunm"], "output": "Invalid old password,please try again"})


def fetchSubCategoryAJAX(request):
    cnm = request.GET.get("cnm")
    sclist = myadmin_models.SubCategory.objects.filter(catnm=cnm)
    sclist_options = "<option>select sub category</option>"
    for row in sclist:
        sclist_options += ("<option>"+row. Subcatnm+"</option>")
    return HttpResponse(sclist_options)
