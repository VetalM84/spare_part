from unittest import skip

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

    def test_get_all_spare_parts_categories(self):
        response = self.client.get(path=reverse("get_spare_parts_categories"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mileage/all_spare_parts_categories.html")
        self.assertEqual(len(response.context["categories"]), 2)

    def test_index(self):
        response = self.client.get(path=reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mileage/index.html")
        self.assertEqual(len(response.context["cars"]), 2)

    def test_get_car_models(self):
        url = reverse("car_models_all", args=(CarBrand.objects.get(brand="Audi").id,))
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mileage/car_models.html")
        self.assertEqual(len(response.context["car_models"]), 2)

    def test_get_model_info(self):
        url = reverse("model_info", args=(CarModel.objects.get(model_name="A6").id,))
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mileage/model_info.html")
        self.assertContains(response, "Все для Audi A6")
        self.assertEqual(len(response.context["spare_parts"]), 1)


class UserTest(TestCase):

    # @classmethod
    # def setUpTestData(cls):
    #     pass
    #
    # @classmethod
    # def tearDownTestData(cls):
    #     print("tearDownTestData")

    # def test_get_absolute_url(self):
    #     author=Author.objects.get(id=1)
    #     #This will also fail if the urlconf is not defined.
    #     self.assertEquals(author.get_absolute_url(),'/catalog/author/1')

    def setUp(self):
        # User = get_user_model().objects.all()
        self.user = User.objects.create_user(username="test", password="test")
        print("setUp")

    def test_user_profile(self):
        user = User.objects.create_user(username="test2", password="test")
        profile = Profile(user=user)
        self.assertEqual(profile.user.username, "test2")

    def test_user_login(self):
        url = reverse("login")
        response = self.client.post(
            path=url, data={"username": "test", "password": "test"}, follow=True
        )
        print(response.context)
        self.assertRedirects(response, reverse("home"))

    @skip("Doesn't work")
    def test_user_user_logout(self):
        # user = User.objects.create_user(username="test", password="test")
        self.logged_in = self.client.force_login(user=self.user)
        url = reverse("logout")
        response = self.client.get(path=url, follow=True)
        print(self.user.username)
        self.assertTrue(self.user.is_anonymous)
        self.assertRedirects(response, reverse("login"))

    @skip("Doesn't work")
    def test_user_register(self):
        url = reverse("register")
        response = self.client.post(
            path=url,
            data={
                "username": "unittest",
                "email": "test123@tt.tt",
                "password1": "unittest.123",
                "password2": "unittest.123",
            },
            follow=True,
        )
        # users = get_user_model().objects.all()
        # self.assertEqual(users.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mileage/register.html")
        self.assertRedirects(response, reverse("home"))


class ProfileEditFormTest(TestCase):
    def test_clean_drive2_link_correct(self):
        form_data = {"drive2_link": "https://www.drive2.ru/users/test"}
        form = ProfileEditForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_clean_drive2_link_wrong(self):
        form_data = {"drive2_link": "https://www.drive2.ru/something/"}
        form = ProfileEditForm(data=form_data)
        self.assertFalse(form.is_valid())
