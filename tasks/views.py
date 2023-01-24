from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import escape
from django.utils.text import slugify

from tasks.models import Collection, Task


def index(request):
    # Je définis le contexte pour envoyer les informations sur les collections dans ma view
    context = {}

    # Pour récupérer le slug de la requête dans l'url
    collection_slug = request.GET.get("collection")
    # S'il n'y a pas de slug dans l'url, on prend celle par défaut pour l'indiquer dans l'url
    if not collection_slug:
        Collection.get_default_collection()
        return redirect(f"{reverse('home')}?collection=_defaut")

    # Si pas de collection dans l'url on prend celle par défaut
    collection = get_object_or_404(Collection, slug=collection_slug)

    # Je récupère et range toutes les collections par slug
    context["collections"] = Collection.objects.order_by("slug")
    # Je donne au contexte la collection déterminée plus haut
    context["collection"] = collection
    # Je récupère et range les tasks par description
    context["tasks"] = collection.task_set.order_by("description")

    return render(request, 'tasks/index.html', context=context)


def add_collection(request):
    # Je récupère les informations de l'input du formulaire (escape pour protéger les données en 'échappant' les caractères)
    collection_name = escape(request.POST.get("collection-name"))
    # Je crée une Collection (si elle existe) avec les informations récupérées, get_or_create: return a tuple of (object, created), je slugify son nom à ce moment
    collection, created = Collection.objects.get_or_create(name=collection_name, slug=slugify(collection_name))
    # Si elle existe déjà, si elle n'a pas été créée je préviens
    if not created:
        # Cela créera un message d'erreur (voir index.html)
        return HttpResponse("La collection existe déjà.", status=409)

    return render(request, 'tasks/collection.html', context={"collection": collection})


def add_task(request):
    # Je récupère la collection de l'url
    collection = Collection.objects.get(slug=request.POST.get("collection"))

    # Je récupère les informations de l'input du formulaire
    description = escape(request.POST.get("task-description"))
    # Je crée un objet Task avec les informations récupérées et je l'associe à une collection
    task = Task.objects.create(description=description, collection=collection)

    return render(request, 'tasks/task.html', context={"task": task})


def delete_task(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    task.delete()

    return HttpResponse("")


def delete_collection(request, collection_pk):
    collection = get_object_or_404(Collection, pk=collection_pk)
    collection.delete()

    return redirect('home')


def get_tasks(request, collection_pk):
    # Je récupère une collection ou une erreur 404 si elle n'existe pas (pk = primary key
    collection = get_object_or_404(Collection, pk=collection_pk)
    # Je récupère toutes les tâches
    tasks = collection.task_set.order_by("description")

    return render(request, 'tasks/tasks.html', context={"tasks": tasks, "collection": collection})
