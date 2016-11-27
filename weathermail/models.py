from django.db import models


class City(models.Model):
    display_name = models.CharField(max_length=50)
    api_name = models.CharField(max_length=50)
    population = models.IntegerField(default=0)

    def __str__(self):
        return str(self.display_name)+" pop: "+str(self.population)+" ("+str(self.api_name)+")";

class Recipient( models.Model ):
    email = models.CharField(max_length=160, unique=True, blank=False)
    location = models.ForeignKey( City, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.email)+"     receiving weather for: "+str(self.location);
