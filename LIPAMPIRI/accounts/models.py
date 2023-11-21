from django.contrib.auth.models import AbstractUser
from django.db import models
from dateutil.relativedelta import relativedelta  
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from dateutil.relativedelta import relativedelta
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from datetime import timedelta


class CustomUser(AbstractUser):
    name = models.CharField(max_length=30, blank=True, null=True)
    surname = models.CharField(max_length=30, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    date_of_birth = models.DateField(default=datetime(1900, 1, 1).date())
    signup_date = models.DateField(default=datetime.now)
    
    email = models.EmailField(unique=True)
    country = CountryField(default='ZA')
    contact_number = PhoneNumberField(blank=True, null=True) 

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='customuser_set',
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set',
        related_query_name='user'
    )

    def save(self, *args, **kwargs):
        if self.name and self.surname:
            self.first_name = self.name
            self.last_name = self.surname
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class UserSettings(models.Model):
    NOTIFICATION_CHOICES = [
        ('Email','Email'),
        ('SMS', 'SMS')
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)

    # General Settings
    language = models.CharField(max_length=50, default='English')
    time_zone = models.CharField(max_length=50, default='UTC')
    date_format = models.CharField(max_length=50, default='MM/DD/YYYY')
    notification_preferences = models.CharField(max_length=10, choices=NOTIFICATION_CHOICES, default='Email' )


    # Account Settings
    profile_information = models.TextField(default='{}', blank=True)
    username_email = models.CharField(max_length=100, default='', blank=True)
    password = models.CharField(max_length=100, default='', blank=True)
    
    two_factor_authentication = models.BooleanField(default=False, blank=True)
   
    # Privacy & Security
    privacy_settings = models.TextField(blank=True, null=True)
    security_preferences = models.TextField(blank=True, null=True)
    access_control = models.TextField(blank=True, null=True)
    alerts_and_reminders = models.TextField(blank=True, null=True)

    # Notification Settings
    theme_selection = models.CharField(max_length=50)
    font_size_and_style = models.TextField(blank=True, null=True)

    # Integration & Connectivity
    api_key_management = models.TextField(blank=True, null=True)
    third_party_integrations = models.TextField(blank=True, null=True)

    # Data Management
    data_backup_and_restore = models.TextField(blank=True, null=True)
    data_export_import = models.TextField(blank=True, null=True)

    # Logging and Activity
    audit_logs = models.TextField(blank=True, null=True)
    error_logging = models.TextField(blank=True, null=True)

    # Help & Support
    faqs_and_tutorials = models.TextField(blank=True, null=True)
    contact_support = models.TextField(blank=True, null=True)

    # Feedback & Surveys
    feedback_form = models.TextField(blank=True, null=True)
    surveys_and_user_research = models.TextField(blank=True, null=True)

    # Account Deactivation/Deletion
    account_deactivation_deletion_options = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Settings for {self.user.username}"


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)

    # Profile info
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    # Notification
    communication_preference = models.CharField(max_length=20, choices=[('email', 'Email'), ('in-app', 'In-App')], default='email')
    notification_frequency = models.CharField(max_length=20, choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], default='daily')
    visibility_of_profile = models.CharField(max_length=20, choices=[('public', 'Public'), ('private', 'Private')], default='public')
    privacy_preferences = models.TextField(blank=True, null=True, default='{}')


    theme_selection = models.CharField(max_length=20, choices=[('light', 'Light'), ('dark', 'Dark')], default='light')
    font_size = models.CharField(max_length=20, choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], default='medium')
    
    social_media_links = models.TextField(blank=True, null=True, default='{}')
    associated_accounts = models.TextField(blank=True, null=True, default='{}')
    history_and_activity = models.TextField(blank=True, null=True, default='{}')
    
    preferences = models.TextField(blank=True, null=True, default='{}')
    
    def __str__(self):
        return f"Profile for {self.user.username}"



class UserMembership(models.Model):
    # Define choices for payment status
    PAYMENT_STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled'),
    ]

    # Define choices for payment method
    PAYMENT_METHOD_CHOICES = [
        ('Credit Card', 'Credit Card'),
        ('PayPal', 'PayPal'),
    ]

    # Subscription
    MEMBERSHIP_CHOICES = [
        ('Free Trail', 'Free Trail'),
        ('Individual', 'Individual'),
        ('SMME', 'Small, Medium and Micro Enterprise'),
        ('Enterpise', 'Enterpise'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    # Membership details
    membership_type = models.CharField(max_length=30, choices=MEMBERSHIP_CHOICES, default='Free Trail')
    expiration_date = models.DateField(null=True, blank=True)
    renewal_date = models.DateField(null=True, blank=True)


    # Membership status
    is_active = models.BooleanField(default=True)  # Indicates if the membership is currently active
    is_trial = models.BooleanField(default=False)  # Indicates if this is a trial membership

    # Additional information
    payment_status = models.CharField(max_length=30, blank=True, null=True, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=30, blank=True, null=True, choices=PAYMENT_METHOD_CHOICES, default='Credit Card')

    @receiver(post_save, sender='accounts.UserMembership')
    def set_membership_dates(sender, instance, created, **kwargs):
        if created:
            # Set the default values on creation
            instance.is_active = True  # Assume the user is active by default
            instance.expiration_date = datetime.now() + timedelta(days=30) if instance.is_trial else datetime.now() + relativedelta(months=1)
            instance.renewal_date = instance.expiration_date if not instance.is_trial else None
            instance.save()

        elif instance.is_active and not instance.is_trial:
            # Update renewal_date for active non-trial users
            if instance.renewal_date is None or instance.renewal_date < datetime.now().date():
                instance.renewal_date = datetime.now() + relativedelta(months=1)
                instance.save()

        elif not instance.is_active and not instance.is_trial:
            # Update expiration_date for inactive non-trial users
            if instance.expiration_date is None or instance.expiration_date < datetime.now().date():
                instance.expiration_date = datetime.now() + relativedelta(months=1)
                instance.save()

    def __str__(self):
        return f"Membership for {self.user.username}"
