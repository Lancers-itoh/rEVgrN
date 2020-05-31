from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import AdEmail, CustomUser
from .forms import CustomUserForm
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

def index(request):
    email_list = AdEmail.objects.all()
    count_list = []
    for email in email_list:
    	count = email.customuser_set.all().count()
    	count_list.append(count)

    params = list(zip(email_list, count_list))
    context = {'params': params}
    return render(request, 'smsusers/index.html', context)

def detail(request, email_id):
	email = AdEmail.objects.get(pk=email_id)
	if request.method == "POST":
		form = CustomUserForm(request.POST)
		if form.is_valid():
			username  = request.POST['username']
			password = request.POST['password']
			CustomUser.objects.create_user(username, email=email, password=password, Parent_id=email.id)
			return redirect('/users')
	else:
		form = CustomUserForm()
	return render(request, 'smsusers/detail.html', {'email': email, 'form': form})

@csrf_exempt
def create(request):
	if request.method == "POST":
		print("Got New User")
		print(request.POST['email'])
		email = AdEmail(email = request.POST['email'])
		email.save()
	return redirect('/users')

