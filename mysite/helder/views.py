import os
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate , login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib.auth.models import User
from .models import Category, Pattern,Photo,Type
from PIL import Image
# from rest_framework import viewsets
# from .serializers import PhotoSerializer
# from django.utils.datastructures import MultiValueDictKeyError

# def error_404_view(request, exception):

#     # we add the path to the the 404.html file
#     # here. The name of our HTML file is 404.html
#     return render(request, '404.html')
# # login page
# class PhotoViewset(viewsets.ModelViewSet):
#     queryset=User.objects.all()
#     serializer_class=PhotoSerializer


def loginadmin(request):
    if request.method=="POST":
        uname=request.POST['uname']
        pwd=request.POST['pwd']
        user=authenticate(request,username=uname,password=pwd)
        print(user,"hhh")
        if user:
            if user.is_staff==1:
                login(request,user)
                return redirect('adhome')
        messages.error(request, 'Incorrect username or Password', extra_tags='text-danger')
    return render(request, "login.html")

# logout button
def logoutUser(request):
    logout(request)
    return redirect('login')

# addproduct page
@login_required(login_url='login')
def addPhoto(request):
    user = request.user

    categories = user.category_set.all()
    patterns = Pattern.objects.all()
    typess=Type.objects.all()


    # try:
    #     imgname = request.POST['imgname']
    # except MultiValueDictKeyError:
    #     imgname = False

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        image4 = request.FILES.get('image4')

        date = datetime.datetime.now()#.strftime('%H:%M:%S')
        dtls4 = data['dtls4']
        pattern = Pattern.objects.get(id=data['pattern'])
        types = Type.objects.get(id=data['type'])
        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
            name=category
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                user=user,
                name=data['category_new'])

            name=data['category_new']
        else:
            category = None

        im = Image.open(image)
        if im.size<(750,1000):
            messages.error(request, 'incorrect image width or height', extra_tags='text-danger')
        else:
            Photo.objects.create(
            category=category,
            pattern=pattern,
            types=types,
            name=name,
            date=date,
            size=data['size'],
            imgname=data['imgname'],
            description=data['description'],
            detail1=data['fabric'],
            detail2=types,
            detail3=pattern,
            detail4=dtls4,
            detail5=data['dtls5'],
            image=image,
            image1=image1,
            image2=image2,
            image3=image3,
            image4=image4,
            )
            messages.success(request, "Data inserted successfully")
            return redirect('addph')
    context = {'categories': categories,'typess':typess,'patterns':patterns}
    return render(request, 'helderadd.html', context)

    #admin home view
@login_required(login_url='login')
def adminhome(request):
    if request.method == 'GET':
        user = request.user
        category = request.GET.get('category')
        if category == None:
            photo = Photo.objects.filter(category__user=user)
        else:
            photo = Photo.objects.filter(
                category__name=category, category__user=user)

        categories = Category.objects.filter(user=user)
        photos=photo.order_by('-date')
        context = {'categories': categories, 'photos': photos}
        return render(request, 'helderhome.html', context)
    elif request.method == 'POST':
        user = request.user
        data = request.POST
        if data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                user=user,
                name=data['category_new'])

        else:
            category = None
        return redirect("adhome")



def delb(request,id):

    bks=Photo.objects.get(id=id)
    os.remove(bks.image.path)
    os.remove(bks.image1.path)
    os.remove(bks.image2.path)
    os.remove(bks.image3.path)
    os.remove(bks.image4.path)

    bks.delete()
    messages.success(request, "product removed successfully")
    return redirect("adhome")

    #edit page
