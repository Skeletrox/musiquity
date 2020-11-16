from django.db import models
from django_mysql.models import ListTextField
# Create your models here.


class SeedList(models.Model):
    """
        A seedlist. Has the User and the mode as a composite primary key
        The User is a foreign key
    """
    MODE_CHOICES = [
        ("RUN", "Running Music"),
        ("WEIGHTS", "Weights Music"),
        ("POST_WORKOUT", "Post-workout Music"),
        ("RELAX", "Relaxation Music")
    ]
    user = models.ForeignKey("user_service.User", on_delete=models.CASCADE)
    mode = models.CharField(max_length=12, choices=MODE_CHOICES, default="RELAX")
    seed_list = ListTextField(base_field  = models.CharField(max_length=40), size=20)
