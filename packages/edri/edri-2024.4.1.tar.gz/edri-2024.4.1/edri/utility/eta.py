from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Union, List


class ETA:
    # @dataclass
    # class ETARecord:
    #     progress: float
    #     delta: timedelta

    history_count = 10

    class Form:
        @staticmethod
        def seconds(quantity: int) -> str:
            if quantity == 1:
                return "sekunda"
            elif 2 <= quantity <= 4:
                return "sekundy"
            else:
                return "sekund"

    def __init__(self) -> None:
        # self.records: list[ETA.ETARecord] = []
        self.start = datetime.now()
        self.minimum: float = 0.0
        self.maximum: float = 0.0
        self.average: float = 0.0
        self.average_count: int = 0
        self.variance_list: List[float] = []

    def add_record(self, progress: float) -> None:
        current_average = progress / (datetime.now() - self.start).total_seconds()

        self.variance_list.append(abs(current_average - self.average))
        if len(self.variance_list) > self.history_count:
            self.variance_list.pop(0)

        current_average = (self.average * self.average_count + current_average)
        self.average_count += 1

        try:
            self.average = current_average / self.average_count
        except ZeroDivisionError:
            self.average = current_average

    def get_estimation(self) -> Union[str, None]:
        elapsed = datetime.now() - self.start
        remaining = (1 / self.average) - elapsed.total_seconds()
        variance = (sum(self.variance_list) / len(self.variance_list)) * 100
        variance = remaining * variance  # max(0.05, variance)
        return f"Zbývá: {remaining} +- {variance}"
