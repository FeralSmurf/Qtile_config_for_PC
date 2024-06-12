from libqtile import widget
import subprocess


class OpenWebsite(widget.TextBox):
    defaults = [
        (
            "url",
            "https://www.accuweather.com/en/ro/bucharest/287430/hourly-weather-forecast/287430",
            "URL to open",
        ),
        ("unclicked_color", "ffffff", "Color of the text before it's clicked"),
        ("clicked_color", "#a6e3a1", "Color of the text after it's clicked"),
    ]

    def __init__(self, **config):
        config.setdefault("text", "| click for more")
        widget.TextBox.__init__(self, **config)
        self.add_defaults(OpenWebsite.defaults)
        self.clicked = False

    def button_press(self, x, y, button):
        if button == 1:
            subprocess.run(["xdg-open", self.url])
            self.clicked = True
            self.foreground = self.clicked_color
            self.draw()

    def draw(self):
        if not self.clicked:
            self.foreground = self.unclicked_color
        super().draw()
