class Controller:
    def __init__(self, calculator, database, user_interface, notifier):
        self.calculator = calculator
        self.database = database
        self.ui = user_interface
        self.notifier = notifier

    def run_scenario(self):
        s1 = self.ui.get_input("Сторона A: ")
        s2 = self.ui.get_input("Сторона B: ")
        s3 = self.ui.get_input("Сторона C: ")

        cached = self.database.get_record(s1, s2, s3)

        if cached is not None:
            kind, error = cached
        else:
            kind, error = self.calculator.process_triangle(s1, s2, s3)
            self.database.add_record(s1, s2, s3, kind, error)

        self.notifier.send(f"Треугольник ({s1}, {s2}, {s3}): {kind}")

        return kind