from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def send(self, message):
        ...

class EmailNotifier(Notifier):
    def send(self, message):
        print(f"[EMAIL] Отправлено: {message}")
        return True