from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from noxcrux_api.views.OTP import get_user_totp_device


class RegisterForm(UserCreationForm):

    def clean(self):
        if settings.REGISTRATION_OPEN is False:
            raise forms.ValidationError('Registrations are closed.')
        return super(RegisterForm, self).clean()


class UsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

    username = forms.CharField(max_length=255, required=True, label="New username",
                               help_text="Enter your new desired username.",
                               widget=forms.TextInput(attrs={'autofocus': True}))


class DeleteUserForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    password = forms.CharField(max_length=128, required=True, label="Confirm your password",
                               help_text="To confirm your action, please enter your current password",
                               widget=forms.PasswordInput(attrs={'autofocus': True}))

    def clean_password(self):
        password = self.cleaned_data["password"]
        if not self.user.check_password(password):
            raise forms.ValidationError("Your password was entered incorrectly. Please enter it again.",
                                        code='password_incorrect')
        return password


class OTPForm(forms.Form):

    def __init__(self, user, verify=True, *args, **kwargs):
        self.user = user
        self.verify = verify
        super().__init__(*args, **kwargs)

    totp_code = forms.CharField(max_length=6, required=True, label="Code",
                                help_text="Enter the code from your TOTP application.",
                                widget=forms.TextInput(attrs={'autofocus': True}))

    def clean_totp_code(self):
        totp_code = self.cleaned_data["totp_code"]
        if self.verify is False:
            return totp_code
        device = get_user_totp_device(self.user, confirmed=True)
        if device.verify_token(totp_code):
            return totp_code
        else:
            raise forms.ValidationError('The TOTP code you entered is incorrect.')


class FriendForm(forms.Form):

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    friend = forms.CharField(max_length=255, required=True, label="Friend username",
                               help_text="Enter your friend's username",
                               widget=forms.TextInput(attrs={'autofocus': True}))

    def clean_friend(self):
        try:
            friend = User.objects.get(username=self.cleaned_data['friend'])
        except User.DoesNotExist:
            raise forms.ValidationError("User with that username does not exists")
        if self.request.user == friend:
            raise forms.ValidationError("Users cannot be friend with themselves.")
        if self.request.user.friends.filter(friend=friend, validated=False).exists():
            raise forms.ValidationError(f"A friend request was already sent to {friend}")
        if self.request.user.friends.filter(friend=friend, validated=True).exists():
            raise forms.ValidationError(f"You already are friend with {friend}")
        return self.cleaned_data['friend']
