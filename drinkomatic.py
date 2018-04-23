from RPi import GPIO
import time
from collections import namedtuple
from queue import Queue
import threading


Dispensers = namedtuple('Dispensers', ['vodka', 'juice'])


class Dispenser:
    def __init__(self, relay, time_per_10ml=1.4):
        self.relay = relay
        self.time_per_10ml = time_per_10ml

    def start_pouring(self):
        GPIO.output(self.relay, GPIO.LOW)

    def stop_pouring(self):
        GPIO.output(self.relay, GPIO.HIGH)

    def pour_time(self, seconds):
        self.start_pouring()
        time.sleep(seconds)
        self.stop_pouring()

    def pour_amount(self, ml):
        seconds = (self.time_per_10ml * ml) / 10
        self.pour_time(seconds)


class Buzzer:
    def __init__(self, pin):
        self.pin = pin

    def beep(self, count, beep_time=1):
        for _ in range(count):
            print('beep {}'.format(_))
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(beep_time)
            GPIO.output(self.pin, GPIO.LOW)
            time.sleep(0.1)


class Drinkomatic:
    def __init__(self, vodka_relay, juice_relay, buzzer_pin):
        self.dispensers = Dispensers(Dispenser(vodka_relay, time_per_10ml=1.4),
                                     Dispenser(juice_relay, time_per_10ml=0.91))
        self.buzzer = Buzzer(buzzer_pin)
        self.drink_queue = Queue()
        self._prepare_thread = threading.Thread(target=self._prepare_drink)
        print('thread start')
        self._prepare_thread.start()
        print('rpi init')
        self._init_rpi()
        print('init done')

    def _init_rpi(self):
        GPIO.setmode(GPIO.BOARD)
        for dispenser in self.dispensers:
            GPIO.setup(dispenser.relay, GPIO.OUT)
            GPIO.output(dispenser.relay, GPIO.HIGH)
        GPIO.setup(self.buzzer.pin, GPIO.OUT)
        GPIO.output(self.buzzer.pin, GPIO.LOW)

    def _cleanup(self):
        for dispenser in self.dispensers:
            GPIO.output(dispenser.relay, GPIO.HIGH)
        GPIO.output(self.buzzer.pin, GPIO.LOW)
        GPIO.cleanup()

    def stop(self):
        print('stop')
        self.drink_queue.put(None)
        self._prepare_thread.join()
        self._cleanup()

    def prepare_drink(self, recipe):
        self.drink_queue.put(recipe)

    def _prepare_drink(self):
        while True:
            print('wait for recipe')
            recipe = self.drink_queue.get()
            print(recipe)
            if recipe is None:
                break
            for disp, amount in recipe.items():
                dispenser = self.dispensers[disp]
                dispenser.pour_amount(amount)