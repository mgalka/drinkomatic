import unittest
from unittest import mock
import sys

mock.patch.dict('sys.modules', RPi=mock.MagicMock()).start()

class TestDrinkomatic(unittest.TestCase):

    @mock.patch('RPi.GPIO')
    def test_threading(self, mock_gpio):
        from drinkomatic import Drinkomatic
        VODKA_RELAY_PIN = 16
        JUICE_RELAY_PIN = 18
        BUZZER_PIN = 37
        dear_assistant = Drinkomatic(VODKA_RELAY_PIN, JUICE_RELAY_PIN, BUZZER_PIN)
        vodka_recipe = {
            0: 20
        }

        drink_recipe = {
            0: 20,
            1: 80
        }
        try:
            print('Preparing vodka...')
            dear_assistant.prepare_drink(vodka_recipe)
            print('Preparing.drink...')
            dear_assistant.prepare_drink(drink_recipe)
        finally:
            dear_assistant.stop()


if __name__ == '__main__':
    unittest.main()