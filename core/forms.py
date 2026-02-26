from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Room 

User = get_user_model()


# -------------------------
# Room Form
# -------------------------
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'


# -------------------------
# Register Form
# -------------------------
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Reject email format
        if "@" in username:
            raise forms.ValidationError("Username should not be an email address.")

        # Allow only letters and spaces
        if not re.match("^[A-Za-z ]+$", username):
            raise forms.ValidationError("Username should contain only letters.")

        return username