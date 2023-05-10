from django.db import models


class CFSDistrict(models.Model):
    name = models.CharField("Name", max_length=30)

    def __str__(self):
        return f"{self.name}"

# Create your models here.
class Incident(models.Model):
    date = models.DateTimeField("Date of incident")
    place = models.TextField("Location", max_length=75)
    description = models.TextField("Description", max_length=300)
    id_cfsdistrict = models.ForeignKey(CFSDistrict, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.place} at {self.date:%d/%m/%Y}"

    def get_absolute_url(self):
        return f"/file/{self.id}"

    class Meta:
        # …
        permissions = (("can_view_analytics", "Allowed to view analytics"),)