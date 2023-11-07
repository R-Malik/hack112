import pygame
from pygame.locals import*
from characters import*
from movements import*
from attacks import*
from vision import*
from dynamics import*

pygame.init()

clock = pygame.time.Clock()
running = True
knockout = False
vision = False

screenWidth, screenHeight = 1200, 675
screen = pygame.display.set_mode((screenWidth, screenHeight))
background = pygame.image.load("background.jpg").convert()

stageWidth, stageHeight = screenWidth, 125
stage = pygame.Surface((stageWidth, stageHeight), pygame.SRCALPHA, 32)
stage = stage.convert_alpha()

themeSound = pygame.mixer.Sound("sounds/theme.mp3")
themeSound.play(loops=-1)

character1 = makeCharacter("ryu", 400, 100, forward=True)
character2 = makeCharacter("ken", 800, 100, forward=False)

characterMoves1 = {'up': K_w, 'down': K_s, 'left': K_a, 'right': K_d,
                   'block': K_e, 'punch': K_r, 'kick': K_t}
characterMoves2 = {'up': K_UP, 'down': K_DOWN, 'left': K_LEFT, 'right': K_RIGHT,
                   'block': K_m, 'punch': K_COMMA, 'kick': K_PERIOD}

def startGame():
    titleFont = pygame.font.Font('font.ttf', 90)
    startFont = pygame.font.Font('font.ttf', 60)
    titleText = titleFont.render('FARNAMS FIGHT OFF', True, 'red')
    startText = startFont.render('PRESS SPACE TO START', True, 'gold')
    startText2 = startFont.render('PRESS V TO START WITH VISION', True, 'gold')
    
    textRect1 = titleText.get_rect()
    textRect2 = startText.get_rect()
    textRect3 = startText2.get_rect()
    textRect1.center = (600, 300)
    textRect2.center = (600, 450)
    textRect3.center = (600, 550)
    screen.blit(titleText, textRect1)
    screen.blit(startText, textRect2)
    screen.blit(startText2, textRect3)
    pygame.display.flip()
    startScreen = True
    global vision
    while startScreen:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    vision = False
                    startScreen = False
                elif event.key == K_v:
                    vision = True
                    startScreen = False
    startSound = pygame.mixer.Sound("sounds/start.mp3")
    startSound.play()

def victory(character):
    victoryFont = pygame.font.Font('font.ttf', 80)
    restartFont = pygame.font.Font('font.ttf', 30)
    victoryText = victoryFont.render(f'{character} WINS', True, 'lightblue' if character == "PAT" else 'orange')
    restartText = restartFont.render('PRESS SPACE TO RESTART, PRESS V FOR VISION', True, 'white')
    victoryTextRect = victoryText.get_rect()
    restartTextRect = restartText.get_rect()
    victoryTextRect.center = (600, 200)
    restartTextRect.center = (600, 300)
    screen.blit(victoryText, victoryTextRect)
    screen.blit(restartText, restartTextRect)
    pygame.display.flip()
    victoryScreen = True
    while victoryScreen:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    victoryScreen = False
                    restart(visionMode=False)
                if event.key == K_v:
                    victoryScreen = False
                    restart(visionMode=True)

def restart(visionMode):
    startSound = pygame.mixer.Sound("sounds/start.mp3")
    startSound.play()
    global character1
    global character2
    global knockout
    character1 = makeCharacter("ryu", 400, 100, forward=True)
    character2 = makeCharacter("ken", 800, 100, forward=False)
    knockout = False
    global themeSound
    themeSound = pygame.mixer.Sound("sounds/theme.mp3")
    themeSound.play(loops=-1)
    global vision
    vision = visionMode

