import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.delivery_service import calculate_delivery_cost


class TestDeliveryValidation(unittest.TestCase):


    def test_weight_below_minimum_returns_error(self):          #  OK
        cost, date = calculate_delivery_cost(0.05, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "000 0-00-00")

    def test_weight_zero_returns_error(self):                   #  OK
        cost, date = calculate_delivery_cost(0.0, 100, "обычный")
        self.assertEqual(cost, -1)

    def test_weight_negative_returns_error(self):               # OK
        cost, _ = calculate_delivery_cost(-1.0, 100, "обычный")
        self.assertEqual(cost, -1)

    def test_weight_above_maximum_returns_error(self):          #  OK
        cost, _ = calculate_delivery_cost(50.1, 100, "обычный")
        self.assertEqual(cost, -1)

    def test_distance_zero_returns_error(self):                 #  OK
        cost, _ = calculate_delivery_cost(5.0, 0, "обычный")
        self.assertEqual(cost, -1)

    def test_distance_negative_returns_error(self):             #  OK
        cost, _ = calculate_delivery_cost(5.0, -10, "обычный")
        self.assertEqual(cost, -1)

    def test_distance_above_maximum_returns_error(self):        #  OK
        cost, _ = calculate_delivery_cost(5.0, 5001, "обычный")
        self.assertEqual(cost, -1)

    def test_invalid_package_type_returns_error(self):          #  OK
        cost, _ = calculate_delivery_cost(5.0, 100, "неизвестный")
        self.assertEqual(cost, -1)

    def test_empty_package_type_returns_error(self):            #  OK
        cost, _ = calculate_delivery_cost(5.0, 100, "")
        self.assertEqual(cost, -1)


class TestDeliveryBaseCost(unittest.TestCase):


    def test_base_cost_for_light_package(self):                 #  OK
        cost, _ = calculate_delivery_cost(2.0, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_base_cost_for_distance_1(self):                    #  OK
        cost, _ = calculate_delivery_cost(2.0, 1, "обычный")
        self.assertEqual(cost, 205)

    def test_base_cost_for_distance_5000(self):                 #  OK
        cost, _ = calculate_delivery_cost(2.0, 5000, "обычный")
        self.assertEqual(cost, 25200)


class TestDeliveryWeightCoefficients(unittest.TestCase):


    def test_weight_between_5_and_20_gets_1_2(self):            #  OK
        cost, _ = calculate_delivery_cost(10.0, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_weight_above_20_gets_1_5(self):                    #  OK
        cost, _ = calculate_delivery_cost(25.0, 100, "обычный")
        self.assertEqual(cost, 1050)

    def test_weight_exactly_5_has_no_coefficient(self):        #  OK
        cost, _ = calculate_delivery_cost(5.0, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_weight_exactly_20_gets_1_5(self):                  #  OK
        cost, _ = calculate_delivery_cost(20.0, 100, "обычный")
        self.assertEqual(cost, 1050)


class TestDeliveryPackageType(unittest.TestCase):


    def test_fragile_adds_300(self):                            #  OK
        cost, _ = calculate_delivery_cost(2.0, 100, "хрупкий")
        self.assertEqual(cost, 1000)

    def test_dangerous_adds_1000(self):                         #  OK
        cost, _ = calculate_delivery_cost(2.0, 100, "опасный")
        self.assertEqual(cost, 1700)

    def test_normal_has_no_surcharge(self):                     #  OK
        cost, _ = calculate_delivery_cost(2.0, 100, "обычный")
        self.assertEqual(cost, 700)


class TestDeliveryExpress(unittest.TestCase):


    def test_express_should_be_more_expensive_than_regular(self):   # АААААААААА
        # AssertionError: 350 not greater than 700
        # в delivery_service.py строка `total_cost *= 0.5`
        regular_cost, _ = calculate_delivery_cost(2.0, 100, "обычный", is_express=False)
        express_cost, _ = calculate_delivery_cost(2.0, 100, "обычный", is_express=True)
        self.assertGreater(express_cost, regular_cost)

    def test_express_cost_is_not_half_of_regular(self):             # АААААААААА
        # AssertionError: 350 == 350
        # та же строка `total_cost *= 0.5`
        regular_cost, _ = calculate_delivery_cost(2.0, 100, "обычный")
        express_cost, _ = calculate_delivery_cost(2.0, 100, "обычный", is_express=True)
        self.assertNotEqual(express_cost, regular_cost // 2)

    def test_express_delivery_at_least_one_day(self):               #  ААААААААААА
        # AssertionError: '2026-09-03' == '2026-09-03'
        #  в delivery_service.py строка `days_needed = days_needed // 2`
        # (при days_needed = 1 получается 0, доставка в день отправки)
        _, date = calculate_delivery_cost(2.0, 100, "обычный", is_express=True)
        self.assertNotEqual(date, "2026-09-03")

    def test_express_faster_than_regular_for_long_distance(self):   #  OK
        _, regular_date = calculate_delivery_cost(2.0, 5000, "обычный")
        _, express_date = calculate_delivery_cost(2.0, 5000, "обычный", is_express=True)
        self.assertLess(express_date, regular_date)


class TestDeliveryDates(unittest.TestCase):


    def test_short_distance_delivers_in_one_day(self):          #  OK
        _, date = calculate_delivery_cost(2.0, 100, "обычный")
        self.assertEqual(date, "2026-09-04")

    def test_distance_500_delivers_in_one_day(self):            #  OK
        _, date = calculate_delivery_cost(2.0, 500, "обычный")
        self.assertEqual(date, "2026-09-04")

    def test_distance_1000_delivers_in_two_days(self):          #  OK
        _, date = calculate_delivery_cost(2.0, 1000, "обычный")
        self.assertEqual(date, "2026-09-05")

    def test_distance_2500_delivers_in_five_days(self):         #  OK
        _, date = calculate_delivery_cost(2.0, 2500, "обычный")
        self.assertEqual(date, "2026-09-08")

    def test_long_distance_delivers_in_ten_days(self):          #  OK
        _, date = calculate_delivery_cost(2.0, 5000, "обычный")
        self.assertEqual(date, "2026-09-13")


class TestDeliveryCombinations(unittest.TestCase):


    def test_fragile_and_express_combination(self):
        # weight=10, distance=100, хрупкий, экспресс
        # (200+500)*1.2 = 840; +300 = 1140; *1.5 = 1710
        cost, _ = calculate_delivery_cost(10.0, 100, "хрупкий", is_express=True)
        self.assertEqual(cost, 1710)

    def test_heavy_dangerous_combination(self):                 # OK
        cost, _ = calculate_delivery_cost(30.0, 200, "опасный")
        self.assertEqual(cost, 2800)


if __name__ == "__main__":
    unittest.main()