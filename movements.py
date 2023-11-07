import pygame
from pygame.locals import*

def changeVelocity(self, characterMoves, key, yBound):
    if key == characterMoves['up'] and self.posY >= yBound:
        self.velY = -10
        jumpSound = pygame.mixer.Sound("sounds/jump.mp3")
        jumpSound.play()
    if key == characterMoves['down'] and not self.crouch:
        self.velY = 10
        self.crouch = True
        crouchSound = pygame.mixer.Sound("sounds/crouch.mp3")
        crouchSound.play()
    if key == characterMoves['left']:
        self.velX = -10
    if key == characterMoves['right']:
        self.velX = 10

def stopVelocity(self, characterMoves, key):
    if key == characterMoves['left']:
        self.velX = 0
    if key == characterMoves['right']:
        self.velX = 0
    if key == characterMoves['down']:
        self.velY -= 10
        self.crouch = False

def changeCharacterPosition(self, stageBound, other, screenWidth, screenHeight):
    # change sprite
    if self.hold > 0:
        self.hold -= 1
        if self.hold == 0:
            self.posX += self.xAdjust
            self.xAdjust = 0
            self.block = False
            self.kick = False
    else:
        if self.forward:
            if self.velX < 0 or other.posX > self.posX + self.surf.get_width():
                if self.posX > 20 or self.velX > 0:
                    self.posX += self.velX
        else:
            if self.velX > 0 or other.posX < self.posX - self.surf.get_width():
                if self.posX < screenWidth - self.sizeX or self.velX < 0:
                    self.posX += self.velX
        
        if self.velY < 0:
            self.posY += self.velY
        
        if self.posY >= stageBound:
            self.posY = stageBound

        if self.posY == stageBound and self.crouch:
            self.posY = 425
            self.changeSprite(f"{self.name}/{self.name}_crouch.png", self.posY, self.sizeY, 125, 125)
        elif self.posY < stageBound:
            self.changeSprite(f"{self.name}/{self.name}_midair.png", self.posY, self.sizeY, 115, 175)
        else:
            self.changeSprite(f"{self.name}/{self.name}_default.png", self.posY, self.sizeY, 125, 175)
    
    if (self.posY < 425 and self.crouch) or (self.posY < 375 and not self.crouch):
        self.posY += self.velY
        self.velY += 0.5
    
    if self.posY >= 425 and self.crouch or self.kick:
        self.posY = 425
    elif self.posY >= 375:
        self.posY = 375
    
    if self.hp <= 0:
        self.posY = 475