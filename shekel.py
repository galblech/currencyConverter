class ILS:
    # Fixed exchange value used as default in case api is not working
    exc = 0.28

    def get_value(self):
        return self.exc

    def set_value(self, exc):
        self.exc = exc

    def calculate(self, user_input):
        return user_input * self.get_value()