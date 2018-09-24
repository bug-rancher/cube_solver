from .element import Element


class Corner(Element):
    def __init__(self, stickers):
        super(Corner, self).__init__(stickers)

        self.r_0 = [self.stickers[0].color, self.stickers[1].color, self.stickers[2].color]
        self.r_1 = [self.stickers[2].color, self.stickers[0].color, self.stickers[1].color]
        self.r_2 = [self.stickers[1].color, self.stickers[2].color, self.stickers[0].color]
