from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import AdEmail, CustomUser
from .forms import CustomUserForm, AdEmailForm
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

def index(request):
	if request.user.username != "adminuser":
		return redirect("/")

	form = AdEmailForm(request.POST or None)
	if form.is_valid():
		email = request.POST['email']
		AdEmail.objects.create(email = email)
		return redirect('/adminuser')
	else:
	    email_list = AdEmail.objects.all()
	    count_list = []
	    for email in email_list:
	    	count = email.customuser_set.all().count()
	    	count_list.append(count)

	    params = list(zip(email_list, count_list))
	    context = {'params': params, 'form': form}
	    return render(request, 'smsusers/index.html', context)

def detail(request, email_id):
	if request.user.username != "adminuser":
		return redirect("/")

	def send_mail(user, str_password):
		subject = "競馬タイム予想アプリ本登録完了のお知らせ"
		message = "競馬タイム予想アプリ\n ID:" + user.username + "\n Password:" + str_password
		from_email = 'tomaccessible@gmail.com'  # 送信者
		user.email_user(subject, message, from_email)  # メールの送信

	email = AdEmail.objects.get(pk=email_id)
	user_exist = False
	usernames = ""
	if email.customuser_set.count() >= 1:
		user_exist = True

		usernames = email.customuser_set.all()

	form = CustomUserForm(request.POST or None)
	if 	form.is_valid():
		username  = request.POST['username']
		password = request.POST['password']
		user = CustomUser.objects.create_user(username, email=email.email, password=password, Parent_id=email.id)
		send_mail(user, password)
		return redirect('/adminuser/')
	else:
		return render(request, 'smsusers/detail.html', {'email': email, 'form': form, 'user_exist': user_exist, 'usernames': usernames})

@require_POST
def email_delete(request, email_id):
	if request.user.username != "adminuser":
		return redirect("/")

	ademail = get_object_or_404(AdEmail, id=email_id)
	ademail.delete()
	return redirect('/adminuser/')


def email_edit(request, email_id):
	if request.user.username != "adminuser":
		return redirect("/")
		
	email = get_object_or_404(AdEmail, id=email_id)
	if request.method == "POST":
		form = AdEmailForm(request.POST, instance=email)
		if form.is_valid():
			form.save()
			return redirect('/adminuser/')
	else:
		form = AdEmailForm(instance = email)
	return render(request, 'smsusers/email_edit.html', {'form': form, 'email':email })


#From swift
@csrf_exempt
def create(request):
	if request.method == "POST":
		print("Got New User")
		print(request.POST['email'])
		email = AdEmail(email = request.POST['email'])
		email.save()
	return redirect('/adminuser/')






