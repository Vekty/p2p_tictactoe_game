import pygame
import sqlite3
pygame.init()

ximage=pygame.image.load("x.png")
ximage=pygame.transform.scale(ximage,(80,80))
oimage=pygame.image.load("0.jpg")
oimage=pygame.transform.scale(oimage,(80,80))
xrect=ximage.get_rect()
orect=oimage.get_rect()

font = pygame.font.SysFont("monospace", 15)

tictac=[[0,0,0],[0,0,0],[0,0,0]]

database=sqlite3.connect("database.db")
cursor=database.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS GameScore(scoreplayer1,scoreplayer2)")


def get_cell(pos):
    x, y = pos
    return x // 80, y // 80

def draw_mark():
    for row in range(3):
        for col in range(3):
            if tictac[row][col] == "X":
                screen.blit(ximage, (col * 80, row * 80))
            elif tictac[row][col] == "O":
                screen.blit(oimage, (col * 80, row * 80))

def win(tictac):
    if tictac[0][0]==tictac[0][1] and tictac[0][0]==tictac[0][2] and tictac[0][0]!=0:
        return True
    if tictac[1][0]==tictac[1][1] and tictac[1][0]==tictac[1][2] and tictac[1][0]!=0:
        return True
    if tictac[2][0]==tictac[2][1] and tictac[2][0]==tictac[2][1] and tictac[2][0]!=0:
        return True
    if tictac[0][0]==tictac[1][0] and tictac[0][0]==tictac[2][0] and tictac[0][0]!=0:
        return True
    if tictac[0][1] == tictac[1][1] and tictac[0][1] == tictac[2][1] and tictac[0][1]!=0:
        return True
    if tictac[0][2] == tictac[1][2] and tictac[0][2] == tictac[2][2] and tictac[0][2]!=0:
        return True
    if tictac[1][1] == tictac[2][2] and tictac[0][0]==tictac[1][1] and tictac[1][1]!=0:
        return True
    if tictac[0][2]==tictac[1][1] and tictac[0][2]==tictac[2][0] and tictac[0][2]!=0:
        return True
    return False
def restart():
    screen.fill("black")
    pygame.draw.line(screen, "white", (0, 80), (240, 80))
    pygame.draw.line(screen, "white", (0, 160), (240, 160))
    pygame.draw.line(screen, "white", (80, 0), (80, 240))
    pygame.draw.line(screen, "white", (160, 0), (160, 240))
    pygame.draw.line(screen, "red", (0, 240), (300, 240))
    global tictac
    tictac = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
if __name__ == "__main__":
    clock = pygame.time.Clock()
    running = True
    screen=pygame.display.set_mode((240,320))
    screen.fill("black")
    pygame.draw.line(screen,"white",(0,80),(240,80))
    pygame.draw.line(screen,"white",(0,160),(240,160))
    pygame.draw.line(screen, "white", (80, 0), (80, 240))
    pygame.draw.line(screen, "white", (160, 0), (160, 240))
    pygame.draw.line(screen, "red", (0, 240), (300,240))
    xturn=True
    score1=0
    score2=0

    cursor.execute("""DELETE FROM GameScore""")

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
                    if win(tictac) and xturn==False:
                        score1=score1+1
                        cursor.execute("""INSERT INTO GameScore VALUES 
                                       (?,?)""",(score1,score2))
                        database.commit()
                        restart()
                    elif win(tictac) and xturn==True:
                        score2=score2+1
                        cursor.execute("""INSERT INTO GameScore VALUES
                                        (?,?)""",(score1,score2))
                        database.commit()
                        restart()
        pygame.display.flip()
        clock.tick(60)

result=cursor.execute("SELECT player1,player2 FROM GameScore")
print(result.fetchall())
cursor.close()
pygame.quit()