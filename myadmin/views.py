from django.shortcuts import render, redirect
from business import models as business_models
from . import models
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse


def sessioncheckmyadmin_middleware(get_response):
    def middleware(request):
        if request.path == '/myadmin/' or request.path == '/myadmin/manageusers/' or request.path == '/myadmin/manageuserstatus/' or request.path == '/myadmin/addcategory/':
            if request.session['sunm'] == None or request.session['srole'] != "admin":
                response = redirect('/login/')
            else:
                response = get_response(request)
        else:
            response = get_response(request)
        return response
    return middleware


def adminhome(request):
    return render(request, "adminhome.html", {"sunm": request.session["sunm"]})


def manageusers(request):
    userDetails = business_models.Register.objects.filter(role='user')
    return render(request, "manageusers.html", {"userDetails": userDetails, "sunm": request.session["sunm"]})


def manageuserstatus(request):
    regid = request.GET.get("regid")
    s = request.GET.get("s")

    if s == "block":
        business_models.Register.objects.filter(
            regid=int(regid)).update(status=0)
        return redirect("/myadmin/manageusers/")

    elif s == "verify":
        business_models.Register.objects.filter(
            regid=int(regid)).update(status=1)
        return redirect("/myadmin/manageusers/")

    else:
        business_models.Register.objects.filter(regid=int(regid)).delete()
        return redirect("/myadmin/manageusers/")


def addcategory(request):
    if request.method == "GET":
        return render(request, "addcategory.html", { "sunm": request.session["sunm"]})
    else:
        catnm = request.POST.get("catnm")
        caticon = request.FILES['caticon']
        fs = FileSystemStorage()
        filename = fs.save(caticon.name, caticon)
        print(catnm, "---", filename)
        p = models.Category(catnm=catnm, caticonname=filename)
        p.save()
        return render(request, "addcategory.html", {"output": "category Added Successfully", "sunm": request.session["sunm"]})


def subcategory(request):
    clist = models.Category.objects.all()
    if request.method == "GET":
        return render(request, "subcategory.html", {"clist": clist, "sunm": request.session["sunm"]})
    else:
        catnm = request.POST.get("catnm")
        subcatnm = request.POST.get("subcatnm")
        caticon = request.FILES['caticon']
        fs = FileSystemStorage()
        filename = fs.save(caticon.name, caticon)
        p = models.SubCategory(
            catnm=catnm, Subcatnm=subcatnm, subcaticonname=filename)
        p.save()

        return render(request, "subcategory.html", {"clist": clist, "output": 'Sub Category Added Successfully', "sunm": request.session["sunm"]})


def cpmyadmin(request):
    if request.method == "GET":
        return render(request, "cpmyadmin.html", {"output": "","sunm":request.session["sunm"]})
    else:
        opass = request.POST.get("opass")
        npass = request.POST.get("npass")
        cnpass = request.POST.get("cnpass")
        res = business_models.Register.objects.filter(username=request.session["sunm"], password=opass).exists()
        if res:
            if npass == cnpass:
                business_models.Register.objects.filter(username=request.session["sunm"], password=opass).update(password=cnpass)
                return render(request, "cpmyadmin.html", {"sunm": request.session["sunm"], "output": "password change successfully,please login again"})
            else:
                return render(request, "cpmyadmin,html", {"sunm": request.session["sunm"], "output": "New & confirm password mismatch,try again"})
        else:
            return render(request, "cpmyadmin.html", {"sunm": request.session["sunm"], "output": "Invalid old password,please try again"})
