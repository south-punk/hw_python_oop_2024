M_IN_KM : int = 1000
KM_H_IN_M_H: float = 1000 / 3600
H_IN_MIN: int = 60
METER: int = 100


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: int,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
    
    def get_message(self) -> str:
        print(f'Тип тренировки: {self.training_type}; '
              f'Длительность:  {self.duration:.3f} ч.; '
              f'Дистанция: {self.distance:.3f} км; '
              f'Ср. скорость: {self.speed:.3f} км/ч; '
              f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: int,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> None:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self, # type(self).__name__
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER *
                 self.get_mean_speed() +
                 self.CALORIES_MEAN_SPEED_SHIFT) *
                 self.weight / M_IN_KM *
                 self.duration * H_IN_MIN)

    def __str__(self) -> str:
        return 'Бег'


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEF_1: int = 0.035
    COEF_2: int = 0.029

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: int,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.COEF_1 * self.weight +
                ((self.get_mean_speed() * KM_H_IN_M_H)**2 /
                (self.height / METER)) *
                self.COEF_2 * self.weight) * self.duration * H_IN_MIN)
    
    def __str__(self) -> str:
        return 'Спортивная ходьба'


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    COEF_1 = 1.1
    COEF_2 = 2

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: int,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
    
    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / M_IN_KM / self.duration)
    
    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEF_1) *
                self.COEF_2 * self.weight * self.duration)
    
    def __str__(self) -> str:
        return 'Плавание'


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'SWM':
        return Swimming(*data)
    elif workout_type == "RUN":
        return Running(*data)
    else:
        return SportsWalking(*data)

def main(training: Training) -> InfoMessage:
    """Главная функция."""
    info = training.show_training_info()
    return info.get_message()


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
