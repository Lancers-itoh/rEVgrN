from django.db import models
from django.contrib.auth.models import AbstractUser

class AdEmail(models.Model):
	email = models.EmailField(max_length=254)

class CustomUser(AbstractUser):
	#デフォルトのAbstractUserを継承しフィールドを拡張する
	Parent = models.ForeignKey(AdEmail, on_delete=models.CASCADE)
	#username
	#password

	#12345678