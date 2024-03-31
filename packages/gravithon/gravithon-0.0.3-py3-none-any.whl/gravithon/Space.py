from numpy import array, ndarray
from gravithon.Body import Body
from gravithon.errors import *
from multipledispatch import dispatch


class Space:
    def __str__(self):
        string = ''

        # bodies
        string += f'{len(self.bodies)} BODIES:\n'
        for body in self.bodies:
            # indent body's string
            for line in str(body).split('\n'):
                string += '\t' + line + '\n'

            string += '\n'

        # time
        string += f'Time: {self.time}'

        return string

    def __init__(self, dimensions: int):
        self.bodies = []
        self.time = float(0)
        self.dimensions = dimensions

    def add_body(self, body: Body, position: ndarray, velocity: ndarray = None):
        # check dimensions
        if len(position) != self.dimensions:
            # dimensions doesn't match
            raise DimensionsError('Space', self.dimensions, body.name + '\'s position', len(position))

        if velocity is not None and len(velocity) != self.dimensions:
            raise DimensionsError('Space', self.dimensions, body.name + '\'s velocity', len(velocity))

        # check if body has been already added
        for existing_body in self.bodies:
            if body.name == existing_body.name:
                raise Exception(f'A body named "{body.name}" already exists in this space')

        # add body
        body.position = position
        if velocity is None:
            body.velocity = array([0] * self.dimensions)
        else:
            body.velocity = velocity

        self.bodies.append(body)

    @dispatch(Body)
    def remove_body(self, body):
        try:
            self.bodies.remove(body)
        except ValueError:
            raise BodyNotFoundError(body.name)

    @dispatch(str)
    def remove_body(self, body_name):
        # find body in bodies list
        try:
            body: Body = next(body for body in self.bodies if body.name == body_name)
        except StopIteration:
            raise BodyNotFoundError(body_name)

        self.remove_body(body)

    def step(self):
        raise NotImplementedError()
