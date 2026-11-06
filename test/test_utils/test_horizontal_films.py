import unittest

from ochre.utils.envelope import calculate_film_resistances


class HorizontalFilmTestCase(unittest.TestCase):
    def test_warm_room_below_cold_attic(self):
        films = calculate_film_resistances(
            "Attic Floor",
            {"Exterior Zone Label": "ATC", "Interior Zone Label": "LIV", "Tilt (deg)": 0},
            {"Average Ambient Temperature (C)": 5},
        )
        enhanced = 9.482 * 12.9 ** (1 / 3) / (7.238 - 1)
        for resistance in films.values():
            self.assertAlmostEqual(1 / resistance, enhanced)

    def test_hot_attic_above_cool_room(self):
        films = calculate_film_resistances(
            "Attic Floor",
            {"Exterior Zone Label": "ATC", "Interior Zone Label": "LIV", "Tilt (deg)": 0},
            {"Average Ambient Temperature (C)": 30},
        )
        reduced = 1.810 * 12.9 ** (1 / 3) / (1.382 + 1)
        for resistance in films.values():
            self.assertAlmostEqual(1 / resistance, reduced)

    def test_vertical_surface_unchanged(self):
        films = calculate_film_resistances(
            "Interior Wall",
            {"Exterior Zone Label": "LIV", "Interior Zone Label": "LIV", "Tilt (deg)": 90},
            {},
        )
        self.assertAlmostEqual(1 / films["Interior Film Resistance (m^2-K/W)"], 1.31 * 12.9 ** (1 / 3))
