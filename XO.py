import pygame
import sqlite3
import sysv_ipc

pygame.init()

ximage=pygame.image.load("x.png")
ximage=pygame.transform.scale(ximage,(80,80))
oimage=pygame.image.load("O.png")
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
    for i in range(3):
        if tictac[i][0] == tictac[i][1] == tictac[i][2] != 0:
            return True
        if tictac[0][i] == tictac[1][i] == tictac[2][i] != 0:
            return True
    if tictac[0][0] == tictac[1][1] == tictac[2][2] != 0:
        return True
    if tictac[0][2] == tictac[1][1] == tictac[2][0] != 0:
        return True

    return False
def draw(tictac):
    count=0
    for row in range(3):
        for col in range(3):
            if tictac[row][col]=="X" or tictac[row][col]=="O":
                count=count+1
    return count==9
def restart():
    screen.fill("black")
    pygame.draw.line(screen, "white", (0, 80), (240, 80))
    pygame.draw.line(screen, "white", (0, 160), (240, 160))
    pygame.draw.line(screen, "white", (80, 0), (80, 240))
    pygame.draw.line(screen, "white", (160, 0), (160, 240))
    pygame.draw.line(screen, "red", (0, 240), (300, 240))
    global tictac
    tictac = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    cursor.execute("SELECT player1, player2 FROM GameScore ORDER BY ROWID DESC LIMIT 1")
    scores = cursor.fetchone()

    player1score = scores[0] if scores else 0
    player2score = scores[1] if scores else 0

    label = font.render(f"Player 1: {player1score}|Player 2: {player2score}", 1, (255, 255, 0))
    screen.blit(label, (5, 280))

if __name__ == "__main__":
    clock = pygame.time.Clock()
    running = True
    screen=pygame.display.set_mode((240,320))
    screen.fill("black")
    pygame.draw.line(screen,"white",(0,80),(240,80))
    pygame.draw.line(screen,"white",(0,160),(240,160))
    pygame.draw.line(screen, "white", (80, 0), (80, 240))
    pygame.draw.line(screen, "white", (160, 0), (160, 240))
    pygame.draw.line(screen, "white", (0, 240), (300,240))
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
                    if win(tictac)==True and xturn==False:
                        score1=score1+1
                        cursor.execute("""INSERT INTO GameScore VALUES 
                                       (?,?)""",(score1,score2))
                        database.commit()
                        restart()
                    elif win(tictac)==True and xturn==True:
                        score2=score2+1
                        cursor.execute("""INSERT INTO GameScore VALUES
                                        (?,?)""",(score1,score2))
                        database.commit()
                        restart()
                    elif draw(tictac):
                        restart()
        pygame.display.flip()
        clock.tick(60)

cursor.close()
pygame.quit()