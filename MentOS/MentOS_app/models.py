from django.db import models
from django.contrib.auth.models import User
from PIL import Image

USER_PROFILE_INTEREST_CHOICES = [
    ('Career Advising', 'Career Advising'),
    ('Cybersecurity', 'Cybersecurity'),
    ('Software Development', 'Software Development'),
    ('Databases', 'Databases'),
    ('Computer Networking', 'Computer Networking'),
    ('Information Technology', 'Information Technology'),
    ('Health & Wellness', 'Health & Wellness'),
    ('Nutrition', 'Nutrition'),
    ('Exercise', 'Exercise'),
    ('Yoga', 'Yoga'),
    ('Weightlifting', 'Weightlifting'),
    ('Relationship Advice', 'Relationship Advice'),
    ('Love & Dating', 'Love & Dating'),
    ('Cars & Other Motorvechiles', 'Cars & Other Motorvechiles'),
    ('Homeownership', 'Homeownership'),
    ('Culinary', 'Culinary'),
    ('Business', 'Business'),
    ('Spiritual', 'Spiritual'),
    ('Mindfulness', 'Mindfulness'),
    ('Competitive Gaming', 'Competitive Gaming'),
    ('Accounting', 'Accounting'), 
    ('Financial Planning', 'Financial Planning'),
    ('Engineering', 'Engineering'),
    ('Marketing', 'Marketing'),
    ('Agriculture', 'Argiculture'),
    ('Other', 'Other')
]

USER_PROFILE_INTEREST_CHOICES.sort(key = lambda x: x[0])

USER_PROFILE_BIO_DEFAULT = "Hello World! This is my biography. I will tell other users about myself here."

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(default=USER_PROFILE_BIO_DEFAULT)
    interest = models.CharField(max_length=100, choices=USER_PROFILE_INTEREST_CHOICES, default='Other')
    total_rating = models.IntegerField(default=0)
    number_of_raters = models.IntegerField(default=0)
    list_of_raters = models.TextField(default="$")
    status = models.BooleanField(default=True)
    # blocked_users will be other users who have blocked this user
    blocked_users = models.TextField(default="$")
    current_connections = models.TextField(default="$")
    pending_connections = models.TextField(default="$")

    
    def __str__(self):
        return f'{self.user.username} User Profile'

    def save(self, **kwargs):
        """Resize user profile images if they are too big"""
        super().save()
        img = Image.open(self.profile_img.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_img.path)

