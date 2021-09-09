import logging
from django.views import generic

from .forms import InquiryForm

def index(request):
    return render(request, 'index.html')

class IndexView(generic.TemplateView):
    template_name = "index.html"

class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
------------------------------------------------------------------------------

    self.fields['name'].widget.attrs['class'] = 'form-control col-9'
    self.fields['name'].widget.attrs['placeholder'] ='お名前をここに入力してください。'
    self.fields['email'].widget.attrs['class'] ='form-control col-11'
    self.fields['email'].widget.attrs['placeholder'] ='メールアドレスをここに入力してください。'
    self.fields['title'].widget.attrs['class'] ='form-control col-11'
    self.fields['title'].widget.attrs['placeholder'] ='タイトルをここに入力してください。'
    self.fields['message'].widget.attrs['class'] ='form-control col-12'
    self.fields['message'].widget.attrs['placeholder'] ='メッセージをここに入力してください。'
-----------------------------------------------------
import logging

from django.urls import reverse_lazy
from django.views import generic

from.forms import InquiryForm

logger = logging.getLogger(__name__)

class IndexView(generic.TemplateView):
    template_name = "index.html"

class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('diary:inquiry')

    def form_valid(self, form): 
        form.send_email()
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)
----------------------------------------------------

def send_email(self):
    name = self.cleaned_data['name']
    email = self.cleaned_data['email']
    title = self.cleaned_data['title']
    message = self.cleaned_data['message']

    subject = 'お問合せ{}'.format(title)
    message = '送信者名: {0}\nメールアドレス: {1}\nメッセージ:\n{2}'.format(name, email, message)
    form_email = 'admin@example.com'
    to_list = [
        'test@example.com'
    ]
    cc_list = [
        email
    ]

    message = EmailMessage(subject=subject, body=message, form_email=form_email, to=to_list, cc=cc_list)
    message.send()
---------------------------------------------------------------------------------------------------
{% extends 'base.html' %}
{% load static %}

{% block title %}お問合せ | Private Diary{% endblock %}

{% block contents %}
<!-- Content section 1-->
<section id="scroll">
    <div class="container px-5">
        <div class="row gx-5 align-items-center">
            <form method="POST">
                {% csrf_token %}
                {{ form.non_field_errors }}

                {% for field in from %}
                <div class="form-group row">
                    <label for="{{ field.id_for_label }}" class="col-sm-4 col-form-label">
                        <strong>{{ field.label_tag }}</strong>
                    </label>
                    <div class="col-sm-8">
                        {{ field }}
                        {{ field.errors }}
                    </div>
                </div>
                {% endfor %}
                <div class="offset-sm-4 col-sm-8">
                    <button class="btn btn-primary" type="submit"></button>
                </div>
            </form>
        </div>
    </div>
</section>
{% endblock %}