from collections import OrderedDict
import unittest

from test_util import ScanPointGeneratorTest
from scanpointgenerator import LineGenerator


class LineGeneratorTest(ScanPointGeneratorTest):

    def setUp(self):
        self.g = LineGenerator("x", "mm", 1.0, 9.0, 5, alternate_direction=True)

    def test_init(self):
        self.assertEqual(self.g.position_units, dict(x="mm"))
        self.assertEqual(self.g.index_dims, [5])
        self.assertEqual(self.g.index_names, ["x"])

    def test_iterator(self):
        positions = [1.0, 3.0, 5.0, 7.0, 9.0]
        lower = [0.0, 2.0, 4.0, 6.0, 8.0]
        upper = [2.0, 4.0, 6.0, 8.0, 10.0]
        indexes = [0, 1, 2, 3, 4]
        for i, p in enumerate(self.g.iterator()):
            self.assertEqual(p.positions, dict(x=positions[i]))
            self.assertEqual(p.lower, dict(x=lower[i]))
            self.assertEqual(p.upper, dict(x=upper[i]))
            self.assertEqual(p.indexes, [indexes[i]])
        self.assertEqual(i, 4)

    def test_to_dict(self):
        expected_dict = OrderedDict()
        expected_dict['type'] = "LineGenerator"
        expected_dict['name'] = "x"
        expected_dict['units'] = "mm"
        expected_dict['start'] = [1.0]
        expected_dict['stop'] = [9.0]
        expected_dict['num'] = 5
        expected_dict['alternate_direction'] = True

        d = self.g.to_dict()

        self.assertEqual(expected_dict, d)

    def test_from_dict(self):
        _dict = OrderedDict()
        _dict['name'] = "x"
        _dict['units'] = "mm"
        _dict['start'] = [1.0]
        _dict['stop'] = [9.0]
        _dict['num'] = 5
        _dict['alternate_direction'] = True

        units_dict = OrderedDict()
        units_dict['x'] = "mm"

        gen = LineGenerator.from_dict(_dict)

        self.assertEqual("x", gen.name)
        self.assertEqual(units_dict, gen.position_units)
        self.assertEqual([1.0], gen.start)
        self.assertEqual([9.0], gen.stop)
        self.assertEqual(5, gen.num)
        self.assertTrue(gen.alternate_direction)


class LineGenerator2DTest(ScanPointGeneratorTest):

    def setUp(self):
        self.g = LineGenerator("XYLine", "mm", [1.0, 2.0], [5.0, 10.0], 5)

    def test_init(self):
        self.assertEqual(self.g.position_units, dict(XYLine_X="mm", XYLine_Y="mm"))
        self.assertEqual(self.g.index_dims, [5])
        self.assertEqual(self.g.index_names, ["XYLine"])

    def test_given_inconsistent_dims_then_raise_error(self):

        with self.assertRaises(ValueError):
            LineGenerator("x", "mm", [1.0], [5.0, 10.0], 5)

    def test_numbered_axes_names_generated(self):
        l = LineGenerator("5DScan", "mm", [0.0]*5, [10.0]*5, 5)
        self.assertEqual(l.axes, ["5DScan_X", "5DScan_Y", "5DScan_Z", "5DScan_4", "5DScan_5"])

    def test_give_one_point_then_step_zero(self):
        l = LineGenerator("5DScan", "mm", [0.0]*5, [10.0]*5, 1)
        self.assertEqual(l.step, [0]*5)

    def test_iterator(self):
        x_positions = [1.0, 2.0, 3.0, 4.0, 5.0]
        y_positions = [2.0, 4.0, 6.0, 8.0, 10.0]
        lower = [0.5, 1.5, 2.5, 3.5, 4.5]
        upper = [1.5, 2.5, 3.5, 4.5, 5.5]
        indexes = [0, 1, 2, 3, 4]
        for i, p in enumerate(self.g.iterator()):
            self.assertEqual(p.positions, dict(XYLine_X=x_positions[i],
                                               XYLine_Y=y_positions[i]))
            self.assertEqual(p.lower["XYLine_X"], lower[i])
            self.assertEqual(p.upper["XYLine_X"], upper[i])
            self.assertEqual(p.indexes, [indexes[i]])
        self.assertEqual(i, 4)

if __name__ == "__main__":
    unittest.main()



