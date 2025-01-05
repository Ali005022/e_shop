from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User
from .models import Profile  

from .models import Product, Order, Cart, Category
from .forms import ProductForm  # Assuming you have this form defined

# Decorator for admin staff check
def staff_member_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        return redirect('login')  # Redirect to login if not authenticated or not staff
    return _wrapped_view

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ProductForm, DiscountForm  
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ProductForm, DiscountForm, ProductEditForm
from .models import Product, Order, Category
from django.utils.decorators import method_decorator

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ProductForm, ProductEditForm, DiscountForm
from .models import Product, Order, User, Category

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Product, Order, Category, User
from .forms import ProductForm, ProductEditForm, DiscountForm
from django.db.models import Sum
import json

@method_decorator([login_required, staff_member_required], name='dispatch')
class AdminDashboardView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        orders = Order.objects.all().order_by('-date')[:5]  # Latest 5 orders
        users = User.objects.all()
        categories = Category.objects.all()
        total_sales = Order.objects.filter(is_paid=True).aggregate(total=Sum('total'))['total'] or 0

        # Count data
        order_count = orders.count()
        product_count = products.count()
        user_count = users.count()
        category_count = categories.count()

        # Prepare data for chart
        chart_data = json.dumps({
            'products': product_count,
            'orders': order_count,
            'users': user_count,
            'categories': category_count
        })

        form = ProductForm()  # Form for adding new product
        discount_form = DiscountForm()  # Form for bulk discount
        edit_form = None  # Default: No product is being edited

        # Check if editing a product
        product_id = request.GET.get('edit_product')
        if product_id:
            product = get_object_or_404(Product, id=product_id)
            edit_form = ProductEditForm(instance=product)

        context = {
            'products': products,
            'orders': orders,
            'users': users,
            'categories': categories,
            'total_sales': total_sales,
            'order_count': order_count,
            'product_count': product_count,
            'user_count': user_count,
            'category_count': category_count,
            'form': form,
            'discount_form': discount_form,
            'edit_form': edit_form,  # Add edit form to context
            'chart_data': chart_data  # Send chart data to template
        }
        return render(request, 'store/admin_dashboard.html', context)

    def post(self, request, *args, **kwargs):
        if 'add_product' in request.POST:  # Add new product request
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Product added successfully.')
            else:
                messages.error(request, 'Failed to add product.')
        
        elif 'delete_product' in request.POST:  # Delete product request
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            product.delete()
            messages.success(request, 'Product deleted successfully.')

        elif 'remove_discount' in request.POST:  # Remove discount request
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            product.discount = 0  # Remove the discount
            product.save()
            messages.success(request, f"Discount removed from {product.name} successfully.")

        elif 'update_discount' in request.POST:  # Update discount request
            product_id = request.POST.get('product_id')
            discount = request.POST.get('discount')
            product = get_object_or_404(Product, id=product_id)
            
            if discount.isdigit() and 0 <= int(discount) <= 100:
                product.discount = int(discount)
                product.save()
                messages.success(request, f"Discount for {product.name} updated successfully.")
            else:
                messages.error(request, "Discount value must be between 0 and 100.")

        elif 'apply_bulk_discount' in request.POST:  # Apply bulk discount
            discount = request.POST.get('bulk_discount')
            if discount.isdigit() and 0 <= int(discount) <= 100:
                Product.objects.update(discount=int(discount))
                messages.success(request, f"Bulk discount of {discount}% applied to all products.")
            else:
                messages.error(request, "Discount value must be between 0 and 100.")
        
        elif 'edit_product' in request.POST:  # Handle product update
            product_id = request.POST.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            form = ProductEditForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, f"Product {product.name} updated successfully.")
            else:
                messages.error(request, "Failed to update product.")
        
        return redirect('admin_dashboard')

@method_decorator(login_required, name='dispatch')
class UserDashboardView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login if not authenticated
        
        cart = Cart.objects.filter(user=request.user).first()
        orders = Order.objects.filter(user=request.user)
        
        context = {
            'cart': cart,
            'orders': orders,
        }
        return render(request, 'store/user_dashboard.html', context)

# Search view for products
from django.views.generic import ListView

class SearchView(ListView):
    model = Product
    template_name = 'store/search_results.html'  # Search results template
    context_object_name = 'results'  # Context variable for template
    paginate_by = 10  # Number of results per page

    def get_queryset(self):
        query = self.request.GET.get('q', '')  # Get search query from URL
        if query:
            return Product.objects.filter(name__icontains=query)  # Search by product name
        return Product.objects.none()  # Return no results if no query
from django.urls import reverse
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
import random
from .models import Product, Cart, CartItem, Category, Profile, Order
from .forms import ProductForm, RegisterForm, SignUpForm, UserProfileForm
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView


class HomeView(View):
    def get(self, request, *args, **kwargs):
        featured_products = Product.objects.all()
        return render(request, 'store/home.html', {'featured_products': featured_products})


class CategoryListView(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'categories.html', {'categories': categories})


class ProductListView(ListView):
    model = Product
    template_name = 'store/products.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        category_id = self.request.GET.get('category', None)
        queryset = Product.objects.all()
        if query:
            queryset = queryset.filter(name__icontains=query)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context





class VerifyLoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'store/verify_login.html')

    def post(self, request, *args, **kwargs):
        input_code = request.POST.get('verification_code')
        actual_code = request.session.get('verification_code')

        if input_code == str(actual_code):
            email = request.session.get('email')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return HttpResponse("User with this email does not exist.")
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Invalid verification code.")


