# mixins.py
from django.contrib import messages
from django.shortcuts import render

class SweetAlert2Mixin:
    def add_sweetalert_message(self, request, message, message_type='success'):
        """
        این متد پیام را به صفحه ارسال می‌کند تا در قالب SweetAlert2 نشان داده شود.
        """
        messages.add_message(request, getattr(messages, message_type.upper()), message)
        
    def render_with_sweetalert(self, request, template_name, context=None):
        """
        این متد قالب را با پیام‌های SweetAlert2 نمایش می‌دهد.
        """
        if context is None:
            context = {}
        
        # پیام‌ها را به اسکریپت SweetAlert2 تبدیل می‌کنیم.
        if messages.get_messages(request):
            context['sweetalert_messages'] = [msg.message for msg in messages.get_messages(request)]
        
        return render(request, template_name, context)