startGame()
while running:
    clock.tick(60)

    yBound1 = screenHeight-stageHeight-character1.surf.get_height()
    yBound2 = screenHeight-stageHeight-character2.surf.get_height()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            changeVelocity(character1, characterMoves1, event.key, yBound1)
            changeVelocity(character2, characterMoves2, event.key, yBound2)
            attack(character1, characterMoves1, character2, event.key, screenWidth)
            attack(character2, characterMoves2, character1, event.key, screenWidth)
        elif event.type == KEYUP:
            stopVelocity(character1, characterMoves1, event.key)
            stopVelocity(character2, characterMoves2, event.key)
    if vision:
        bodyPoints = displayVideo(screen)
        if bodyPoints.get("nose", (0,0))[1] < 45:
            changeVelocity(character1, characterMoves1, characterMoves1["up"], yBound1)
        elif checkPunch(bodyPoints.get("left_wrist", (0,0))[0], bodyPoints.get("right_wrist", (0,0))[0], 
                bodyPoints.get("left_shoulder", (0,0))[0], bodyPoints.get("right_shoulder", (0,0))[0]):
            attack(character1, characterMoves1, character2, characterMoves1["punch"], screenWidth)

        if bodyPoints.get("nose", (0,0))[1] > 100:
            changeVelocity(character1, characterMoves1, characterMoves1["down"], yBound1)
        elif character1.crouch:
            stopVelocity(character1, characterMoves1, characterMoves1["down"])
        
        lean = checkLean(bodyPoints.get("nose", (0, 0)), bodyPoints.get("left_hip", (0, 0)),
                        bodyPoints.get("right_hip", (0, 0)))
        if lean == 1:
            changeVelocity(character1, characterMoves1, characterMoves1["right"], yBound1)
        elif lean == -1:
            changeVelocity(character1, characterMoves1, characterMoves1["left"], yBound1)
        else:
            stopVelocity(character1, characterMoves1, characterMoves1["left"])

    if not knockout:
        if character1.hp <= 0:
            character1.posX -= 60
            koSound = pygame.mixer.Sound("sounds/death.mp3")
            koSound.play()
            character1.changeSprite("ryu/ryu_ko.png", character2.posY, character2.sizeY, 225, 75)
            character1.posY -= 100
            knockout = True
            themeSound.fadeout(1000)
            victorySound = pygame.mixer.Sound("sounds/victory.mp3")
            victorySound.set_volume(200)
            victorySound.play()
        if character2.hp <= 0:
            character2.posX += 50
            koSound = pygame.mixer.Sound("sounds/death.mp3")
            koSound.play()
            character2.posY -= 100
            character2.changeSprite("ken/ken_ko.png", character2.posY, character2.sizeY, 225, 75)
            knockout = True
            themeSound.fadeout(1000)
            victorySound = pygame.mixer.Sound("sounds/victory.mp3")
            victorySound.set_volume(200)
            victorySound.play()

        changeCharacterPosition(character1, yBound1, character2, screenWidth, screenHeight)
        changeCharacterPosition(character2, yBound2, character1, screenWidth, screenHeight)

        hpBar1 = [50, 40, 500, 20]
        hpBarOutline1 = Rect(hpBar1[0] - 4, hpBar1[1] - 4, hpBar1[2] + 8, hpBar1[3] + 8)
        hpBarHealth1 = Rect(550 - character1.hp * 5, hpBar1[1], character1.hp * 5, hpBar1[3])
        hpBar2 = [650, 40, 500, 20]
        hpBarOutline2 = Rect(hpBar2[0] - 4, hpBar2[1] - 4, hpBar2[2] + 8, hpBar2[3] + 8)
        hpBarHealth2 = Rect(hpBar2[0], hpBar2[1], character2.hp * 5, hpBar2[3])
        middleBoxOutline = Rect(550, 24, 100, 52)
        middleBoxFill = Rect(550, 28, 100, 44)

        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, "white", hpBarOutline1, 4)
        pygame.draw.rect(screen, "red", hpBarHealth1)
        pygame.draw.rect(screen, "white", hpBarOutline2, 4)
        pygame.draw.rect(screen, "red", hpBarHealth2)
        pygame.draw.rect(screen, "black", middleBoxFill)
        pygame.draw.rect(screen, "white", middleBoxOutline, 4)

        font = pygame.font.Font('font.ttf', 60)
        text = font.render('KO', False, 'red')
        textRect = text.get_rect()
        textRect.center = (600, 50)

        font = pygame.font.Font('font.ttf', 30)
        character1Text = font.render('PAT', False, 'white')
        character1Rect = character1Text.get_rect()
        character1Rect.center = (character1.posX, character1.posY-25)
        character2Text = font.render('MIKE', False, 'white')
        character2Rect = character2Text.get_rect()
        character2Rect.center = (character2.posX + 140, character2.posY-25)
            
        screen.blit(text, textRect)
        screen.blit(character1Text, character1Rect)
        screen.blit(character2Text, character2Rect)
        screen.blit(stage, (0, screenHeight-stageHeight))
        screen.blit(character1.surf, (character1.posX, character1.posY))
        screen.blit(character2.surf, (character2.posX, character2.posY))
        
        if character1.hp <= 0:
            victory('MIKE')
        elif character2.hp <= 0:
            victory('PAT')
            
    pygame.display.flip()

pygame.quit()