from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError
#reference https://jumpyoshim.hatenablog.com/entry/how-to-automate-createsuperuser-on-django

class Command(createsuperuser.Command):  # Django標準のcreatesuperuserコマンドを継承
    help = 'Create a superuser'  # helpコマンド実行時のコマンド概要

    def handle(self, *args, **options):  # コマンド実行時のメイン処理
        from smsusers.models import PhoneNumber
        pn = PhoneNumber(phonenumber = '09012345678')
        pn.save()

        options.setdefault('interactive', False)
        username = 'admin'
        email = 'admin@admin.com'
        password = 'adminpass'
        database = options.get('database')

        user_data = {
            'username': username,
            'email': email,
            'password': password,
            'Parent_id': pn.id,
        }

        # 既に同じユーザー名のユーザーが存在するか確認。なければユーザー作成
        exists = self.UserModel._default_manager.db_manager(database).filter(username=username).exists()
        if not exists:
            self.UserModel._default_manager.db_manager(database).create_superuser(**user_data)
