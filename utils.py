import pygame, pygame.freetype

def Textify(words, size, x, y, win):
    bitFont = pygame.freetype.Font("assets/8bitOperatorPlus8-Bold.ttf", size)
    text, rect = bitFont.render(str(words), (0, 0, 0))
    x -= (rect.width)/2
    y -= (rect.height)/2
    win.blit(text, (round(x), round(y)))