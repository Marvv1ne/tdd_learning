import unittest
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class NewVisitorTest(unittest.TestCase):
    """Тест первого посетителя"""

    def setUp(self) -> None:
        """Установка"""

        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        """Демонтаж"""

        self.browser.quit()

    def test_can_start_a_list_and_retrive_it_later(self) -> None:
        # Посетитель открывает браузер Firefox заходит на домашнюю страницу веб приложения
        self.browser.get("http://localhost:8000")

        # На домашней странице посетитель видит заголовок To-Do
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_elements(By.TAG_NAME, "h1")
        self.assertIn("To-Do", header_text)

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
        self.assertTrue(any(row.text == "1: Изучить TDD" for row in rows))

        # Текстовое поле по-прежнему предлагает добавить еще один элемент
        # Пользователь вводить "изучить DDD"

        inputbox.send_keys("Изучить DDD")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertTrue(any(row.text == "2: Изучить DDD" for row in rows))

        self.fail("Need to finish test")


if __name__ == "__main__":
    unittest.main(warnings="ignore")
