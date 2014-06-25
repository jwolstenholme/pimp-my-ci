from lib.const import *

class BuildJob:
    max_leds = MAX_LEDS

    def __init__(self, name, num_leds=1, offset=1):
        if name is None or name.strip() == '':
            raise ValueError('Name must not be blank')

        if num_leds <= 0 or num_leds >= self.max_leds:
            raise ValueError('Invalid num_leds')

        if offset < 0 or offset >= self.max_leds:
            raise ValueError('Invalid offset')

        self.name = name
        self.num_leds = num_leds
        self.offset = offset

    def led_addresses(self, index):
        return range(index, min(index + self.num_leds, self.max_leds))

    def next_index(self, index):
        if index >= self.max_leds - 1:
            raise ArithmeticError('No leds available')
        return self.num_leds + self.offset + index