@login_required(login_url='login')
def form2Photo(request,pk):
    user = request.user

    categories = user.category_set.all()
    patterns= Pattern.objects.all()
    typess=Type.objects.all()
    # user = request.user
    photos = Photo.objects.get(id=pk)

    # categories = user.category_set.all()
    if request.method=="GET":
        photos = Photo.objects.get(id=pk)
        context = {'categories': categories,'typess':typess,'patterns':patterns,'photos':photos}
        context['data']=photos
        return render(request,'helderedit.html',context)

    elif request.method=="POST":

        #   #for image edit

        data = request.POST
        date = datetime.datetime.now()
        name1=photos.name
        pattern = Pattern.objects.get(id=data['pattern'])
        types = Type.objects.get(id=data['type'])
        dtls4 = data['dtls4']
        ij=request.FILES.get('image')
        try:
            im = Image.open(ij)
            if im.size<(750,1000):
                messages.error(request, 'incorrect image width or height', extra_tags='text-danger')
            else:
                if request.FILES.get('image')!=None:
                    os.remove(photos.image.path)
                    image = request.FILES.get('image')
                else:
                    image=photos.image
                if request.FILES.get('image1')!=None:
                    os.remove(photos.image1.path)
                    image1 = request.FILES.get('image1')

                else:
                    image1=photos.image1
                if request.FILES.get('image2')!=None:
                    os.remove(photos.image2.path)
                    image2 = request.FILES.get('image2')

                else:
                    image2=photos.image2
                if request.FILES.get('image3')!=None:
                    os.remove(photos.image3.path)
                    image3 = request.FILES.get('image3')

                else:
                    image3=photos.image3
                if request.FILES.get('image4')!=None:
                    os.remove(photos.image4.path)
                    image4 = request.FILES.get('image4')

                else:
                    image4=photos.image4


                Photo.objects.create(
                    category=photos.category,
                    pattern=pattern,
                    types=types,
                    imgname=data['imgname'],
                    name=name1,
                    description=data['description'],
                    date=date,
                    size=data['size'],
                    detail1=data['fabric'],
                    detail2=types,
                    detail3=pattern,
                    detail4=dtls4,
                    detail5=data['dtls5'],
                    image=image,
                    image1=image1,
                    image2=image2,
                    image3=image3,
                    image4=image4,
                    )
                bks=Photo.objects.get(id=pk)
                bks.delete()
                messages.success(request, "prodect details updated")
        except:
            if request.FILES.get('image')!=None:
                os.remove(photos.image.path)
                image = request.FILES.get('image')
            else:
                image=photos.image
            if request.FILES.get('image1')!=None:
                os.remove(photos.image1.path)
                image1 = request.FILES.get('image1')

            else:
                image1=photos.image1
            if request.FILES.get('image2')!=None:
                os.remove(photos.image2.path)
                image2 = request.FILES.get('image2')

            else:
                image2=photos.image2
            if request.FILES.get('image3')!=None:
                os.remove(photos.image3.path)
                image3 = request.FILES.get('image3')

            else:
                image3=photos.image3
            if request.FILES.get('image4')!=None:
                os.remove(photos.image4.path)
                image4 = request.FILES.get('image4')

            else:
                image4=photos.image4


            Photo.objects.create(
                    category=photos.category,
                    pattern=pattern,
                    types=types,
                    imgname=data['imgname'],
                    name=name1,
                    description=data['description'],
                    date=date,
                    size=data['size'],
                    detail1=data['fabric'],
                    detail2=types,
                    detail3=pattern,
                    detail4=dtls4,
                    detail5=data['dtls5'],
                    image=image,
                    image1=image1,
                    image2=image2,
                    image3=image3,
                    image4=image4,
                    )
            bks=Photo.objects.get(id=pk)
            bks.delete()
            messages.success(request, "prodect details updated")
        return redirect('adhome')

