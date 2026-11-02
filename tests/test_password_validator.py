import unittest
from src.password_validator import validate_password

class TestPasswordValidator(unittest.TestCase):

    # 1. Позитивное тестирование
    def test_valid_password_latin(self):
        self.assertTrue(validate_password("SecurePass1!"))

    def test_valid_password_cyrillic(self):
        self.assertTrue(validate_password("ПарольТест9#"))

    # 2. Анализ граничных значений длины (BVA)
    def test_boundary_length_7(self):
        self.assertFalse(validate_password("Aa1!aaa"))

    def test_boundary_length_8(self):
        self.assertTrue(validate_password("Aa1!aaaa"))

    def test_boundary_length_20(self):
        self.assertTrue(validate_password("Aa1!aaaaaaaaaaaaaaaa"))

    def test_boundary_length_21(self):
        self.assertFalse(validate_password("Aa1!aaaaaaaaaaaaaaaaa"))

    # 3. Классы эквивалентности (отсутствие символов)
    def test_missing_uppercase(self):
        self.assertFalse(validate_password("securepass1!"))

    def test_missing_lowercase(self):
        self.assertFalse(validate_password("SECUREPASS1!"))

    def test_missing_digit(self):
        self.assertFalse(validate_password("SecurePassword!"))

    def test_missing_special_char(self):
        self.assertFalse(validate_password("SecurePassword1"))

    def test_invalid_special_char(self):
        self.assertFalse(validate_password("SecurePass1_"))

    # 4. Тестирование исключительных ситуаций
    def test_space_inside_raises_value_error(self):
        with self.assertRaises(ValueError):
            validate_password("Pass 1234!")

    def test_space_at_start_raises_value_error(self):
        with self.assertRaises(ValueError):
            validate_password(" Pass1234!")

    def test_space_at_end_raises_value_error(self):
        with self.assertRaises(ValueError):
            validate_password("Pass1234! ")

    def test_invalid_type_int_raises_type_error(self):
        with self.assertRaises(TypeError):
            validate_password(12345678)

    def test_invalid_type_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            validate_password(None)

    def test_invalid_type_list_raises_type_error(self):
        with self.assertRaises(TypeError):
            validate_password(["P", "a", "s", "s"])

if __name__ == "__main__":
    unittest.main()