from dataclasses import dataclass, asdict
from typing import List, Union


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    OUT_MESSAGE_RU = ('Тип тренировки: {training_type}; '
                      'Длительность: {duration:.3f} ч.; '
                      'Дистанция: {distance:.3f} км; '
                      'Ср. скорость: {speed:.3f} км/ч; '
                      'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Возвращает f-строку, с данными, которые надо подать на вывод."""
        data = asdict(self)
        mes = self.OUT_MESSAGE_RU.format(training_type=data['training_type'],
                                         duration=data['duration'],
                                         distance=data['distance'],
                                         speed=data['speed'],
                                         calories=data['calories'])
        return mes


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
        raise NotImplementedError
        # Проверяет, что метод переопределен в дочернем классе.

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.__class__.__name__
        duration_main = self.duration
        distance_main = self.get_distance()
        speed_main = self.get_mean_speed()
        calories = self.get_spent_calories()
        final_message = InfoMessage(training_type,
                                    duration_main,
                                    distance_main,
                                    speed_main,
                                    calories)
        return final_message


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1 = 18  # внешний коэффициент для формулы
    COEFF_CALORIE_2 = 20  # внешний коэффициент для формулы

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Метод расчета калорий для бега. Берёт всё из род. класса."""
        spent_calories = ((self.COEFF_CALORIE_1
                          * super().get_mean_speed()
                          - self.COEFF_CALORIE_2) * self.weight / self.M_IN_KM
                          * self.duration * self.MIN_IN_HOUR)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_1 = 0.035  # внешний коэффициент для формулы
    COEFF_CALORIE_2 = 0.029  # внешний коэффициент для формулы

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)

        self.height = height

    def get_spent_calories(self) -> float:
        """Метод расчета калорий для ходьбы."""
        spent_calories = ((self.COEFF_CALORIE_1 * self.weight
                          + (super().get_mean_speed()**2
                             // self.height)
                          * self.COEFF_CALORIE_2 * self.weight)
                          * self.duration * self.MIN_IN_HOUR)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    COEFF_CALORIE_1 = 1.1  # внешний коэффициент для формулы
    COEFF_CALORIE_2 = 2.0  # внешний коэффициент для формулы

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
        spent_calories = ((self.get_mean_speed()
                          + self.COEFF_CALORIE_1) * self.COEFF_CALORIE_2
                          * self.weight)
        return spent_calories


def read_package(workout_type: str,
                 data: List[Union[int, float]]) -> Union[Training, None]:
    """Прочитать данные полученные от датчиков."""

    TRAIN = {'SWM': Swimming,
             'RUN': Running,
             'WLK': SportsWalking}
    try:
        training_actual = TRAIN[workout_type](*data)
        return training_actual
    except KeyError:
        print('Неизвестная кодировка типа тренировки.')
        return None


def main(training: Union[Training, None]) -> None:
    """Главная функция."""

    try:
        info = InfoMessage.get_message(training.show_training_info())
        print(info)
    except AttributeError:
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
