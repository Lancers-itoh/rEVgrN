from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.views import generic
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Racelist, Post, Racedata
from django.templatetags.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from .Xscraping import Parse_from, Predict_from_these, normalization
import numpy as np

"""
Django Auth

The LoginRequired mixin
https://docs.djangoproject.com/en/2.0/topics/auth/default/#the-loginrequired-mixin

The login_required decorator
https://docs.djangoproject.com/en/2.0/topics/auth/default/#the-login-required-decorator
@login_required
"""



class IndexView(LoginRequiredMixin, generic.ListView):
    model = Racelist
    paginate_by = 5
    ordering = ['date']


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Racelist

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        race =  Racelist.objects.get(pk=self.kwargs['pk'])
        horse_names = race.racedata_set.values_list('horse_name', flat=True).all()
        horse_values = race.racedata_set.values_list('horse_data', flat=True).all()

        predict_times = list(range(len(horse_names)))
        for i in range(len(horse_names)):
            str_value = horse_values[i].rstrip("/")
    
            try:
                value = [float(s) for s in str_value.split('/')]
                data = np.array(value)
            except:
                context['message'] = "データの欠損により予測ができません"
                return context

            normalized_data = normalization(data, 'static/data/Xmean.csv', 'static/data/Xstd.csv')
            Ymean = 92.68061322261258
            Ystd = 19.06101964452713
            predict_times[i] = Predict_from_these(normalized_data, "static/data/mlp_model.sav", Ymean, Ystd)[0]/60
        
        racedata = np.array([horse_names, predict_times])
        racedata = racedata.T
        racedata_sorted = racedata[np.argsort(racedata[:, 1])]
        context['predict_data'] = racedata_sorted

        return context
   


class CreateView(LoginRequiredMixin, generic.edit.CreateView):  # The LoginRequired mixin
    model = Post
    fields = ['title', 'text']  # '__all__'

    # template_name = 'blogs/post_form.html'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # https://docs.djangoproject.com/en/2.0/topics/class-based-views/generic-editing/#models-and-request-user
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)


class UpdateView(LoginRequiredMixin, generic.edit.UpdateView):  # The LoginRequired mixin
    model = Post
    fields = ['title', 'text']  # '__all__'

    # template_name = 'blogs/post_form.html'

    def dispatch(self, request, *args, **kwargs):
        # ownership validation
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to edit.')

        return super(UpdateView, self).dispatch(request, *args, **kwargs)


class DeleteView(LoginRequiredMixin, generic.edit.DeleteView):  # The LoginRequired mixin
    model = Post
    success_url = reverse_lazy('blogs:index')

    # blogs/post_confirm_delete.html

    def dispatch(self, request, *args, **kwargs):
        # ownership validation
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to delete.')

        return super(DeleteView, self).dispatch(request, *args, **kwargs)


@login_required
def help(request):
    return HttpResponse("Member Only Help Page")
