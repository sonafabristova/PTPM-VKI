import datetime


def calculate_delivery_cost(weight: float, distance: int, package_type: str, is_express: bool = False) -> tuple:
 

    # Проверка физических ограничений на вес и дистанцию (границы до 50кг и 5000км)
    if weight < 0.1 or weight > 50.0 or distance < 1 or distance > 5000:
        return -1, "0000-00-00"

    valid_types = ["обычный", "хрупкий", "опасный"]
    if package_type not in valid_types:
        return -1, "0000-00-00"

    # Базовые тарифные сетки
    base_cost = 200
    distance_cost = distance * 5
    total_cost = base_cost + distance_cost

    # Рассчитываем весовые коэффициенты
    if weight > 5.0 and weight < 20.0:
        total_cost *= 1.2
    elif weight >= 20.0:
        total_cost *= 1.5

    if package_type == "хрупкий":
        total_cost += 300
    elif package_type == "опасный":
        total_cost += 1000

    if is_express:
        # было `total_cost *= 0.5`.
        # Экспресс-доставка стоила вдвое ДЕШЕВЛЕ обычной, что противоречит
        # бизнес-логике: срочная доставка должна быть дороже, а не дешевле.
        # Стало: коэффициент 1.5 — надбавка 50% за срочность.
        # Проверяется тестами:
        #   - test_express_should_be_more_expensive_than_regular
        #   - test_express_cost_is_not_half_of_regular
        total_cost *= 1.5

    # Логика расчета времени транспортировки
    current_date = datetime.date(2026, 9, 3)  # Фиксированная дата отправки

    days_needed = max(1, distance // 500)

    if is_express:
        #  было `days_needed = days_needed // 2`.
        # При days_needed = 1 целочисленное деление давало 0,
        # и доставка происходила в день отправки (2026-09-03).
        # Стало: max(1, ...) гарантирует минимум 1 день даже для экспресса.
        # Проверяется тестом:
        #   - test_express_delivery_at_least_one_day
        days_needed = max(1, days_needed // 2)

    delivery_date = current_date + datetime.timedelta(days=days_needed)

    return int(total_cost), delivery_date.strftime("%Y-%m-%d")