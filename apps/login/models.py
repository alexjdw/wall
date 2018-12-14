from django.db import models
import re


# Create your models here.
class UserManager(models.Manager):
    def validate_user(self, formdata):
        print(formdata)
        errors = {}
        if 'username' not in formdata:
            errors['username'] = "Username not in form data."
        else:
            un = formdata.get('username')
            if 5 > len(un):
                errors['username'] = "Username is too short."
            if len(un) > 30:
                errors['username'] = "Username is too long."
            if len(self.filter(username=un)) > 0:
                errors['username'] = "Username is already registered."
            if '@' in un:
                errors['username'] = "Please remove the @ from your username"


        if 'email' not in formdata:
            errors['email'] = "Email not in form data."
        else:
            em = formdata.get('email')
            email_re = re.compile(r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}', flags=re.IGNORECASE)
            if not email_re.match(em):
                errors['email'] = "Email isn't a valid email."
            else:
                if len(self.filter(email=em)) > 0:
                    errors['email'] = "Email is already registered."

        if 'password' not in formdata:
            errors['password'] = "Password not in form data."
        else:
            pw = formdata.get('password')
            if len(pw) < 8:
                errors['password'] = "Password must be 8 characters."
            if 'confirm' not in formdata:
                errors['confirm'] = "Please retype your password in the confirm field."
            else:
                if pw != formdata.get('confirm'):
                    errors['password'] = ["Password must match the confirm field."]

        return errors


class User(models.Model):
    username = models.CharField(max_length=30)
    pw_hash = models.CharField(max_length=80)
    email = models.EmailField(max_length=80)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()
