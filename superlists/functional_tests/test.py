import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    """Тест первого посетителя"""

    def setUp(self) -> None:
        """Установка"""

        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        """Демонтаж"""

        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        """Ожидает строку в таблице списка"""
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, "id_list_table")
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

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
        self.wait_for_row_in_list_table("1: Изучить TDD")

        table = self.browser.find_element(By.ID, "id_list_table")

        # Текстовое поле по-прежнему предлагает добавить еще один элемент
        # Пользователь вводить "изучить DDD"

        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Изучить DDD")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("2: Изучить DDD")
        table = self.browser.find_element(By.ID, "id_list_table")

        self.wait_for_row_in_list_table("1: Изучить TDD")

        self.wait_for_row_in_list_table("2: Изучить DDD")
        # self.fail("Need to finish test")

    def test_multiple_users_can_start_lists_at_different_urls(self):
        """тест: многочисленные пользователи могут начать списки по разным url"""

        # Первый пользователь начинает новый список
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Изучить TDD")
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table("1: Изучить TDD")

        # Первый пользователь замечает, что его список имеет уникальный URL-адрес
        first_user_list_url = self.browser.current_url
        self.assertRegex(first_user_list_url, "/lists/.+")

        # Второй пользователь заходит на сайт
        # Используется новый сеанс браузера, тем самым обеспечивая, что бы
        # никакая информация от первого пользователя не прошла через данные cookie и пр.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Второй пользователь посещает домашнюю страницу. Нет никаких
        # признаков списка первого пользователя
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, "body").text

        self.assertNotIn("Изучить TDD", page_text)

        # Второй пользователь начинает новый список, вводя новый элемент
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Изучить ООП")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Изучить ООП")

        # Второй пользователь получает уникальный URL-адрес
        second_user_list_url = self.browser.current_url
        self.assertRegex(second_user_list_url, "/list/.+")
        self.assertNotEqual(second_user_list_url, first_user_list_url)

        # В списке второго пользователя нет элементов списка
        # первого пользователя
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Изучить TDD", page_text)
        self.assertIn("Изучить ООП", page_text)
