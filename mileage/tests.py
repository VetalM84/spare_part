from unittest import skip

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from mileage.forms import ProfileEditForm
from mileage.models import (
    CarBrand,
    CarModel,
    Comment,
    Profile,
    Review,
    SparePart,
    SparePartCategory,
    User,
)


class ViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User.objects.create_user(username="test", password="test")

        CarBrand.objects.create(brand="Audi")
        CarBrand.objects.create(brand="Mercedes")

        CarModel.objects.create(model_name="A6", brand_id=1)
        CarModel.objects.create(model_name="Q5", brand_id=1)
        CarModel.objects.create(model_name="S600", brand_id=2)

        SparePartCategory.objects.create(name="Двигатель")
        SparePartCategory.objects.create(name="Ходовая")

        SparePart.objects.create(
            name="Поршень",
            brand="STR",
            number="4545451",
            category=SparePartCategory.objects.get(name="Двигатель"),
        )
        SparePart.objects.create(
            name="Шаровая опора",
            brand="TRW",
            number="0121 ER",
            category=SparePartCategory.objects.get(name="Ходовая"),
        )
        Review.objects.create(
            spare_part=SparePart.objects.get(name="Поршень"),
            mileage=25,
            car_brand=CarBrand.objects.get(brand="Audi"),
            car_model=CarModel.objects.get(model_name="A6"),
            owner=User.objects.get(username="test"),
            rating=5,
            testimonial="Отличный поршень",
        )
        print("setUpClass")

    @classmethod
    def tearDownClass(cls):
        print("tearDown")

    def setUp(self):
        self.user = User.objects.get(username="test")
        self.client.force_login(user=self.user)
        print("setUp")

    def tearDown(self):
        print("tearDown")

    def test_search(self):
        """Test search with GET query."""
        url = reverse("search_page")
        response = self.client.get(path=url, data={"q": "Поршень"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mileage/search.html")
        self.assertTrue(SparePart.objects.all().count(), 1)

    def test_add_review_success(self):
        """Test add a new review success."""
        response = self.client.post(
            path=reverse("add_review_page"),
            data={
                "spare_part": 1,
                "mileage": 25,
                "car_brand": 1,
                "car_model": 1,
                "rating": 4,
                "testimonial": "Отличный поршень",
            },
            follow=True,
        )
        # print(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mileage/add_review.html")
        self.assertTrue(Review.objects.all().count(), 2)

    def test_add_new_spare_part_fail(self):
        """Test add a new spare part fail."""
        response = self.client.post(
            path=reverse("new_spare_part"),
            data={
                "name": "Поршень",
                "brand": "STR",
                "number": "4545451",
                "category": 1,
            },
            follow=True,
        )
        print(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mileage/add_new_spare_part.html")
        self.assertContains(response, text="uk-alert-danger")

    def test_add_new_spare_part_success(self):
        """Test add a new spare part with success."""
        response = self.client.post(
            path=reverse("new_spare_part"),
            data={
                "name": "test_name",
                "brand": "test_brand",
                "number": "1122 hhy HH",
                "category": 1,
            },
            follow=True,
        )
        print(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text="uk-alert-success")
        self.assertRedirects(response, reverse("add_review_page"))

    def test_get_all_spare_parts_categories(self):
        """Test a list of all spare parts categories."""
        response = self.client.get(path=reverse("get_spare_parts_categories"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mileage/all_spare_parts_categories.html")
        self.assertEqual(len(response.context["categories"]), 2)

    def test_get_spare_parts_category(self):
        """Test a list of spare parts for a given category."""
        url = reverse(
            "spare_parts_category", args=(SparePartCategory.objects.get(name="Двигатель").id,)
        )
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mileage/spare_parts_category.html")
        self.assertEqual(len(response.context["all_spare_parts"]), 1)

    def test_index(self):
        """Test home page with CarBrand list."""
        response = self.client.get(path=reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mileage/index.html")
        self.assertEqual(len(response.context["cars"]), 2)

    def test_get_car_models(self):
        """Test get a list of car models for a given brand."""
        url = reverse("car_models_all", args=(CarBrand.objects.get(brand="Audi").id,))
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mileage/car_models.html")
        self.assertEqual(len(response.context["car_models"]), 2)

    def test_get_model_info(self):
        """Test get a list of spare parts for a given car model."""
        url = reverse("model_info", args=(CarModel.objects.get(model_name="A6").id,))
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mileage/model_info.html")
        self.assertEqual(len(response.context["spare_parts"]), 1)


class UserTest(TestCase):
    """Test user views."""

    def test_user_profile(self):
        """Test user profile page."""
        user = User.objects.create_user(username="test2", password="test")
        profile = Profile(user=user)
        self.assertEqual(profile.user.username, "test2")

    def test_user_login(self):
        """Test user login."""
        url = reverse("login")
        response = self.client.post(
            path=url, data={"username": "test", "password": "test"}, follow=True
        )
        print(response.context)
        self.assertRedirects(response, reverse("home"))

    def test_user_register(self):
        """Test user registration."""
        response = self.client.post(
            path=reverse("register"),
            data={
                "username": "unittest",
                "email": "test123@tt.tt",
                "password1": "Fshfkshfkf.123",
                "password2": "Fshfkshfkf.123",
            },
            follow=True,
        )
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("home"))


class ProfileEditFormTest(TestCase):
    def test_clean_drive2_link_correct(self):
        """Test drive2 link is correct."""
        form_data = {"drive2_link": "https://www.drive2.ru/users/test"}
        form = ProfileEditForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_clean_drive2_link_wrong(self):
        """Test drive2 link if it is wrong."""
        form_data = {"drive2_link": "https://www.drive2.ru/something/"}
        form = ProfileEditForm(data=form_data)
        self.assertFalse(form.is_valid())
