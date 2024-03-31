from abc import ABC, abstractmethod
from numpy import ndarray
from gravithon.errors import *


class Body(ABC):
    name: str
    mass: float
    position: ndarray
    velocity: ndarray

    def __str__(self):
        return \
                self.name.upper() + '\n' + \
                '-' * len(self.name) + '\n' + \
                f'Mass: {self.mass}' + '\n' + \
                f'Position: {self.position}' + '\n' + \
                f'Velocity: {self.velocity}'

    def move(self, position: ndarray):
        # check dimensions
        if len(self.position) != len(position):
            raise DimensionsError(self.name + '\'s position', len(self.position), 'added position', len(position))

        self.position += position

    def accelerate(self, velocity: ndarray):
        # check dimensions
        if len(self.velocity) != len(velocity):
            raise DimensionsError(self.name + '\'s velocity', len(self.velocity), 'added velocity', len(velocity))

        self.velocity += velocity
