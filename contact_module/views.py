from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import FormView

from site_module.models import SiteSetting
from . import forms
# from .forms import ContactUsForm
from .forms import ContactUsModelForm
from .models import Contact


# Create your views here.

class ContactUsView(FormView):
    template_name = 'contact_module/contact_us_page.html'
    form_class = forms.ContactUsModelForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        setting = SiteSetting.objects.filter(is_main_setting=True).first()
        contex = super().get_context_data(**kwargs)
        contex['setting'] = setting
        return contex
# class ContactUsView(View):
#     def get(self, request):
#         contact_form = ContactUsModelForm()
#         return render(request, 'contact_module/contact_us_page.html' , {
#             'contact_form': contact_form,
#         })
#     def post(self, request):
#         contact_form = ContactUsModelForm(request.POST)
#         if contact_form.is_valid():
#             contact_form.save()
#             return redirect('home_page')
#
#         return render(request, 'contact_module/contact_us_page.html' , {
#             'contact_form': contact_form,
#         })

def contact_page(request):
    if request.method == 'POST':
        # contact_form = ContactUsForm(request.POST)
        contact_form = ContactUsModelForm(request.POST)
        if contact_form.is_valid():
            # contact = Contact(
            #     message=contact_form.cleaned_data.get('message'),
            #     name=contact_form.cleaned_data.get('full_name'),
            #     email=contact_form.cleaned_data.get('email'),
            #     title=contact_form.cleaned_data.get('subject'),
            # )
            # contact.save()
            contact_form.save()
            return redirect('home_page')
    else:
        contact_form = ContactUsModelForm()

    return render(request, 'contact_module/contact_us_page.html' , {
        'contact_form': contact_form,
    })
