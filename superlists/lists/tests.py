from django.test import TestCase
from lists.models import Item


class HomePageTest(TestCase):
    def test_home_uses_template(self):
        """
        тест: используется домашний шаблон
        """
        response = self.client.get("/")

        self.assertTemplateUsed(response, "home.html")

    def test_can_save_a_POST_request(self):
        """
        тест: POST запрос сохраняется
        """
        response = self.client.post("/", data={"item_text": "A new list item"})
        self.assertContains(response, "A new list item")
        self.assertTemplateUsed(response, "home.html")


class ItemModelTest(TestCase):
    """тест модели элемента списка"""

    def test_saving_and_retrieviing_items(self):
        """тест сохранения и получения элементов списка"""

        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(second_saved_item.text, "Item the second")
