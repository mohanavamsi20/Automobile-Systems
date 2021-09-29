from django.shortcuts import render, redirect, get_object_or_404

from django.views import View
from django.views.generic.base import TemplateResponseMixin

from .forms import SellCarModelForm, BuyCarModelForm
from django.contrib import messages
from home.models import User
from models.models import Make, Model, Variant
from .models import BuyCar, SellCar
from .filters import ShopCarFilter
from django.core.paginator import Paginator

import smtplib, ssl

# Create your views here.
def render_shop(request):
    template_name = 'shop/home.html'
    return render(request, template_name)

class SellCreateView(View):
    template_name = 'shop/sell_oldcar.html'

    def get(self, request, *args, **kwargs):
        if 'username' in request.session:
            form = SellCarModelForm()
            context = {"form": form}
            return render(request, self.template_name, context)
        return redirect('/login')

    def post(self, request, *args, **kwargs):
        if 'username' in request.session:
            form = SellCarModelForm(request.POST, request.FILES)
            context = {"form": form}
            if form.is_valid():
                form.save()
                mailSeller(request, form)
                form = SellCarModelForm()
                context = {"form": form}
                messages.info(request, 'Your product is online Check your gmail for more info')
                list(messages.get_messages(request))
                return render(request, self.template_name, context)
            return render(request, self.template_name, context)
        return redirect('/login')

def load_models(request):
    make_id = request.GET.get('make_id')
    models = Model.objects.filter(make_id=make_id).all()
    return render(request, 'shop/model_dropdown_list_options.html', {'models': models})

def load_variants(request):
    model_id = request.GET.get('model_id')
    variants = Variant.objects.filter(model_id=model_id).all()
    return render(request, 'shop/variant_dropdown_list_options.html', {'variants': variants})

def mailSeller(request, form):
    if 'username' in request.session:
        sender = "",
        password = ""
        with open("shop/static/credentials.txt", "r") as f:
            file = f.readlines()
            sender = file[0].strip()
            password = file[1].strip()
        port = 465
        fullname = form.cleaned_data['fullname']
        make = form.cleaned_data['make']
        model = form.cleaned_data['model']
        variant = form.cleaned_data['variant']
        price = form.cleaned_data['price']
        receiver = form.cleaned_data['email']
        print(sender, password)
        print(receiver)
        sent_body = ("Hello, Mr./Ms."+ fullname + " Your automobile sale is live \n"
                    "Make: " + str(make) + "\n"
                    "Model: " + str(model) + "\n"
                    "Variant: " + str(variant) + "\n"
                     "Price: "+ str(price) +"\n"+"\n"
                     "Contact us for queries\n"
                     "Team AMG")
        email_text = """\From: %s

                %s
                """ % (sender,  sent_body)
        context = ssl.create_default_context()
        print("Starting to send")
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, email_text)
        print("Email sent!")
        return
    return redirect('/login')

def render_buy(request):
    template_name = 'shop/buy_oldcar.html'
    if request.method == 'GET':
        objects = SellCar.objects.filter(status='True')
        myFilter = ShopCarFilter(request.POST, queryset=objects)
        objects = myFilter.qs
        page_num = request.GET.get('page')
        models_paginator = Paginator(objects, 6)
        page = models_paginator.get_page(page_num)
        context = {"objects": objects, 'myFilter': myFilter, 'count': models_paginator.count, 'page': page}
        return render(request, template_name, context)
    if request.method == 'POST':
        if 'username' in request.session:
            objects = SellCar.objects.filter(status='True')
            myFilter = ShopCarFilter(request.POST, queryset=objects)
            objects = myFilter.qs
            page_num = request.GET.get('page')
            models_paginator = Paginator(objects, 6)
            page = models_paginator.get_page(page_num)
            context = {"objects": objects, 'myFilter': myFilter, 'count': models_paginator.count, 'page': page}
            return render(request, template_name, context)
        return redirect('/login')
    return render(request, template_name)

def product_detail(request,id):
    template_name = 'shop/details.html'
    if request.method == 'GET':
        car = get_object_or_404(SellCar,id=id)
        context = {'car':car}
        return render(request, template_name, context)
    if request.method == 'POST':
        if 'username' in request.session:
            car = get_object_or_404(SellCar, id=id)
            user = User.objects.get(email=request.session.get('username'))
            form = BuyCarModelForm(request.POST)
            context = {}
            context['car'] = car
            context['user'] = user
            if form.is_valid():
                att = form.save(commit=False)
                att.car = context['car']
                att.user = context['user']
                car.status = False
                car.save()
                form.save()
                messages.info(request, 'You have ordered this car')
                list(messages.get_messages(request))
                return render(request, template_name, context)
            return render(request,template_name)
        return redirect('/login')

def your_sales(request):
    template_name='shop/sales.html'
    if 'username' in request.session:
        if request.method == 'GET':
            sales = SellCar.objects.filter(email=request.session.get('username'))
            myFilter = ShopCarFilter(request.POST, queryset=sales)
            objects = myFilter.qs
            page_num = request.GET.get('page')
            models_paginator = Paginator(objects, 6)
            page = models_paginator.get_page(page_num)
            context = {"objects":objects,'myFilter': myFilter, 'count': models_paginator.count, 'page': page}
            return render(request, template_name, context)
        return render(request, template_name)
    return redirect('/login')

def your_orders(request):
    template_name='shop/orders.html'
    if 'username' in request.session:
        if request.method == 'GET':
            user = User.objects.get(email=request.session.get('username'))
            objects = BuyCar.objects.filter(user=user)
            page_num = request.GET.get('page')
            models_paginator = Paginator(objects, 6)
            page = models_paginator.get_page(page_num)
            context = {"objects":objects, 'count': models_paginator.count, 'page': page}
            return render(request, template_name, context)
        return render(request, template_name)
    return redirect('/login')