import unittest

from selenium import webdriver


class NewVisitorTest(unittest.TestCase):
    "Тест первого посетителя"

    def setUp(self) -> None:
        "Установка"

        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        "Демонтаж"

        self.browser.quit()

    def test_can_start_a_list_and_retrive_it_later(self) -> None:
        self.browser.get("http://localhost:8000")

        self.assertIn("To-Do", self.browser.title)
        self.fail("Need to finish test")


if __name__ == "__main__":
    unittest.main(warnings="ignore")
