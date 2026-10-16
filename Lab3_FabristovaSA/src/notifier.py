from abc import ABC, abstractmethod


class Notifier(ABC):
    """Интерфейс отправки данных во внешнюю систему."""

    @abstractmethod
    def send(self, message):
        """Отправить строку во внешний сервер. Вернуть True при успехе."""
        ...


class EmailNotifier(Notifier):
    """Имитация отправки на email-сервер. Реального сетевого вызова нет."""

    def send(self, message):
        print(f"[EMAIL] Отправлено: {message}")
        return True