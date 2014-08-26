
from lib.config import Config

class BuildJob:

    def __init__(self, dictionary):
        self.name       = dictionary.get('name')
        self.num_leds   = dictionary.get('num_leds', 1)
        self.offset     = dictionary.get('offset', 1)
        self.success    = dictionary.get('success', '__RANDOM')
        self.failure    = dictionary.get('failure', '__RANDOM')

        if self.name is None or self.name.strip() == '':
            raise ValueError('Name must not be blank')

        if self.num_leds <= 0 or self.num_leds >= Config.total_number_leds:
            raise ValueError('Invalid num_leds')

        if self.offset < 0 or self.offset >= Config.total_number_leds:
            raise ValueError('Invalid offset')


    #Returns the array of led indecies this job will occupy at the given index
    def led_addresses(self, index):
        return range(index, min(index + self.num_leds, Config.total_number_leds))

    def led_coordinates(self, index):
        addresses = self.led_addresses(index)
        return [addresses[0], (addresses[-1] + 1)]

    def next_index(self, index):
        if index >= Config.total_number_leds - 1:
            raise ArithmeticError('No leds available')
        return self.num_leds + self.offset + index

    @staticmethod
    def from_dictionaries(dictionaries):
        jobs = list()
        for job_description in dictionaries:
            jobs.append( BuildJob(job_description) )
        return jobs