@method_decorator(login_required, name='dispatch')
class CartView(View):
    def get(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.cartitem_set.all()
        except Cart.DoesNotExist:
            cart_items = []
        return render(request, 'store/cart.html', {'cart_items': cart_items, 'cart': cart})


class AddToCartView(View):
    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity

        cart_item.save()
        return redirect('cart')


class UpdateCartItemView(View):
    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id)
        new_quantity = int(request.POST.get('quantity'))
        if new_quantity > 0:
            item.quantity = new_quantity
            item.save()
        return redirect('cart')


class RemoveFromCartView(View):
    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id)
        item.delete()
        return redirect('cart')


@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)
        if cart.items.all().count() > 0:
            cart.delete()
            return render(request, 'store/success.html')
        else:
            return render(request, 'store/cart.html', {'error': 'Your cart is empty.'})


class AddProductView(View):
    def get(self, request, *args, **kwargs):
        form = ProductForm()
        return render(request, 'store/add_product.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('products'))
        return render(request, 'store/add_product.html', {'form': form})


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'store/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            profile = Profile.objects.create(user=user)
            profile.email = form.cleaned_data.get('email')
            profile.phone_number = form.cleaned_data.get('phone_number')
            profile.save()

            messages.success(request, 'Registration successful.')
            return redirect(reverse('login'))
        else:
            messages.error(request, 'Please check the form for errors.')

        return render(request, 'store/register.html', {'form': form})


class VerifyView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'store/verify.html')

    def post(self, request, *args, **kwargs):
        email = request.session.get('email')
        verification_code = request.POST.get('verification_code')
        if int(verification_code) == request.session.get('verification_code'):
            user = authenticate(username=email, password='defaultpassword')
            if user is None:
                user = User.objects.create_user(username=email, email=email, password='defaultpassword')
            login(request, user)
            return redirect(reverse('products'))
        else:
            return render(request, 'store/verify.html', {'error': 'Invalid verification code.'})


class UserProfileView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        form = UserProfileForm(instance=request.user.profile)
        cart = Cart.objects.filter(user=request.user).first()
        orders = Order.objects.filter(user=request.user)

        context = {
            'form': form,
            'cart': cart,
            'orders': orders,
        }
        return render(request, 'store/user_profile.html', context)

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(request.POST, instance=request.user.profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('user_profile')
        else:
            messages.error(request, 'Please check the form for errors.')

        return render(request, 'store/user_profile.html', {'form': form})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('login'))


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'


class OrderHistoryView(View):
    def get(self, request, *args, **kwargs):
        user_orders = Order.objects.filter(user=request.user)
        return render(request, 'store/order_history.html', {'orders': user_orders})
    




class CustomLoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'store/login.html')

    def post(self, request, *args, **kwargs):
        identifier = request.POST.get('identifier')  # Could be email, phone, or username
        password = request.POST.get('password')

        # ابتدا چک می‌کنیم که ورودی آیا ایمیل است
        if "@" in identifier:
            # اگر ایمیل باشد، تلاش برای احراز هویت با ایمیل
            user = authenticate(request, username=identifier, password=password)
        elif identifier.isdigit():  # اگر ورودی شماره تلفن باشد
            # تلاش برای پیدا کردن کاربری با شماره تلفن
            try:
                profile = Profile.objects.get(phone_number=identifier)
                user = authenticate(request, username=profile.user.username, password=password)
            except Profile.DoesNotExist:
                user = None
        else:  # در غیر اینصورت ورودی نام کاربری است
            user = authenticate(request, username=identifier, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Invalid credentials.")
        from django.views.generic import ListView
from .models import Category

class CategoryListView(ListView):
    model = Category
    template_name = 'store/category_list.html'  # نام قالب مربوط به دسته‌بندی‌ها
    context_object_name = 'categories'  # نام متغیر در قالب

from django.views.generic import ListView
from .models import Product, Category

class CategoryProductListView(ListView):
    model = Product
    template_name = 'store/category_products.html'  # نام قالب محصولات یک دسته
    context_object_name = 'products'  # نام متغیر در قالب

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Product.objects.filter(category_id=category_id)
    

    from django.views.generic import ListView
from .models import Product

class FeaturedProductListView(ListView):
    model = Product
    template_name = 'store/featured_products.html'  # نام قالب محصولات ویژه
    context_object_name = 'products'  # نام متغیر در قالب

    def get_queryset(self):
        return Product.objects.filter(discount__gt=0)  # محصولات با تخفیف بیشتر از صفر
    

    # store/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import ProductEditForm
from .models import Product

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductEditForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "محصول با موفقیت ویرایش شد.")
            return redirect('admin_dashboard')  # پس از ویرایش، به داشبورد مدیریت برگردیم
        else:
            messages.error(request, "خطا در ویرایش محصول.")
    else:
        form = ProductEditForm(instance=product)

    return render(request, 'store/edit_product.html', {'form': form, 'product': product})


# e_shop/store/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from .models import Product
from .forms import ProductEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

@method_decorator([login_required, staff_member_required], name='dispatch')
class ProductEditView(View):
    def get(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, id=product_id)
        form = ProductEditForm(instance=product)

        return render(request, 'store/edit_product.html', {'form': form, 'product': product})

    def post(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, id=product_id)
        form = ProductEditForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            messages.success(request, f'Product {product.name} updated successfully.')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Failed to update product.')

        return render(request, 'store/edit_product.html', {'form': form, 'product': product})



