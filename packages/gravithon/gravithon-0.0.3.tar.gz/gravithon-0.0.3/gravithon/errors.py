class BodyNotFoundError(Exception):
    def __init__(self, name):
        message = f'Body {name} was not found in space'
        super().__init__(message)


class DimensionsError(Exception):
    def __init__(self, body1_name, body1_dimensions,
                 body2_name, body2_dimensions):
        message = f'{body1_name} has {body1_dimensions} dimensions, but {body2_name} has {body2_dimensions} dimensions'
        super().__init__(message)
