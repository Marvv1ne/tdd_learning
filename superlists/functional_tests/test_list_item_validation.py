from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    """Тест валидации элементов списка"""

    def test_cannot_add_empty_list_items(self):
        """тест: нельзя добавлять пустые элементы списка"""
        # Пользователь открывает домашнюю страницу и случайно
        # пытается отправить пустой элемент списка.
        # Он нажимает Enter на пустом поле ввода.
        self.browser.get(self.live_server_url)

        self.browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)
        # Домашняя страница обновляется, и появляется сообщение
        # об ошибке, которое говорит, что элементы списка не должны
        # быть пустыми.

        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element(By.CSS_SELECTOR, ".has_error").text,
                "You can't have an empty list item",
            )
        )
        # Он пробует снова, теперь с неким текстом для элемента,
        # и теперь это срабатывает.
        self.browser.find_element(By.ID, "id_new_item").send_keys("Изучить ООП")
        self.browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Изучить ООП")
        # Как ни странно, пользователь решает отправить второй пустой
        # элемент списка.
        self.browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)
        # Он получает аналогичное предупреждение на странице списка.
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element(By.CSS_SELECTOR, ".has_error").text,
                "You can't have an empty list item",
            )
        )
        # И он может его исправить, заполнив поле неким текстом.
        self.browser.find_element(By.ID, "id_new_item").send_keys("Изучить ФП")
        self.browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Изучить ООП")
        self.wait_for_row_in_list_table("2: Изучить ФП")
