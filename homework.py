from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        message: str = (
            "Тип тренировки: {0}; "
            "Длительность: {1:.3f} ч.; "
            "Дистанция: {2:.3f} км; "
            "Ср. скорость: {3:.3f} км/ч; "
            "Потрачено ккал: {4:.3f}."
        ).format(
            self.training_type,
            self.duration,
            self.distance,
            self.speed,
            self.calories
        )
        return message


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    H_IN_M: int = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.type = Running.__name__

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance: float = self.get_distance()
        return distance / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.type,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mean_speed: float = self.get_mean_speed()
        duration_m: float = self.duration * self.H_IN_M
        result: float = (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER
                * mean_speed
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * duration_m
        )
        return result


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER_1: float = 0.035
    CALORIES_WEIGHT_MULTIPLIER_2: float = 0.029
    KMH_IN_MS: float = 0.278
    SM_IN_M: int = 100

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: int
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.type = SportsWalking.__name__

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mean_speed_m_s: float = self.get_mean_speed() * self.KMH_IN_MS
        height_m: float = self.height / self.SM_IN_M
        result: float = (
            (
                self.CALORIES_WEIGHT_MULTIPLIER_1
                * self.weight
                + (mean_speed_m_s**2 / height_m)
                * self.CALORIES_WEIGHT_MULTIPLIER_2
                * self.weight
            )
            * self.duration
            * self.H_IN_M
        )
        return result


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: int,
        count_pool: int,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.type = Swimming.__name__

    def get_mean_speed(self) -> float:
        result: float = (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )
        return result

    def get_spent_calories(self) -> float:

        mean_speed: float = self.get_mean_speed()
        result: float = (
            (mean_speed + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.CALORIES_MEAN_SPEED_MULTIPLIER
            * self.weight
            * self.duration
        )
        return result


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    types_of_training: dict = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking
    }
    if workout_type in types_of_training:
        return types_of_training[workout_type](*data)
    return Training(*data)


def main(training: Training) -> None:
    """Главная функция."""
    INFO: InfoMessage = training.show_training_info()
    print(INFO.get_message())


if __name__ == "__main__":
    packages: list[tuple[str, list]] = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
