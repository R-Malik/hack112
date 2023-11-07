import pygame
from pygame.locals import*

def attack(self, characterMoves, other, key, screenWidth):
    distanceX = abs(self.posX - other.posX)
    distanceY = abs(self.posY - other.posY)
    if key == characterMoves['punch'] and self.hold == 0:
        self.hold = 25
        if not self.forward:
            self.posX -= 75
            self.xAdjust = 75
        if self.crouch:
            self.changeSprite(f"{self.name}/{self.name}_jab.png", self.posY, self.sizeY, 200, 125)
        else:
            self.changeSprite(f"{self.name}/{self.name}_punch.png", self.posY, self.sizeY, 200, 175)
        punchSound = pygame.mixer.Sound("sounds/punch.mp3")
        punchSound.play()
        if distanceX < 175 and distanceY < 150 and not other.crouch and not other.block:
            other.hp -= 10
            other.hold = 20
            other.changeSprite(f"{other.name}/{other.name}_hurt.png", other.posY, other.sizeY, 125, 175)
    if key == characterMoves['kick'] and self.hold == 0 and not self.crouch:
        self.hold = 25
        if not self.forward:
            self.posX -= 75
            self.xAdjust = 75
        self.changeSprite(f"{self.name}/{self.name}_kick.png", self.posY, self.sizeY, 250, 125)
        self.kick = True
        kickSound = pygame.mixer.Sound("sounds/kick.mp3")
        kickSound.play()
        if distanceX < 200 and distanceY < 150 and not other.block:
            other.hp -= 10
            other.hold = 25
            other.changeSprite(f"{other.name}/{other.name}_hurt.png", other.posY, other.sizeY, 125, 175)
    if key == characterMoves['block'] and self.hold == 0:
        blockSound = pygame.mixer.Sound("sounds/block.mp3")
        blockSound.play()
        if not self.forward:
            if self.posX < screenWidth - self.sizeX or self.velX < 0:
                self.posX += 75
        else:
            if self.posX > 20 or self.velX > 0:
                self.posX -= 75
        self.hold = 50
        self.block = True
        self.changeSprite(f"{self.name}/{self.name}_block.png", other.posY, other.sizeY, 125, 175)

def unblock(self, characterMoves, key):
    if key == characterMoves['block']:
        self.block = False
        self.changeSprite(f"{self.name}/{self.name}_default.png", self.posY, self.sizeY, 125, 175)