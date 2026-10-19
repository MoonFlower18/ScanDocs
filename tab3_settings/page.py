from core.placeholder import PlaceholderPage


class SettingsPage(PlaceholderPage):
    def __init__(self, parent):
        super().__init__(
            parent,
            title="Настройки",
            subtitle="Настройки словарей и пути",
            hint="Тут чет будет",
        )