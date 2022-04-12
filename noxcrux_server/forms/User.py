from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.conf import settings
from noxcrux_api.views.OTP import get_user_totp_device
from noxcrux_api.models.UserKeysContainer import UserKeysContainer


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, help_text="Check to stay logged in")

    def clean_remember_me(self):
        remember_me = self.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
        return remember_me


class RegisterForm(forms.ModelForm):
    """
    UserCreationForm copy to bind API and server fields
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

    class Meta:
        model = User
        fields = ["username"]
        field_classes = {'username': UsernameField}

    error_messages = {
        'password_mismatch': 'The two password fields didn’t match.'
    }

    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    def clean(self):
        if settings.REGISTRATION_OPEN is False:
            raise forms.ValidationError('Registrations are closed.')
        return super(RegisterForm, self).clean()

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class KeysContainerForm(forms.ModelForm):
    class Meta:
        model = UserKeysContainer
        fields = ['public_key', 'private_key', 'iv']

    public_key = forms.CharField(widget=forms.HiddenInput())
    private_key = forms.CharField(widget=forms.HiddenInput())
    iv = forms.CharField(widget=forms.HiddenInput())


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


class ShareForm(FriendForm):

    def clean_friend(self):
        try:
            friend = User.objects.get(username=self.cleaned_data['friend'])
        except User.DoesNotExist:
            raise forms.ValidationError("User with that username does not exists")
        if self.request.user == friend:
            raise forms.ValidationError("Users cannot grant themselves horcruxes.")
        if not self.request.user.friends.filter(friend=friend, validated=True).exists():
            raise forms.ValidationError(f"You are not friend with {friend}")
        return self.cleaned_data['friend']
