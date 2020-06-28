from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.views import generic
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Racelist, Racedata
from django.templatetags.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from .Xscraping import Predict_from_these, normalization
import numpy as np
from django.db.models import Q

"""
Django Auth

The LoginRequired mixin
https://docs.djangoproject.com/en/2.0/topics/auth/default/#the-loginrequired-mixin

The login_required decorator
https://docs.djangoproject.com/en/2.0/topics/auth/default/#the-login-required-decorator
@login_required
"""



class IndexView(LoginRequiredMixin, generic.ListView):
    def get_queryset(self):
        q_word = self.request.GET.get('query')
 
        if q_word:
            object_list = Racelist.objects.filter(
                Q(title__icontains=q_word) | Q(place__icontains=q_word) | Q(date__icontains=q_word)).order_by('date')
        else:
            object_list = Racelist.objects.all().order_by('date').reverse()
        return object_list


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Racelist

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        race =  Racelist.objects.get(pk=self.kwargs['pk'])

        horse_names = race.racedata_set.values_list('horse_name', flat=True).all()
        horse_values = race.racedata_set.values_list('horse_data', flat=True).all()
        lackparams = race.racedata_set.values_list('lackparams', flat=True).all()

        predict_times = list(range(len(horse_names)))
        for i in range(len(horse_names)):
            str_value = horse_values[i].rstrip("/")
            try:
                value = [float(s) for s in str_value.split('/')]
                data = np.array(value)
            except:
                context['message'] = "データの欠損により予測ができません"
                return context

            normalized_data = normalization(data)
            predict_times[i] = round(Predict_from_these(normalized_data, "static/data/mlp_model.sav")[0]/60,3)
        
        racedata = np.array([horse_names, predict_times, lackparams])
        racedata = racedata.T
        racedata_sorted = racedata[np.argsort(racedata[:, 1])]
        context['predict_data'] = racedata_sorted

        return context

@login_required
def help(request):
    return HttpResponse("Member Only Help Page")
