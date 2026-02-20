import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class NewVisitorTest(LiveServerTestCase):
    """Тест первого посетителя"""

    def setUp(self) -> None:
        """Установка"""

        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        """Демонтаж"""

        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        """Подтверждение строки в таблице списка"""
        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrive_it_later(self) -> None:
        # Посетитель открывает браузер Firefox заходит на домашнюю страницу веб приложения
        self.browser.get(self.live_server_url)

        # На домашней странице посетитель видит заголовок To-Do
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1")
        self.assertEqual("Your To-Do list", header_text.text)

        # Посетителю сразу же предлагается ввести элемент списка
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")
        # Пользователь набирает в текстовом поле "Изучить TDD"
        inputbox.send_keys("Изучить TDD")

        # После нажатия Enter страница обновляется и теперь на странице
        # отображается "1: Изучить TDD" в качестве элемента списка
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")

        # Текстовое поле по-прежнему предлагает добавить еще один элемент
        # Пользователь вводить "изучить DDD"

        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Изучить DDD")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")

        self.check_for_row_in_list_table("1: Изучить TDD")

        self.check_for_row_in_list_table("2: Изучить DDD")

        self.fail("Need to finish test")


if __name__ == "__main__":
    unittest.main(warnings="ignore")
