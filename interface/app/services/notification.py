class BaseNotification:
    def send(self):
        pass


class TelegramNotification(BaseNotification):
    pass


class EmailNotification(BaseNotification):
    pass


class PhoneNotification(BaseNotification):
    pass


class PlatformNotification(BaseNotification):
    pass
