import pygame
import sqlite3
pygame.init()
ximage=pygame.image.load("x.png")
ximage=pygame.transform.scale(ximage,(80,80))
oimage=pygame.image.load("0.jpg")
oimage=pygame.transform.scale(oimage,(80,80))
xrect=ximage.get_rect()
orect=oimage.get_rect()
tictac=[[0,0,0],[0,0,0],[0,0,0]]
def get_cell(pos):
    x, y = pos
    return x // 80, y // 80
def draw_mark():
    screen.fill("black")
    pygame.draw.line(screen, "white", (0, 80), (240, 80))
    pygame.draw.line(screen, "white", (0, 160), (240, 160))
    pygame.draw.line(screen, "white", (80, 0), (80, 240))
    pygame.draw.line(screen, "white", (160, 0), (160, 240))
    for row in range(3):
        for col in range(3):
            if tictac[row][col] == "X":
                screen.blit(ximage, (col * 80, row * 80))
            elif tictac[row][col] == "O":
                screen.blit(oimage, (col * 80, row * 80))
def win(tictac):
    xrows=["X","X","X"]
    orows=["O","O","O"]
    if tictac[0]==xrows or tictac[0]==orows:
        return True
    elif tictac[1]==xrows or tictac[1]==orows:
        return True
    elif tictac[2]==xrows or tictac[2]==orows:
        return True
    return False
if __name__ == "__main__":
    clock = pygame.time.Clock()
    running = True
    screen=pygame.display.set_mode((240,240))
    screen.fill("black")
    pygame.draw.line(screen,"white",(0,80),(240,80))
    pygame.draw.line(screen,"white",(0,160),(240,160))
    pygame.draw.line(screen, "white", (80, 0), (80, 240))
    pygame.draw.line(screen, "white", (160, 0), (160, 240))
    xturn=True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type==pygame.MOUSEBUTTONUP:
                col, row = get_cell(event.pos)
                if tictac[row][col] == 0:
                    tictac[row][col] = "X" if xturn else "O"
                    xturn = not xturn
                    draw_mark()
                    if win(tictac):
                        screen.fill("black")
        pygame.display.flip()
        clock.tick(60)
pygame.quit()