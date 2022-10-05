from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    city = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwarks):
        super().save(*args, **kwarks)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            ratio = max(img.height, img.width) / min(img.height, img.width)
            maxsize = round(300 * ratio)
            if img.height > img.width:
                img = img.resize((300, maxsize))
            else:
                img = img.resize((maxsize, 300))
        
            left = (img.width - 300)/2
            top = (img.height - 300)/2
            right = (img.width + 300)/2
            bottom = (img.height + 300)/2

            try:
                img = img.crop((left, top, right, bottom))
            except:
                output_size = (300, 300)
                img.thumbnail(output_size)

            img.save(self.image.path)