def product(request):
    category = request.GET.get('category')
    if request.method == 'GET':

        top = Category.objects.filter(tb='top')
        bottom=Category.objects.filter(tb='bottom')
        kids=Category.objects.filter(tb='kids')
        category = request.GET.get('category')
        if category == None:
            photos = Photo.objects.all().order_by('-date')[:12]
        else:
            photos = Photo.objects.all().order_by('-date')[:12]
        # photos=photo.order_by('-date')
        context = {'top': top,'bottom': bottom,'kids' : kids, 'photos': photos}

    return render(request, 'products.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def topwear(request):
    if request.method == 'GET':

        top = Category.objects.filter(tb='top')
        bottom=Category.objects.filter(tb='bottom')
        kids=Category.objects.filter(tb='kids')
        category = request.GET.get('category')
        patterns=Pattern.objects.all()
        types=Type.objects.all()
        if category == None:

            photo = Photo.objects.filter(category__tb='top')
        else:
            photo = Photo.objects.filter(category__name=category)
        photos=photo.order_by('-date')

        context = {'top': top,'bottom': bottom,'kids' : kids, 'photos': photos,'patterns':patterns,'types':types}
    elif request.method == 'POST':
        top = Category.objects.filter(tb='top')
        bottom=Category.objects.filter(tb='bottom')
        kids=Category.objects.filter(tb='kids')
        category = request.GET.get('category')
        patterns=Pattern.objects.all()
        types=Type.objects.all()
        pat=request.POST.get('pattern')
        typ=request.POST.get('type')
        sleev=request.POST.get('dtls4')
        if category == None:
            if sleev=='NONE':
                if pat=='6' and typ=='4':
                    photos = Photo.objects.filter(category__tb='top')[:12]
                elif pat!='6' and typ=='4':
                    photos = Photo.objects.filter(pattern_id=pat,category__tb='top')
                elif pat=='6' and typ!='4':
                    photos = Photo.objects.filter(types_id=typ,category__tb='top')
                elif pat!='6' and typ!='4':
                    photos = Photo.objects.filter(pattern_id=pat,types_id=typ,category__tb='top')
            else:
                if pat=='6' and typ=='4':
                    photos = Photo.objects.filter(category__tb='top',detail4=sleev)[:12]
                elif pat!='6' and typ=='4':
                    photos = Photo.objects.filter(pattern_id=pat,category__tb='top',detail4=sleev)
                elif pat=='6' and typ!='4':
                    photos = Photo.objects.filter(types_id=typ,category__tb='top',detail4=sleev)
                elif pat!='6' and typ!='4':
                    photos = Photo.objects.filter(pattern_id=pat,types_id=typ,category__tb='top',detail4=sleev)
        else:
            if sleev=='NONE':
                if pat=='6' and typ=='4':
                    photos = Photo.objects.filter(category__tb='top',category__name=category)[:12]
                elif pat!='6' and typ=='4':
                    photos = Photo.objects.filter(pattern_id=pat,category__tb='top',category__name=category)
                elif pat=='6' and typ!='4':
                    photos = Photo.objects.filter(types_id=typ,category__tb='top',category__name=category)
                elif pat!='6' and typ!='4':
                    photos = Photo.objects.filter(pattern_id=pat,types_id=typ,category__tb='top',category__name=category)
            else:
                if pat=='6' and typ=='4':
                    photos = Photo.objects.filter(category__tb='top',detail4=sleev,category__name=category)[:12]
                elif pat!='6' and typ=='4':
                    photos = Photo.objects.filter(pattern_id=pat,category__tb='top',detail4=sleev,category__name=category)
                elif pat=='6' and typ!='4':
                    photos = Photo.objects.filter(types_id=typ,category__tb='top',detail4=sleev,category__name=category)
                elif pat!='6' and typ!='4':
                    photos = Photo.objects.filter(pattern_id=pat,types_id=typ,category__tb='top',detail4=sleev,category__name=category)


        context = {'photos': photos,'patterns':patterns,'types':types,'top': top,'bottom': bottom,'kids' : kids}
    return render(request, 'category.html',context)

def bottom(request):
    if request.method == 'GET':
        filter='bottom'
        top = Category.objects.filter(tb='top')
        bottom=Category.objects.filter(tb='bottom')
        kids=Category.objects.filter(tb='kids')
        category = request.GET.get('category')
        patterns=Pattern.objects.all()
        types=Type.objects.all()
        if category == None:
            photo = Photo.objects.filter(category__tb='bottom')
        else:
            photo = Photo.objects.filter(category__name=category)
        photos=photo.order_by('-date')

        context = {'top': top,'bottom': bottom,'kids' : kids, 'photos': photos,'patterns':patterns,'types':types,'filter':filter}
    elif request.method == 'POST':
        top = Category.objects.filter(tb='top')
        bottom=Category.objects.filter(tb='bottom')
        kids=Category.objects.filter(tb='kids')
        category = request.GET.get('category')
        patterns=Pattern.objects.all()
        types=Type.objects.all()
        pat=request.POST.get('pattern')
        typ=request.POST.get('type')
        if pat=='6' and typ=='4':
            photos = Photo.objects.filter(category__tb='bottom')[:12]
        elif pat!='6' and typ=='4':
            photos = Photo.objects.filter(pattern_id=pat,category__tb='bottom')
        elif pat=='6' and typ!='4':
            photos = Photo.objects.filter(types_id=typ,category__tb='bottom')
        elif pat!='6' and typ!='4':
            photos = Photo.objects.filter(pattern_id=pat,types_id=types,category__tb='bottom')
        context = {'photos': photos,'patterns':patterns,'types':types,'top': top,'bottom': bottom,'kids' : kids}
    return render(request, 'category.html',context)

def kids(request):
    if request.method == 'GET':
        top = Category.objects.filter(tb='top')
        bottom=Category.objects.filter(tb='bottom')
        kids=Category.objects.filter(tb='kids')
        category = request.GET.get('category')
        patterns=Pattern.objects.all()
        types=Type.objects.all()
        if category == None:
            photo = Photo.objects.filter(category__tb='kids')
        else:
            photo = Photo.objects.filter(category__name=category,category__tb='kids')
        photos=photo.order_by('-date')

        context = {'top': top,'bottom': bottom,'kids' : kids, 'photos': photos,'patterns':patterns,'types':types}
    elif request.method == 'POST':
        print('hi')
        top = Category.objects.filter(tb='top')
        bottom=Category.objects.filter(tb='bottom')
        kids=Category.objects.filter(tb='kids')
        category = request.GET.get('category')
        patterns=Pattern.objects.all()
        types=Type.objects.all()
        pat=request.POST.get('pattern')
        typ=request.POST.get('type')
        sleev=request.POST.get('dtls4')
        if category == None:
            if sleev=='NONE':
                if pat=='6' and typ=='4':
                    photos = Photo.objects.filter(category__tb='kids')[:12]
                elif pat!='6' and typ=='4':
                    photos = Photo.objects.filter(pattern_id=pat,category__tb='kids')
                elif pat=='6' and typ!='4':
                    photos = Photo.objects.filter(types_id=typ,category__tb='kids')
                elif pat!='6' and typ!='4':
                    photos = Photo.objects.filter(pattern_id=pat,types_id=typ,category__tb='kids')
            else:
                if pat=='6' and typ=='4':
                    photos = Photo.objects.filter(category__tb='kids',detail4=sleev)[:12]
                elif pat!='6' and typ=='4':
                    photos = Photo.objects.filter(pattern_id=pat,category__tb='kids',detail4=sleev)
                elif pat=='6' and typ!='4':
                    photos = Photo.objects.filter(types_id=typ,category__tb='kids',detail4=sleev)
                elif pat!='6' and typ!='4':
                    photos = Photo.objects.filter(pattern_id=pat,types_id=typ,category__tb='kids',detail4=sleev)
        else:
            if sleev=='NONE':
                if pat=='6' and typ=='4':
                    photos = Photo.objects.filter(category__tb='kids',category__name=category)[:12]
                elif pat!='6' and typ=='4':
                    photos = Photo.objects.filter(pattern_id=pat,category__tb='kids',category__name=category)
                elif pat=='6' and typ!='4':
                    photos = Photo.objects.filter(types_id=typ,category__tb='kids',category__name=category)
                elif pat!='6' and typ!='4':
                    photos = Photo.objects.filter(pattern_id=pat,types_id=typ,category__tb='kids',category__name=category)
            else:
                if pat=='6' and typ=='4':
                    photos = Photo.objects.filter(category__tb='kids',detail4=sleev,category__name=category)[:12]
                elif pat!='6' and typ=='4':
                    photos = Photo.objects.filter(pattern_id=pat,category__tb='kids',detail4=sleev,category__name=category)
                elif pat=='6' and typ!='4':
                    photos = Photo.objects.filter(types_id=typ,category__tb='kids',detail4=sleev,category__name=category)
                elif pat!='6' and typ!='4':
                    photos = Photo.objects.filter(pattern_id=pat,types_id=typ,category__tb='kids',detail4=sleev,category__name=category)


        context = {'photos': photos,'patterns':patterns,'types':types,'top': top,'bottom': bottom,'kids' : kids,}
    return render(request, 'category.html',context)



def index(request):
    categories = Category.objects.all()
    top= Photo.objects.filter(category__tb='top').order_by('-date')[:3]
    bottom = Photo.objects.filter(category__tb='bottom').order_by('-date')[:2]
    context = {'categories': categories,'top':top,'bottom':bottom}
    return render(request, 'index.html', context)