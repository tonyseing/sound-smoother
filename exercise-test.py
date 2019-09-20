import unittest
from exercise import decimate_by_2, downsample_by_2, convolution, low_pass_filter
import numpy as np

KAISER_FILTER = [-0.01452123, -0.0155227 , 0.01667252, 0.01800633, -0.01957209, -0.0214361 , 0.02369253, 0.02647989, -0.03001054, -0.03462755, 0.04092347, 0.05001757, -0.06430831, -0.09003163, 0.15005272, 0.45015816, 0.45015816, 0.15005272, -0.09003163, -0.06430831, 0.05001757, 0.04092347, -0.03462755, -0.03001054, 0.02647989, 0.02369253, -0.0214361 , -0.01957209, 0.01800633, 0.01667252, -0.0155227 , -0.01452123]


class ExerciseTests(unittest.TestCase):
    def test_odd_length_signal(self):
        audio_signal = [1, 2, 3, 4, 5, 6, 7]
        decimated_signal = decimate_by_2(audio_signal)
        expected_signal = [1,3,5,7]
        self.assertEqual(decimated_signal, expected_signal)

    def test_even_length_signal(self):
        audio_signal = [1, 2, 3, 4, 5, 6, 7, 8]
        decimated_signal = decimate_by_2(audio_signal)
        expected_signal = [1,3,5,7]
        self.assertEqual(decimated_signal, expected_signal)

    def test_empty_signal(self):
        audio_signal = []
        decimated_signal = decimate_by_2(audio_signal)
        expected_signal = []
        self.assertEqual(decimated_signal, expected_signal)

    def test_convolution(self):
        signal = [1] * 40
        c = convolution(KAISER_FILTER, signal)
        expected = list(np.convolve(KAISER_FILTER, signal))
        np.testing.assert_almost_equal(c, expected, decimal=7)

    def test_low_pass_filter(self):
        signal = [1] * 40
        c = low_pass_filter(signal)
        expected = list(np.convolve(KAISER_FILTER, signal) * 2)
        np.testing.assert_almost_equal(c, expected, decimal=7)

    def test_downsample_by_2(self):
        signal = [1] * 40
        downsampled = downsample_by_2(signal)
        expected = list(np.convolve(KAISER_FILTER, signal) * 2)[::2]

if __name__ == '__main__':
    unittest.main()

