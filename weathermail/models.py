from django.db import models

# Create your models here.



class City(models.Model):
    display_name = models.CharField(max_length=50)
    api_name = models.CharField(max_length=50)
    population = models.IntegerField(default=0);

    def __str__(self):
        return str(self.display_name)+" pop: "+str(self.population)+" ("+str(self.api_name)+")";
