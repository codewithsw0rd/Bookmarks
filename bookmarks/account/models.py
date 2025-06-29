from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    date_of_birth = models.DateTimeField(blank=True, null=True)
    photo = models.ImageField(
        upload_to='users/%y/%m/%d/',
        blank=True
    )
    
    def __str__(self):
        return f'Profile for {self.user.username}'
    
class Contact(models.Model):
    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='rel_from_set',
        on_delete=models.CASCADE
    )
    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='rel_to_set',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']
        
    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"
    
user_model = get_user_model()
user_model.add_to_class(
    'following',
    models.ManyToManyField(
        'self',
        through=Contact,
        related_name='followers',
        symmetrical=False
    )
)