import pygame

class Character(pygame.sprite.Sprite):
    def __init__(self, name=None, posX=0, posY=0, sizeX=0, sizeY=0, sprite=None, forward=True):
        super(Character, self).__init__()
        # sprite
        image = pygame.image.load(sprite).convert_alpha()
        image = pygame.transform.scale(image, (sizeX, sizeY))
        if not forward:
            image = pygame.transform.flip(image, True, False)
        self.surf = image
        self.rect = self.surf.get_rect()

        #location
        self.posX = posX - self.surf.get_width() / 2
        self.posY = posY + self.surf.get_height()
        self.velX = 0
        self.velY = 0
        self.sizeX, self.sizeY = sizeX, sizeY

        #properties
        self.name = name
        self.forward = forward
        self.crouch = False
        self.kick = False
        self.hold = 0
        self.xAdjust = 0
        self.block = False
        self.hp = 100
    
    def changeSprite(self, sprite, oldPosY, oldSizeY, sizeX, sizeY):
        self.posY = oldPosY + (oldSizeY - sizeY)

        image = pygame.image.load(sprite).convert_alpha()
        image = pygame.transform.scale(image, (sizeX, sizeY))
        if not self.forward:
            image = pygame.transform.flip(image, True, False)
        self.surf = image
        self.rect = self.surf.get_rect()

def makeCharacter(name, posX, posY, forward):
    match name:
        case "ryu":
            return Character(name="ryu", posX=posX, posY=posY,
                            sizeX=140, sizeY=175,
                            sprite="ryu/ryu_default.png", forward=forward)
        case "ken":
            return Character(name="ken", posX=posX, posY=posY, 
                            sizeX=140, sizeY=175, 
                            sprite="ken/ken_default.png", forward=forward)
        case _:
            return None