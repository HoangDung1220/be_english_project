from django.db import models

class Roles(models.Model):

    name = models.CharField(max_length=20, null=False)

    def __str__(self) :
        return self.name

    class Meta:
        db_table = "roles"
