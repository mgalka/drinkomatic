import drinkomatic

VODKA_RELAY = 16
JUICE_RELAY = 18
BUZZER_PIN = 37
dear_assistant = drinkomatic.Drinkomatic(VODKA_RELAY, JUICE_RELAY, BUZZER_PIN)
vodka_recipe = {
    0: 20
}

drink_recipe = {
    0: 20,
    1: 80
}

if __name__ == '__main__':
    print('Preparing vodka...')
    dear_assistant.prepare_drink(vodka_recipe)
    print('Preparing.drink...')
    dear_assistant.prepare_drink(drink_recipe)