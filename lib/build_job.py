
class BuildJob:

    def __init__(self, total_leds, name, num_leds=1, offset=1):
        self.total_leds = total_leds

        if name is None or name.strip() == '':
            raise ValueError('Name must not be blank')

        if num_leds <= 0 or num_leds >= total_leds:
            raise ValueError('Invalid num_leds')

        if offset < 0 or offset >= total_leds:
            raise ValueError('Invalid offset')

        self.name = name
        self.num_leds = num_leds
        self.offset = offset

    #Returns the array of led indecies this job will occupy at the given index
    def led_addresses(self, index):
        return range(index, min(index + self.num_leds, self.total_leds))

    def led_coordinates(self, index):
        addresses = self.led_addresses(index)
        return [addresses[0], (addresses[-1] + 1)]

    def next_index(self, index):
        if index >= self.total_leds - 1:
            raise ArithmeticError('No leds available')
        return self.num_leds + self.offset + index
