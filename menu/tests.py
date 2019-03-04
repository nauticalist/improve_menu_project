from datetime import timedelta
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.forms import ValidationError

from . import models
from . import forms


class MenuViewsTest(TestCase):
    def setUp(self):
        """Create a test user"""
        self.username = "testuser"
        self.email = "testuser@domain.tld"
        self.password = "testpassword"
        self.chef = get_user_model().objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
        )
        # Create some ingredients
        self.ingredient1 = models.Ingredient.objects.create(
            name='ing1'
        )
        self.ingredient2 = models.Ingredient.objects.create(
            name='ing2'
        )
        self.ingredient3 = models.Ingredient.objects.create(
            name='ing3'
        )
        # Create some menu items
        self.item1 = models.Item.objects.create(
            name='item1',
            description='menu item 1',
            chef=self.chef
        )
        self.item1.ingredients.add(self.ingredient1, self.ingredient2)
        self.item2 = models.Item.objects.create(
            name='item2',
            description='menu item 2',
            chef=self.chef
        )
        self.item2.ingredients.add(self.ingredient1, self.ingredient3)
        # Create expired menu for test
        self.expired_menu = models.Menu.objects.create(
            season='MenuExpired',
            expiration_date=timezone.now() - timedelta(days=90)
        )
        self.expired_menu.items.add(self.item1)
        # create a non-expired menu
        self.menu = models.Menu.objects.create(
            season='Season1',
            expiration_date=timezone.now() + timedelta(days=90)
        )
        self.menu.items.add(self.item1, self.item2)

    def test_menu_list_view(self):
        """
        Test menu list views
        """
        resp = self.client.get(reverse('menu_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.menu, resp.context['menus'])
        self.assertNotIn(self.expired_menu, resp.context['menus'])
        self.assertTemplateUsed(resp, 'menu/menu_list.html')

    def test_menu_detail_view(self):
        """
        Test menu details view
        """
        resp = self.client.get(reverse(
            'menu_detail', kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.menu, resp.context['menu'])
        self.assertNotEqual(self.expired_menu, resp.context['menu'])

    def test_menu_detail_view_for_404(self):
        """
        Test 404 error for not existing menus
        """
        resp = self.client.get(reverse('menu_detail', kwargs={'pk': 999}))
        self.assertEqual(resp.status_code, 404)

    def test_item_detail_view(self):
        """
        Test for item details views
        """
        resp = self.client.get(reverse(
            'item_detail', kwargs={'pk': self.item1.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.item1, resp.context['item'])
        self.assertTemplateUsed('menu/item_detail.html')

    def test_item_detail_view_for_404(self):
        """
        Test 404 errır fır not existing items
        """
        resp = self.client.get(reverse('item_detail', kwargs={'pk': 999}))
        self.assertEqual(resp.status_code, 404)

    def test_create_new_menu_view(self):
        """
        Test view for menu creation page
        """
        self.client.login(username=self.username, password=self.password)
        get_resp = self.client.get(reverse(
            'menu_new'))
        post_resp = self.client.post(reverse(
            'menu_new'))
        self.assertEqual(get_resp.status_code, 200)
        self.assertEqual(post_resp.status_code, 200)
        self.assertTemplateUsed('menu/menu_form.html')

    def test_edit_menu_view(self):
        """
        Test edit menu view
        """
        self.client.login(username=self.username, password=self.password)
        get_resp = self.client.get(reverse(
            'menu_edit', kwargs={'pk': self.menu.pk}))
        post_resp = self.client.post(reverse(
            'menu_edit', kwargs={'pk': self.menu.pk}))
        self.assertEqual(get_resp.status_code, 200)
        self.assertEqual(post_resp.status_code, 200)
        self.assertTemplateUsed('menu/menu_form.html')

    def test_create_menu_form_with_valid_data(self):
        """
        Check menu form with valid form data
        """
        expire_date = timezone.now() + timedelta(days=100)
        data = {'season': 'seasonx',
                'items': [self.item1.pk],
                'expiration_date': expire_date
                }
        form = forms.MenuForm(data=data)
        self.assertTrue(form.is_valid())
        menu = form.save()
        self.assertEqual(menu.season, 'seasonx')
        self.assertEqual(menu.expiration_date, expire_date)

    def test_create_menu_form_with_blank_data(self):
        """
        Test create menu form with blank data. Should return false
        """
        form = forms.MenuForm(data={})
        self.assertFalse(form.is_valid())

    def test_create_menu_form_with_invalid_data(self):
        """
        Test create menu form with invalid date
        """
        expire_date = timezone.now() - timedelta(days=100)
        data = {'season': 'seasony',
                'items': [self.item2.pk],
                'expiration_date': expire_date}
        form = forms.MenuForm(data=data)
        self.assertRaises(ValidationError, form.full_clean())


class MenuModelsTest(TestCase):
    def test_menu_repr(self):
        """
        Check menu object representation
        """
        menu = models.Menu(
            season='Winter 2017')
        self.assertEqual(str(menu), 'Winter 2017')
