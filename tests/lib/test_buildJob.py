from unittest import TestCase
from lib.build_job import BuildJob


class TestBuildJob(TestCase):
    def setUp(self):
        self.build_job = BuildJob(dict(name='Test Build Job', url='http://some/url'))

    def test_job_name_validation(self):
        self.assertRaises(ValueError, BuildJob, dict(name=None, url='http://some/url'))
        self.assertRaises(ValueError, BuildJob, dict(name='', url='http://some/url'))

    def test_num_leds_validation(self):
        self.assertRaises(ValueError, BuildJob, dict(name='some', num_leds=0, url='http://some/url'))
        self.assertRaises(ValueError, BuildJob, dict(name='some', num_leds=33, url='http://some/url'))

    def test_offset_validation(self):
        self.assertRaises(ValueError, BuildJob, dict(name='some', num_leds=2, offset=32, url='http://some/url'))
        self.assertRaises(ValueError, BuildJob, dict(name='some', num_leds=2, offset=-1, url='http://some/url'))

    def test_url_validation(self):
        self.assertRaises(ValueError, BuildJob, dict(name='some', num_leds=2, offset=32))
        self.assertRaises(ValueError, BuildJob, dict(name='some', num_leds=2, offset=-1, url=None))

    def test_default_build_job(self):
        self.assertEqual(self.build_job.name, 'Test Build Job')
        self.assertEqual(self.build_job.offset, 1)
        self.assertEqual(self.build_job.num_leds, 1)

    def test_led_addresses_for_first_index(self):
        self.assertEqual(self.build_job.led_addresses(0), [0])

    def test_led_addresses_for_multiple_leds(self):
        build_job = BuildJob(dict(name='Some Job', num_leds=4, url='http://some/url'))
        self.assertEqual(build_job.led_addresses(0), [0, 1, 2, 3])

    def test_remaining_leds_are_utilized_when_almost_exhausted(self):
        build_job = BuildJob(dict(name='Some Job', num_leds=4, url='http://some/url'))
        self.assertEqual(build_job.led_addresses(29), [29, 30, 31])

    def test_next_index_with_padding(self):
        self.assertEqual(self.build_job.next_index(0), 2)

        build_job = BuildJob(dict(name='Some Job', num_leds=4, url='http://some/url'))
        self.assertEqual(build_job.next_index(0), 5)

    def test_next_index_with_large_padding(self):
        build_job = BuildJob(dict(name='Some Job', num_leds=4, offset=5, url='http://some/url'))
        self.assertEqual(build_job.next_index(0), 9)

    def test_next_index_upper_bounds(self):
        self.assertRaises(ArithmeticError, self.build_job.next_index, 31)

    def test_coordinates(self):
        build_job = BuildJob(dict(name='Some Job', num_leds=4, url='http://some/url'))
        self.assertEqual(build_job.led_coordinates(0), [0, 4])
        self.assertEqual(build_job.led_coordinates(10), [10, 14])
        self.assertEqual(build_job.led_coordinates(29), [29, 32])

