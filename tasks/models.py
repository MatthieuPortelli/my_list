from django.db import models
from django.utils.text import slugify


class Collection(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField()

    # Pour afficher le nom de la collection dans la section admin
    def __str__(self):
        return self.name

    # Si à la création de la collection je ne spécifie pas le slug je le génère (override)
    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.name)
        super().save(*args, **kwargs)

    @classmethod
    # Création d'une collection par défaut, de type Collection, pour récupérer une instance de Collection
    def get_default_collection(cls) -> "Collection":
        collection, _ = cls.objects.get_or_create(name="Liste par défaut", slug="_defaut")
        return collection


class Task(models.Model):
    description = models.CharField(max_length=300)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    # Pour afficher la description de la tâche dans la section admin
    def __str__(self):
        return self.description
