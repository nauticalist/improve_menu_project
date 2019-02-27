from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from . import models
from . import forms


def menu_list(request):
    """
    list all available menus
    """
    menus = models.Menu.objects.filter(
        Q(expiration_date__isnull=True) |
        Q(expiration_date__date__gt=datetime.now())
    ).prefetch_related(
        'items'
    )

    return render(request, 'menu/list_all_current_menus.html',
                  {'menus': menus})


def menu_detail(request, pk):
    menu = get_object_or_404(models.Menu, pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    item = get_object_or_404(models.Item, pk=pk)
    return render(request, 'menu/detail_item.html', {'item': item})


@login_required
def create_new_menu(request):
    if request.method == "POST":
        form = forms.MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.save()
            return redirect('menu_detail', pk=menu.pk)
    else:
        form = forms.MenuForm()
    return render(request, 'menu/menu_edit.html', {'form': form})


@login_required
def edit_menu(request, pk):
    menu = get_object_or_404(models.Menu, pk=pk)
    items = models.Item.objects.all()
    if request.method == "POST":
        menu.season = request.POST.get('season', '')
        menu.expiration_date = datetime.strptime(
            request.POST.get('expiration_date', ''), '%m/%d/%Y')
        menu.items = request.POST.get('items', '')
        menu.save()

    return render(request, 'menu/change_menu.html', {
        'menu': menu,
        'items': items,
        })
