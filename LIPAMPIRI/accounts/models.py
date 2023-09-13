from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    name = models.CharField(max_length=30, blank=True, null=True)
    surname = models.CharField(max_length=30, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
  
    email = models.EmailField(unique=True)

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
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)


    # General Settings
    language = models.CharField(max_length=50, default='English')
    time_zone = models.CharField(max_length=50, default='UTC')
    date_format = models.CharField(max_length=50, default='MM/DD/YYYY')
    notification_preferences = models.TextField(default='{"email": true, "sms": false}')


    # Account Settings
    profile_information = models.TextField(default='{}')
    username_email = models.CharField(max_length=100, default='')
    password = models.CharField(max_length=100, default='')
    two_factor_authentication = models.BooleanField(default=False)
   
    # Privacy & Security
    privacy_settings = models.TextField()
    security_preferences = models.TextField()
    access_control = models.TextField()
    alerts_and_reminders = models.TextField()

    # Notification Settings
    theme_selection = models.CharField(max_length=50)
    font_size_and_style = models.TextField()

    # Integration & Connectivity
    api_key_management = models.TextField()
    third_party_integrations = models.TextField()

    # Data Management
    data_backup_and_restore = models.TextField()
    data_export_import = models.TextField()

    # Logging and Activity
    audit_logs = models.TextField()
    error_logging = models.TextField()

    # Help & Support
    faqs_and_tutorials = models.TextField()
    contact_support = models.TextField()

    # Feedback & Surveys
    feedback_form = models.TextField()
    surveys_and_user_research = models.TextField()

    # Account Deactivation/Deletion
    account_deactivation_deletion_options = models.TextField()

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

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    # Membership details
    membership_type = models.CharField(max_length=30, blank=True, null=True)
    expiration_date = models.DateField(null=True, blank=True)

    # Membership status
    is_active = models.BooleanField(default=True)  # Indicates if the membership is currently active
    is_trial = models.BooleanField(default=False)  # Indicates if this is a trial membership

    # Additional information
    payment_status = models.CharField(max_length=30, blank=True, null=True, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=30, blank=True, null=True, choices=PAYMENT_METHOD_CHOICES, default='Credit Card')

    def __str__(self):
        return f"Membership for {self.user.username}"
