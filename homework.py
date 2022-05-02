class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Возвращает f-строку, с данными, которые надо подать на вывод."""

        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')
    pass


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HOUR = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return self.get_spent_calories()
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        try:
            training_type = self.__class__.__name__
            duration_main = self.duration
            distance_main = self.get_distance()
            speed_main = self.get_mean_speed()
            calories = self.get_spent_calories()
            return InfoMessage(training_type,
                               duration_main,
                               distance_main,
                               speed_main,
                               calories)
        except TypeError:
            pass


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)
        self.LEN_STEP = 0.65

    def get_spent_calories(self) -> float:
        """Метод расчета калорий для бега. Берёт всё из род. класса."""

        coeff_calorie_1 = 18  # внешний коэффициент для формулы
        coeff_calorie_2 = 20  # внешний коэффициент для формулы
        spent_calories = ((coeff_calorie_1
                          * super().get_mean_speed()
                          - coeff_calorie_2) * self.weight / self.M_IN_KM
                          * self.duration * self.MIN_IN_HOUR)
        return spent_calories
    pass


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)

        self.height = height

    def get_spent_calories(self) -> float:
        """Метод расчета калорий для ходьбы."""

        coeff_calorie_1 = 0.035  # внешний коэффициент для формулы
        coeff_calorie_2 = 0.029  # внешний коэффициент для формулы

        spent_calories = ((coeff_calorie_1 * self.weight
                          + (super().get_mean_speed()**2
                             // self.height)
                          * coeff_calorie_2 * self.weight)
                          * self.duration * self.MIN_IN_HOUR)
        return spent_calories

    pass


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)

        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Метод расчета средней скорости для плавания"""

        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Метод расчёта калорий для плавания."""

        coeff_calorie_1 = 1.1  # внешний коэффициент для формулы
        coeff_calorie_2 = 2.0  # внешний коэффициент для формулы
        spent_calories = ((self.get_mean_speed()
                          + coeff_calorie_1) * coeff_calorie_2 * self.weight)
        return spent_calories
    pass


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    TRAIN = {'SWM': Swimming,
             'RUN': Running,
             'WLK': SportsWalking}
    training_actual = TRAIN[workout_type](*data)
    return training_actual
    pass


def main(training: Training) -> None:
    """Главная функция."""

    try:
        info = InfoMessage.get_message(training.show_training_info())
        print(info)
    except TypeError:
        pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
