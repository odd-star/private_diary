import logging
from django.contrib.auth.models import User

from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages

from.forms import InquiryForm
from django.contrib.auth.mixins import LoginRequiredMixin

logger = logging.getLogger(__name__)

from .models import Diary

class IndexView(generic.TemplateView):
    template_name = "index.html"

class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('diary:inquiry')

class DiaryListView(LoginRequiredMixin, generic.ListView):
    model = Diary
    template_name = 'diary_detail.html'
    pk_url_kwatg = 'id'

    def form_valid(self, form): 
        form.send_email()
        messages.success(self.request,'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)
    
    def get_queryset(self):
        diaries = Diary.objects.filter(user=self.request.user).order_by('-created_at')
        return diaries