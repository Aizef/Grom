class Card():
    def __init__(self, character, button):
        self.button, self.character = button, character

    def __getitem__(self, item):
        if item == 0:
            return self.character
        else:
            return self.button

    def draw(self, surface):
        self.button.draw(surface)