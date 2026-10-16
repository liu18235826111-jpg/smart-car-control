class Motor:
    def __init__(self, response=2.0):
        self.speed = 0.0
        self.response = response

    def update(self, control, dt):
        self.speed += self.response * (control - self.speed) * dt
        return self.speed