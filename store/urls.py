# store/urls.py

from django.urls import path
from .views import (
    HomeView, RegisterView, VerifyView, UserProfileView, VerifyLoginView,
    ProductListView, CartView, AddToCartView, CheckoutView, AddProductView, OrderHistoryView,UpdateCartItemView,RemoveFromCartView,ProductDetailView,LogoutView,CategoryListView,CategoryProductListView
)
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import AdminDashboardView,CategoryListView,CustomLoginView,SearchView,FeaturedProductListView,ProductEditView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyView.as_view(), name='verify'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('verify_login/', VerifyLoginView.as_view(), name='verify_login'),
    path('products/', ProductListView.as_view(), name='products'),
    path('cart/', CartView.as_view(), name='cart'),  # نام مسیر 'cart' برای سبد خرید
    path('add_to_cart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add_product/', AddProductView.as_view(), name='add_product'),
     path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:category_id>/', CategoryProductListView.as_view(), name='category_products'),
    path('featured-products/', FeaturedProductListView.as_view(), name='featured_products'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('order_history/', OrderHistoryView.as_view(), name='order_history'),
    path('cart/update/<int:item_id>/', UpdateCartItemView.as_view(), name='update_cart_item'),
     path('cart/remove/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
     path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
     path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('search/', SearchView.as_view(), name='search'),  # استفاده از ویو کلاس‌محور
    


    #  path('contact/', ContactView.as_view(), name='contact'),

    path('logout/', LogoutView.as_view(), name='logout'),
    # path('automation/', AutomationView.as_view(), name='automation'),
  path('edit-product/<int:product_id>/', ProductEditView.as_view(), name='edit_product'),
     

    # مسیرهای بازیابی کلمه عبور
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
