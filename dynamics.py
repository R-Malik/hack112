import pygame
import math

def checkPunch(leftX1, rightX1, leftX2, rightX2):
    print(leftX1, leftX2, rightX1, rightX2)
    if abs(leftX1 - leftX2) > 100 or abs(rightX1 - rightX2) > 100:
        return True
    else:
        return False

def checkKick(leftY1, rightY1, leftY2, rightY2):
    if abs(leftY1 - leftY2) < 50 or abs(rightY1 - rightY2) < 50:
        return True
    else:
        return False

def checkLean(nose, hip1, hip2):
    difX = nose[0] - (hip1[0] + hip2[0]) / 2
    difY = nose[1] - (hip1[1] + hip2[1]) / 2
    rads = math.atan(difY / difX)
    if abs(rads) * 180 / math.pi < 60 and rads > 0:
        return 1
    if abs(rads) * 180 / math.pi < 75 and rads < 0:
        return -1
    return 0



# def changeVelocity(self, characterMoves, lean, yBound):
#     if jump and self.posY >= yBound:
#         self.velY = -10
#         jumpSound = pygame.mixer.Sound("sounds/jump.mp3")
#         jumpSound.play()
#     if crouch:
#         self.velY = 10
#         self.crouch = True
#         crouchSound = pygame.mixer.Sound("sounds/crouch.mp3")
#         crouchSound.play()
#     if leanLeft:
#         self.velX = -10
#     if leanRight:
#         self.velX = 10
#     if notLeaning:
#         self.velX = 0
#     if uncrouch:
#         self.velY -= 10
#         self.crouch = False

# def changeCharacterPosition(self, stageBound, other, screenWidth, screenHeight):
#     # change sprite
#     if self.hold > 0:
#         self.hold -= 1
#         if self.hold == 0:
#             self.posX += self.xAdjust
#             self.xAdjust = 0
#             self.block = False
#     else:
#         if self.forward:
#             if self.velX < 0 or other.posX > self.posX + self.surf.get_width():
#                 if self.posX > 20 or self.velX > 0:
#                     self.posX += self.velX
#         else:
#             if self.velX > 0 or other.posX < self.posX - self.surf.get_width():
#                 if self.posX < screenWidth - self.sizeX or self.velX < 0:
#                     self.posX += self.velX
#         if self.velY < 0:
#             self.posY += self.velY
#         if self.posY < stageBound:
#             self.posY += self.velY
#             self.velY += 0.5

#         if self.posY >= stageBound:
#             self.posY = stageBound
            
#         if self.posY == stageBound and self.crouch:
#             self.posY = 380
#             self.changeSprite(f"{self.name}/{self.name}_crouch.png", self.posY, self.sizeY, 125, 125)
#         elif self.posY < stageBound:
#             self.changeSprite(f"{self.name}/{self.name}_midair.png", self.posY, self.sizeY, 125, 175)
#         else:
#             self.changeSprite(f"{self.name}/{self.name}_default.png", self.posY, self.sizeY, 125, 175)
        