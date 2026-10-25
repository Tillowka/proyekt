from django.shortcuts import render,redirect,get_object_or_404
from .models import Product, ProductRequest, ProductRequestSystem,UserProfile, ProductRequestAdmin
from admins.forms import ProductRequestForm, createProductForm,editProductForm,CreateUserForm,editUserForm
from django.contrib.auth.models import User
from django.utils import timezone

def index(request):
    products = Product.objects.all()
    context = {
        'products':products
    }
    return render(request, 'index.html',context)

    
    
    
    

def admin_page(request):
    if not request.user.is_authenticated:
        return redirect('login')

    profile = getattr(request.user, 'userprofile', None)

    if profile is None:
        return redirect('login')

    if profile.role == 'boshliq':

        return render(request, 'boshliq/home.html')

    elif profile.role == 'admin':
        return render(request, 'admin/base_admin.html')

    elif profile.role == 'sotuvchi':
        return render(request, 'sotuvchi/home.html')

    return redirect('login')

def shop(request):
    return render(request, 'shop.html')

def table_page(request):
    product = Product.objects.all()
    context = {
        'product':product

    }
    return render(request, 'admin/base_table.html',context)

def create_table(request):
    if request.method == 'POST':
        form = createProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('table_page')
    else:
        form = createProductForm()
    return render(request, 'admin/create.html', {'form': form})

def delete_product(request, pk):
    products = Product.objects.get(pk=pk)
    products.delete()
    return redirect('table_page')



def edit_product(request, pk):
    products = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = editProductForm(request.POST, request.FILES, instance=products)
        if form.is_valid():
            form.save()
            return redirect('table_page')
    else:
        form = editProductForm(instance=products)
    return render(request, 'admin/edit.html', {'form': form})

def create_user(request):
    if not request.user.is_authenticated:
        return redirect('index')

    profile = getattr(request.user, 'userprofile', None)
    if profile is None or profile.role not in ['boshliq', 'admin']:
        return redirect('admin_page')

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']
            raiting = form.cleaned_data['raiting']
            phonenumber = form.cleaned_data['phonenumber']

            if User.objects.filter(username=username).exists():
                form.add_error('username', 'This username already exists.')
            else:
                user = User.objects.create_user(username=username, password=password)
                UserProfile.objects.create(phonenumber=phonenumber, user=user, role=role, raiting=raiting)
                return redirect('boshliq_page')
    else:
        form = CreateUserForm()

    return render(request, 'create_user.html', {'form': form})

def admins(request):
    admin_soni = UserProfile.objects.filter(role='admin').count()
    sotuvchi_soni = UserProfile.objects.filter(role='sotuvchi').count()
    product_soni = Product.objects.count()
    foydalanuvchilar = UserProfile.objects.all()
    profile = getattr(request.user, 'userprofile', None)
    
    context = {
        'admin_soni': admin_soni,
        'sotuvchi_soni': sotuvchi_soni,
        'product_soni': product_soni,
        'username': request.user.username,
        'foydalanuvchilar': foydalanuvchilar,
        'profile': profile,
    }
    return render(request, 'boshliq/admins.html', context)
    
def hisobot(request):
    product_soni = Product.objects.count()
    admin_soni = UserProfile.objects.filter(role='admin').count()
    sotuvchi_soni = UserProfile.objects.filter(role='sotuvchi').count()
    context = {
        'product_soni': product_soni,
        'admin_soni': admin_soni,
        'sotuvchi_soni': sotuvchi_soni,
        'username': request.user.username,
    }
    return render(request, 'boshliq/hisobot.html', context)

def foydalanuvchilar(request):
    return render(request, 'boshliq/users.html')

def boshliq_page(request):
    return render(request, 'boshliq/home.html')

def edit_user(request, pk):
    
    profile = UserProfile.objects.get(user__pk=pk)
    if request.method == 'POST':
        form = editUserForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('admins')
    else:
        form = editUserForm(instance=profile)
    return render(request, 'boshliq/edit_user.html', {'form': form, 'profile': profile})

def delete_user(request, pk):
    user = User.objects.get(pk=pk)
    user.delete()

    return redirect('admins')




def seller_page(request):

    requests = ProductRequest.objects.filter(user=request.user.userprofile).select_related(
        'admin_data', 'system_data'
    )
    
    if request.method == 'POST':

        form = ProductRequestForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            productrequest = form.save(commit=False)
            productrequest.user = request.user.userprofile
            
            productrequest.save()
            ProductRequestSystem.objects.create(
                product_request=productrequest,
                status='pending'
            )
          
        
            return redirect('sotuvchi_page')

    else:
        form = ProductRequestForm()

    context = {
        'form': form,
        'requests': requests,
        
    }

    return render(
        request,
        'sotuvchi/product_jonatish.html',
        context
    )

def product_requests(request):

    requests = ProductRequest.objects.filter(
        system_data__status='pending'
    ).select_related(
        'user',
        'system_data',
        'admin_data__tekshirgan'
    )

    done = ProductRequest.objects.filter(
        system_data__status__in=[
            'need_fix',
            'approved',
            'rejected'
        ]
    ).select_related(
        'user',
        'system_data',
        'admin_data__tekshirgan'
    )

    return render(
        request,
        'admin/admin_requests.html',
        {
            'requests': requests,
            'done': done
        }
    )
def qabul_product(request, pk):
    product = get_object_or_404(ProductRequest, pk=pk)

    system = product.system_data
    system.status = "approved"
    system.save()

    admin_data, created = ProductRequestAdmin.objects.get_or_create(
        product_request=product
    )

    admin_data.tekshirgan = request.user
    admin_data.tekshirilganvaqt = timezone.now()
    admin_data.save()

    return redirect('product_requests')

def rad_product(request, pk):
    product = get_object_or_404(ProductRequest, pk=pk)
    system = product.system_data
    system.status = "rejected"
    system.save()
    admin_data, created = ProductRequestAdmin.objects.get_or_create(
        product_request=product
    )
    admin = product.admin_data
    admin.admin_comment = "Tovaringiz qabul qilinmadi!"
    admin.save()

    admin_data.tekshirgan = request.user
    admin_data.tekshirilganvaqt = timezone.now()
    admin_data.save()

    return redirect('product_requests')





def tuzatish_product(request, pk):
    product = get_object_or_404(ProductRequest, pk=pk)

    system = product.system_data
    system.status = "need_fix"
    system.save()

    admin_comment = request.POST.get('admin_comment', '')

    admin_data, created = ProductRequestAdmin.objects.get_or_create(
        product_request=product
    )

    admin_data.admin_comment = admin_comment
    admin_data.save()
    product.admin_data.tekshirgan = request.user
    product.admin_data.tekshirilganvaqt = timezone.now()
    product.admin_data.save()

    return redirect('product_requests')
