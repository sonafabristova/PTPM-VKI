from abc import ABC, abstractmethod

class UserInterface(ABC):
    @abstractmethod
    def get_input(self, prompt):
        ...

    @abstractmethod
    def show_message(self, message):
        ...

class ConsoleUserInterface(UserInterface):
    def get_input(self, prompt):
        return input(prompt).strip()

    def show_message(self, message):
        print(message)