from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from .models import Profile, Product

# فرم افزودن محصول
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category', 'discount']  # اضافه کردن discount

# فرم ثبت‌نام
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('ایمیل قبلاً استفاده شده است.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('نام کاربری قبلاً استفاده شده است.')
        return username

# فرم تغییرات اطلاعات کاربری
class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

# فرم تغییرات پروفایل کاربر
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'phone_number', 'email', 'custom_user_id']  # فیلدهایی که می‌خواهید در فرم نمایش داده شوند

# فرم ثبت‌نام کاربر (برای احراز هویت)
class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

# فرم تخفیف محصول (برای اعمال تخفیف بر روی محصولات)
class ProductDiscountForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    discount = forms.IntegerField(min_value=0, max_value=100, label="تخفیف (%)")

# فرم تخفیف انبوه برای همه محصولات
class DiscountForm(forms.Form):
    bulk_discount = forms.IntegerField(
        label="درصد تخفیف برای همه محصولات",
        min_value=0,
        max_value=100,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

# فرم ویرایش محصول
# store/forms.py
from django import forms
from .models import Product, Category

class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category', 'discount']

