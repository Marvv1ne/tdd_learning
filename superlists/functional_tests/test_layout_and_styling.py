import time
import os
from unittest import skip

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    """Тест макета и стилевого оформления"""

    def test_layout_and_styling(self):
        """тест макета и стилевого оформления"""
        # Пользователь открывает домашнюю страницу
        self.browser.get(self.live_server_url)

        window_size = self.browser.get_window_size()
        expected_center = window_size["width"] / 2

        # Он замечает, что поле ввода аккуратно центрировано
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            expected_center,
            delta=50,
        )
        # Он начинает новый список и видит, что полу ввода там тоже
        # аккуратно центрировано
        inputbox.send_keys("testing")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: testing")
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            expected_center,
            delta=50,
        )
