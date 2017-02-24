import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import unittest

from test_util import ScanPointGeneratorTest
from scanpointgenerator import SpiralGenerator


class SpiralGeneratorTest(unittest.TestCase):

    def setUp(self):
        self.g = SpiralGenerator(['x', 'y'], ["cm", "mm"], [0.0, 0.0], 1.4, alternate_direction=True)

    def test_init(self):
        self.assertEqual(self.g.units, dict(x="cm", y="mm"))
        self.assertEqual(self.g.axes, ["x", "y"])

    def test_duplicate_name_raises(self):
        with self.assertRaises(ValueError):
            SpiralGenerator(["x", "x"], ["mm", "mm"], [0.0, 0.0], 1.0)

    def test_array_positions(self):
        positions = [{'y': -0.3211855677650875, 'x': 0.23663214944574582},
                     {'y': -0.25037538922751695, 'x': -0.6440318266552169},
                     {'y': 0.6946549630820702, 'x': -0.5596688286164636},
                     {'y': 0.9919687803189761, 'x': 0.36066957248394327},
                     {'y': 0.3924587351155914, 'x': 1.130650533568409},
                     {'y': -0.5868891557832875, 'x': 1.18586065489788},
                     {'y': -1.332029488076613, 'x': 0.5428735608675326}]
        bounds = [{'y':0.0, 'x':0.0},
                 {'y': -0.5189218293602549, 'x': -0.2214272368007088},
                 {'y': 0.23645222432582483, 'x': -0.7620433832656455},
                 {'y': 0.9671992383675001, 'x': -0.13948222773063082},
                 {'y': 0.7807653675717078, 'x': 0.8146440851904461},
                 {'y': -0.09160107657707395, 'x': 1.2582363345925418},
                 {'y': -1.0190886264001306, 'x': 0.9334439933089926},
                 {'y': -1.4911377166541206, 'x': 0.06839234794968006}]
        self.g.prepare_positions()
        self.g.prepare_bounds()
        p = [{"x":x, "y":y} for (x, y) in zip(self.g.positions['x'], self.g.positions['y'])]
        b = [{"x":x, "y":y} for (x, y) in zip(self.g.bounds['x'], self.g.bounds['y'])]
        self.assertEqual(positions, p)
        self.assertEqual(bounds, b)

    def test_to_dict(self):
        expected_dict = dict()
        expected_dict['typeid'] = "scanpointgenerator:generator/SpiralGenerator:1.0"
        expected_dict['axes'] = ['x', 'y']
        expected_dict['units'] = ['cm', 'mm']
        expected_dict['centre'] = [0.0, 0.0]
        expected_dict['radius'] = 1.4
        expected_dict['scale'] = 1
        expected_dict['alternate_direction'] = True

        d = self.g.to_dict()

        self.assertEqual(expected_dict, d)

    def test_from_dict(self):
        _dict = dict()
        _dict['type'] = "SpiralGenerator"
        _dict['axes'] = ["x", "y"]
        _dict['units'] = ["mm", "cm"]
        _dict['centre'] = [0.0, 0.0]
        _dict['radius'] = 1.4
        _dict['scale'] = 1
        _dict['alternate_direction'] = True

        units_dict = dict()
        units_dict['x'] = "mm"
        units_dict['y'] = "cm"

        gen = SpiralGenerator.from_dict(_dict)

        self.assertEqual(["x", "y"], gen.axes)
        self.assertEqual(["x_y_Spiral"], gen.index_names)
        self.assertEqual(units_dict, gen.units)
        self.assertEqual([0.0, 0.0], gen.centre)
        self.assertEqual(1.4, gen.radius)
        self.assertEqual(1, gen.scale)

if __name__ == "__main__":
    unittest.main(verbosity=2)
