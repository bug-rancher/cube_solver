from .element import Element


class Center(Element):
    def __init__(self, stickers):
        super(Center, self).__init__(stickers)

        self.color = self.stickers[0].color
