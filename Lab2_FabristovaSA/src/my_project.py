import logging
import sys
import math
import os


def setup_logger():
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | [%(levelname)-7s] | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("logs/file_txt.log", encoding="utf-8"),
        ],
    )
    logging.info("Логгер сконфигурирован")


def triangle_info(s1, s2, s3):
    logging.info(f"Запрос: стороны ({s1}, {s2}, {s3})")

    try:
        a, b, c = float(s1), float(s2), float(s3)
    except (ValueError, TypeError):
        logging.error(f"Нечисловые данные: ({s1}, {s2}, {s3})")
        logging.exception("Трассировка:")
        return "", [(-2, -2), (-2, -2), (-2, -2)]

    if a <= 0 or b <= 0 or c <= 0 or a + b <= c or a + c <= b or b + c <= a:
        logging.warning(f"Не треугольник: ({a}, {b}, {c})")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if math.isclose(a, b) and math.isclose(b, c):
        kind = "равносторонний"
    elif math.isclose(a, b) or math.isclose(b, c) or math.isclose(a, c):
        kind = "равнобедренный"
    else:
        kind = "разносторонний"

    coords = calculate_coordinates(a, b, c)
    logging.info(f"Результат: {kind}, координаты={coords}")
    return kind, coords


def calculate_coordinates(a, b, c):
    AB, AC, BC = c, b, a
    xC = (AC ** 2 + AB ** 2 - BC ** 2) / (2 * AB)
    yC = math.sqrt(max(AC ** 2 - xC ** 2, 0.0))

    pts = [(0.0, 0.0), (AB, 0.0), (xC, yC)]

    pad, size = 10, 80
    max_x = max(x for x, _ in pts)
    max_y = max(y for _, y in pts)
    scale = min(size / max_x, size / max_y) if max_x and max_y else 1

    return [
        (int(pad + x * scale), int(100 - pad - y * scale))
        for x, y in pts
    ]


def main():
    setup_logger()
    while True:
        s1 = input("Сторона A: ").strip()
        if s1.lower() == "q":
            break
        s2 = input("Сторона B: ").strip()
        if s2.lower() == "q":
            break
        s3 = input("Сторона C: ").strip()
        if s3.lower() == "q":
            break

        try:
            kind, coords = triangle_info(s1, s2, s3)
            print(f"  Тип: {kind!r}")
            print(f"  Координаты: {coords}")
        except Exception:
            logging.exception("Непредвиденная ошибка при обработке ввода")

    logging.info("Приложение завершено")


if __name__ == "__main__":
    main()