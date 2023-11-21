from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from .models import CustomUser, UserSettings, UserProfile, UserMembership
from django.forms import DateInput, TextInput, Textarea, Select


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    membership_type = forms.CharField(
        label='Membership Type',
        widget=forms.Select(choices=UserMembership.MEMBERSHIP_CHOICES, attrs={'class': 'form-control'}),
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'name', 'surname', 'country', 'date_of_birth', 'contact_number', 'membership_type']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+12125552368'}),
        }


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

            # Try to get existing user profile or create a new one
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.first_name = user.name
            user_profile.last_name = user.surname
            user_profile.location = user.country
            user_profile.date_of_birth = user.date_of_birth
            user_profile.phone_number = user.contact_number

            user_profile.full_name = f"{user.name} {user.surname}"
            user_profile.username = user.username
            user_profile.email = user.email

            user_profile.save()

            # Try to get existing user settings or create a new one
            user_settings, created = UserSettings.objects.get_or_create(user=user)
            user_settings.first_name = user.name
            user_settings.last_name = user.surname
            user_settings.username_email = user.email
            user_settings.password = user.password
            user_settings.save()

        return user



class CustomLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("New passwords do not match")
        return new_password2



    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Invalid username or password. Please try again.")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("This account is inactive.")
        return self.cleaned_data


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = '__all__'
        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'language': forms.TextInput(attrs={'class': 'form-control'}),
            'time_zone': forms.TextInput(attrs={'class': 'form-control'}),
            'date_format': forms.TextInput(attrs={'class': 'form-control'}),
            'notification_preferences': forms.Select(attrs={'class': 'form-control', 'readonly': True, }),
            'profile_information': forms.Textarea(attrs={'class': 'form-control'}),
            'username_email': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'render_value': True}),
            'privacy_settings': forms.Textarea(attrs={'class': 'form-control'}),
            'security_preferences': forms.Textarea(attrs={'class': 'form-control'}),
            'access_control': forms.Textarea(attrs={'class': 'form-control'}),
            'alerts_and_reminders': forms.Textarea(attrs={'class': 'form-control'}),
            'theme_selection': forms.TextInput(attrs={'class': 'form-control'}),
            'font_size_and_style': forms.Textarea(attrs={'class': 'form-control'}),
            'api_key_management': forms.Textarea(attrs={'class': 'form-control'}),
            'third_party_integrations': forms.Textarea(attrs={'class': 'form-control'}),
            'data_backup_and_restore': forms.Textarea(attrs={'class': 'form-control'}),
            'data_export_import': forms.Textarea(attrs={'class': 'form-control'}),
            'audit_logs': forms.Textarea(attrs={'class': 'form-control'}),
            'error_logging': forms.Textarea(attrs={'class': 'form-control'}),
            'faqs_and_tutorials': forms.Textarea(attrs={'class': 'form-control'}),
            'contact_support': forms.Textarea(attrs={'class': 'form-control'}),
            'feedback_form': forms.Textarea(attrs={'class': 'form-control'}),
            'surveys_and_user_research': forms.Textarea(attrs={'class': 'form-control'}),
            'account_deactivation_deletion_options': forms.Textarea(attrs={'class': 'form-control'}),
        }


class UserSettingsDetails(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = '__all__'
        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'first_name': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'language': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'time_zone': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'date_format': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            # 'notification_preferences': forms.Select(attrs={'class': 'form-control', 'readonly': True}),
            
            'notification_preferences': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            
            'profile_information': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'username_email': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'password': forms.TextInput(attrs={'class': 'form-control-plaintext', 'type': 'password','readonly': True}),
            'privacy_settings': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'security_preferences': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'access_control': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'alerts_and_reminders': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'theme_selection': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'font_size_and_style': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'api_key_management': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'third_party_integrations': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'data_backup_and_restore': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'data_export_import': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'audit_logs': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'error_logging': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'faqs_and_tutorials': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'contact_support': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'feedback_form': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'surveys_and_user_research': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'account_deactivation_deletion_options': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
        }





class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'communication_preference': forms.Select(attrs={'class': 'form-control'}),
            'notification_frequency': forms.Select(attrs={'class': 'form-control'}),
            'visibility_of_profile': forms.Select(attrs={'class': 'form-control'}),
            'privacy_preferences': forms.Textarea(attrs={'class': 'form-control'}),
            'theme_selection': forms.Select(attrs={'class': 'form-control'}),
            'font_size': forms.Select(attrs={'class': 'form-control'}),
            'social_media_links': forms.Textarea(attrs={'class': 'form-control'}),
            'associated_accounts': forms.Textarea(attrs={'class': 'form-control'}),
            'history_and_activity': forms.Textarea(attrs={'class': 'form-control'}),
            'preferences': forms.Textarea(attrs={'class': 'form-control'}),
        }


class UserProfileDetails(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'first_name': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'bio': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'location': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control-plaintext', 'type': 'date', 'readonly': True}),
            'full_name': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'username': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control-plaintext form-control-plaintext-plaintext', 'readonly': True}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'profile_picture': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'communication_preference': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'notification_frequency': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'visibility_of_profile': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'privacy_preferences': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'theme_selection': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'font_size': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'social_media_links': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'associated_accounts': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'history_and_activity': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'preferences': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
        }




class UserMembershipForm(forms.ModelForm):
    class Meta:
        model = UserMembership
        fields = '__all__'
        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control'}),
            'membership_type': forms.Select(attrs={'class': 'form-control'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'renewal_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_trial': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'payment_status': forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }

class UserMembershipDetails(UserMembershipForm):
    class Meta(UserMembershipForm.Meta):
        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'membership_type': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'expiration_date': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'renewal_date': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'disabled': True}),
            'is_trial': forms.CheckboxInput(attrs={'class': 'form-check-input', 'disabled': True}),
            'payment_status': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
            'payment_method': forms.TextInput(attrs={'class': 'form-control-plaintext', 'readonly': True}),
        }
