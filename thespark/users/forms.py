from django import forms

from .models import SparkUser

class SparkUserSignUpForm(forms.Form):
    first_name = forms.CharField(max_length=50, label="First Name")
    last_name = forms.CharField(max_length=50, label="Last Name")
    occupation = forms.CharField(max_length=50, label="Occupation e.g student")

    def signup(self,request,user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.occupation = self.cleaned_data['occupation']
        user.save()
        new_spark_user = SparkUser.objects.create(relation=user)
        new_spark_user.save()
