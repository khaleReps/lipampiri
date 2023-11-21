from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, CustomLoginForm, UserSettingsForm, UserProfileForm, UserProfileDetails, UserSettingsDetails,  UserMembershipForm, UserMembershipDetails
from .models import UserProfile, UserSettings, CustomUser, UserMembership
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from .models import CustomUser, UserProfile
from datetime import timedelta, datetime

from journal.models import Entry

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('journal:entry_list')

class CustomRegisterView(generic.CreateView):
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        user = form.save()
        print("User created successfully")

        existing_profile = UserProfile.objects.filter(username=user.username).first()
        if existing_profile:
            messages.error(self.request, 'A profile with the same username already exists.')
            return redirect('accounts:register')

        else:
            # Create a UserProfile for the user
            user_profile = UserProfile.objects.create(
                user=user,
                # Set default values for UserProfile fields
                bio="",
                location="",
                date_of_birth=None,
                full_name=user.get_full_name(),
                username=user.username,
                email=user.email,
                phone_number="",
                profile_picture=user.profile_image,
                communication_preference="email",
                notification_frequency="daily",
                visibility_of_profile="public",
                privacy_preferences="",
                theme_selection="light",
                font_size="medium",
                social_media_links="",
                associated_accounts="",
                history_and_activity="",
                preferences=""
            )
            print("UserProfile created successfully")


            # Create default settings for the user
            settings = UserSettings.objects.create(
                user=user,
                language="English",  # Set your default language
                time_zone="UTC",  # Set your default time zone
                date_format="YYYY-MM-DD",  # Set your default date format
                notification_preferences="",
                profile_information="",  
                two_factor_authentication=False,
                privacy_settings="",
                security_preferences="",
                access_control="",
                alerts_and_reminders="",
                theme_selection="light",
                font_size_and_style="",
                api_key_management="",
                third_party_integrations="",
                data_backup_and_restore="",
                data_export_import="",
                audit_logs="",
                error_logging="",
                faqs_and_tutorials="",
                contact_support="",
                feedback_form="",
                surveys_and_user_research="",
                account_deactivation_deletion_options=""
            )
            print("UserSettings created successfully")

            is_trial = form.cleaned_data['membership_type'] == 'Free Trail'
            today = datetime.now().date()
            expiration_date = today + timedelta(days=30)
            renewal_date = today + timedelta(days=30) if not is_trial else None


            # Create a default UserMembership for the user
            membership = UserMembership.objects.create(
                user=user,
                membership_type="Free Trail",
                expiration_date=expiration_date,
                renewal_date=renewal_date,
                is_active=not is_trial,
                is_trial=is_trial,
                payment_status="Pending",
                payment_method="Credit Card"
            )
            print("UserMembership created successfully")

            
            
            # Associate the UserProfile with the CustomUser
            user.userprofile = user_profile
            user.usersettings = settings
            user.usermembership = membership
            user.save()
            
        return redirect(self.success_url)

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'accounts/login.html'



@method_decorator(login_required, name='dispatch')
class ProfileView(generic.UpdateView):
    model = UserProfile
    form_class = UserProfileDetails
    template_name = 'accounts/profile.html'
    context_object_name = 'user_profile'
    success_url = '/accounts/profile/'

    def get_object(self, queryset=None):
        user_profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        if not user_profile:
            UserProfile.objects.create(user=self.request.user)
            user_profile = self.request.user.userprofile
            print("UserProfile created successfully in ProfileView")


        if not user_profile:
            raise Http404("UserProfile does not exist")

        return user_profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.request.user.userprofile)
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProfileEditView(generic.UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'accounts/profile_edit.html'
    context_object_name = 'user_profile'

    def get_success_url(self):
        # return reverse_lazy('profile_detail', kwargs={'pk': self.object.pk})
        return reverse_lazy('accounts:profile')
    

@method_decorator(login_required, name='dispatch')
class DeleteProfileView(generic.DeleteView):
    model = UserProfile
    template_name = 'accounts/delete_profile.html'  
    context_object_name = 'user_profile'
    success_url = reverse_lazy('your_success_url_name')

    def get_object(self, queryset=None):
        return get_object_or_404(UserProfile, user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your profile has been deleted.')
        return super().delete(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class SettingsView(generic.UpdateView):
    model = UserSettings
    form_class = UserSettingsDetails
    template_name = 'accounts/settings.html'
    context_object_name = 'user_settings'
    success_url = '/accounts/settings/'

    def get_object(self, queryset=None):
        user_settings, created = UserSettings.objects.get_or_create(user=self.request.user)

        if not user_settings:
            UserSettings.objects.create(
                user=self.request.user,
                language="English",
                time_zone="UTC",
                # Add default values for other settings fields
            )
            user_settings = self.request.user.usersettings
            print("UserSettings created successfully in SettingsView")

        if not user_settings:
            raise Http404("UserSettings does not exist")

        return user_settings

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


    
@method_decorator(login_required, name='dispatch')
class SettingsEditView(generic.UpdateView):
    model = UserSettings
    form_class = UserSettingsForm
    template_name = 'accounts/settings_edit.html'
    context_object_name = 'user_settings'

    def get_success_url(self):
        return reverse_lazy('settings_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class DeleteSettingsView(generic.DeleteView):
    model = UserSettings
    template_name = 'accounts/delete_settings.html'  
    context_object_name = 'user_settings'
    success_url = reverse_lazy('your_success_url_name')

    def get_object(self, queryset=None):
        return get_object_or_404(UserSettings, user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your settings has been deleted.')
        return super().delete(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class MembershipView(generic.CreateView):
    model = UserMembership
    form_class = UserMembershipDetails
    template_name = 'accounts/membership.html'
    context_object_name = 'user_membership'

    def get_object(self, queryset=None):
        user_membership, created = UserMembership.objects.get_or_create(user=self.request.user)
        if not user_membership:
            UserMembership.objects.create(
                user=self.request.user,
                membership_type="Free",
                expiration_date=None,
                is_active=True,
                is_trial=False,
                payment_status="Pending",
                payment_method="Credit Card"
            )
            user_membership = self.request.user.usermembership
            print("UserMembership created successfully in MembershipView")

        if not user_membership:
            raise Http404("UserMembership does not exist")

        return user_membership
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_membership'] = self.get_object()  # Assuming get_object returns the user's membership
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class MembershipEditView(generic.UpdateView):
    model = UserMembership
    form_class = UserMembershipForm
    template_name = 'accounts/membership_edit.html'
    context_object_name = 'user_membership'

    def get_queryset(self):
        return UserMembership.objects.filter(user=self.request.user)

@method_decorator(login_required, name='dispatch')
class DeleteMembershipView(generic.DeleteView):
    model = UserMembership
    template_name = 'accounts/delete_membership.html'
    context_object_name = 'user_membership'
    success_url = reverse_lazy('your_success_url_name')

    def get_queryset(self):
        return UserMembership.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your membership has been deleted.')
        return super().delete(request, *args, **kwargs)


def SearchView(request):
    query = request.GET.get('q')
    if query:
        results = Entry.objects.filter(title__icontains=query)
    else:
        results = Entry.objects.none()

    return render(request, 'accounts/search.html', {'results': results, 'query': query})


def AccountView(request):
    context = {}
    return render(request, 'accounts/account.html', context)