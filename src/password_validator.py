def validate_password(password: str) -> bool:

    # --- Здесь будет веселуха по срезовой. Проверка исключений ---
    if not isinstance(password, str):
        raise TypeError("Пароль должен быть строкой")

    if ' ' in password:
        raise ValueError("Пароль не должен содержать пробелы")

    # --- Этап 2. Проверка критериев ---
    # 1. Длина от 8 до 20 включительно
    if not (8 <= len(password) <= 20):
        return False

    # 2. Наличие заглавной буквы
    if not any(c.isupper() for c in password):
        return False

    # 3. Наличие строчной буквы
    if not any(c.islower() for c in password):
        return False

    # 4. Наличие цифры
    if not any(c.isdigit() for c in password):
        return False

    # 5. Наличие спецсимвола из разрешённого списка
    spec_chars = "!@#$%^&*"
    if not any(c in spec_chars for c in password):
        return False

    return True