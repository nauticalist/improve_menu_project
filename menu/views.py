from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from . import models
from . import forms


def menu_list(request):
    """
    list all available menus
    """
    today = datetime.now()
    menus = models.Menu.objects.filter(
        Q(expiration_date=None) |
        Q(expiration_date__date__gt=today)
    ).prefetch_related(
        'items'
    )

    return render(request, 'menu/menu_list.html',
                  {'menus': menus})


def menu_detail(request, pk):
    menu = get_object_or_404(models.Menu, pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    item = get_object_or_404(models.Item, pk=pk)
    return render(request, 'menu/item_detail.html', {'item': item})


@login_required
def create_new_menu(request):
    """
    Create new menu
    """
    if request.method == "POST":
        form = forms.MenuForm(request.POST)
        if form.is_valid():
            menu = form.save()
            return redirect(reverse('menu_detail', kwargs={'pk': menu.pk}))
    else:
        form = forms.MenuForm()
    return render(request, 'menu/menu_form.html', {'form': form})


@login_required
def edit_menu(request, pk):
    """
    Edit an existing menu
    """
    menu = get_object_or_404(models.Menu, pk=pk)
    form = forms.MenuForm(instance=menu)
    if request.method == "POST":
        form = forms.MenuForm(instance=menu, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu_detail', pk=form.instance.pk)
    return render(request, 'menu/menu_form.html', {'form': form})
