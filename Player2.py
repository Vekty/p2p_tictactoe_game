import pygame
import sqlite3
import sysv_ipc
import time


class IPC:
    def __init__(self):
        connected = False
        while not connected:
            try:
                self.messagequeue = sysv_ipc.MessageQueue(12345)
                connected = True
                print("Connected to message queue successfully")
            except sysv_ipc.ExistentialError:
                print("Waiting for Player 1 to create the message queue...")
                time.sleep(2)

    def send(self, message):
        try:
            print(f"Player 2 sending: {message}")
            self.messagequeue.send(message.encode())
        except Exception as e:
            print(f"Error sending message: {e}")

    def receive(self):
        try:
            # Use blocking receive with proper exception handling
            message, _ = self.messagequeue.receive(block=True)
            decoded = message.decode()
            print(f"Player 2 received: {decoded}")
            return decoded
        except Exception as e:
            print(f"Error receiving message: {e}")
            return None

    def remove(self):
        try:
            self.messagequeue.remove()
            print("Message queue removed")
        except Exception as e:
            print(f"Error removing message queue: {e}")

    def flush_messages(self):
        try:
            while True:
                self.messagequeue.receive(block=False)  # Non-blocking receive
        except sysv_ipc.BusyError:
            pass  # No more messages in the queue

pygame.init()

# Load images
ximage = pygame.image.load("x.png")
ximage = pygame.transform.scale(ximage, (80, 80))
oimage = pygame.image.load("O.png")
oimage = pygame.transform.scale(oimage, (80, 80))
xrect = ximage.get_rect()
orect = oimage.get_rect()

font = pygame.font.SysFont("monospace", 15)

tictac = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

database = sqlite3.connect("database.db")
cursor = database.cursor()


def get_cell(pos):  # snap to grid
    x, y = pos
    return x // 80, y // 80


def draw_mark():  # draw the XO table
    for row in range(3):
        for col in range(3):
            if tictac[row][col] == "X":
                screen.blit(ximage, (col * 80, row * 80))
            elif tictac[row][col] == "O":
                screen.blit(oimage, (col * 80, row * 80))


def win(tictac):  # win condition
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


def draw(tictac):  # draw condition
    count = 0
    for row in range(3):
        for col in range(3):
            if tictac[row][col] == "X" or tictac[row][col] == "O":
                count = count + 1
    return count == 9


def restart():  # restart the game in case of win or draw
    global tictac
    tictac = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    screen.fill("black")
    pygame.draw.line(screen, "white", (0, 80), (240, 80))
    pygame.draw.line(screen, "white", (0, 160), (240, 160))
    pygame.draw.line(screen, "white", (80, 0), (80, 240))
    pygame.draw.line(screen, "white", (160, 0), (160, 240))
    pygame.draw.line(screen, "red", (0, 240), (300, 240))

    cursor.execute("SELECT player1, player2 FROM GameScore ORDER BY ROWID DESC LIMIT 1")
    scores = cursor.fetchone()

    player1score = scores[0] if scores else 0
    player2score = scores[1] if scores else 0

    label = font.render(f"Player 1: {player1score}|Player 2: {player2score}", 1, (255, 255, 0))
    screen.blit(label, (5, 280))


    waiting_label = font.render("Waiting for Player 1 (X)", 1, (255, 0, 0))
    screen.blit(waiting_label, (5, 260))

    global oturn
    oturn = False


def check_opponent_move():
    response = msg.receive()
    if response:

        if response == "RESTART":
            print("Received restart signal from Player 1")
            restart()
            return True


        move_data = response.split(',')
        if len(move_data) == 2:
            try:
                col, row = int(move_data[0]), int(move_data[1])
                if 0 <= row < 3 and 0 <= col < 3 and tictac[row][col] == 0:
                    tictac[row][col] = "X"
                    draw_mark()
                    if win(tictac):

                        pygame.display.flip()
                        time.sleep(0.5)
                        restart()
                    elif draw(tictac):

                        pygame.display.flip()
                        time.sleep(0.5)
                        restart()
                    else:
                        global oturn
                        oturn = True

                        pygame.draw.rect(screen, (0, 0, 0), (5, 260, 200, 20))
                        myturn_label = font.render("Your Turn (O)", 1, (0, 255, 0))
                        screen.blit(myturn_label, (5, 260))

                    return True
            except (ValueError, IndexError) as e:
                print(f"Error processing move: {e}")

    return False


if __name__ == "__main__":
    clock = pygame.time.Clock()
    running = True
    screen = pygame.display.set_mode((240, 320))
    screen.fill("black")
    pygame.display.set_caption("Tic-Tac-Toe - Player 2 (O)")
    pygame.draw.line(screen, "white", (0, 80), (240, 80))
    pygame.draw.line(screen, "white", (0, 160), (240, 160))
    pygame.draw.line(screen, "white", (80, 0), (80, 240))
    pygame.draw.line(screen, "white", (160, 0), (160, 240))
    pygame.draw.line(screen, "red", (0, 240), (300, 240))

    waiting_label = font.render("Waiting for Player 1 (X)", 1, (255, 0, 0))
    screen.blit(waiting_label, (5, 260))

    oturn = False
    score1 = 0
    score2 = 0


    msg = IPC()
    print("Player 2 ready. Waiting for Player 1's move...")


    cursor.execute("SELECT player1, player2 FROM GameScore ORDER BY ROWID DESC LIMIT 1")
    scores = cursor.fetchone()

    player1score = scores[0] if scores else 0
    player2score = scores[1] if scores else 0

    label = font.render(f"Player 1: {player1score}|Player 2: {player2score}", 1, (255, 255, 0))
    screen.blit(label, (5, 280))

    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    msg.remove()
                if event.type == pygame.MOUSEBUTTONUP and oturn:
                    col, row = get_cell(event.pos)
                    if 0 <= row < 3 and 0 <= col < 3 and tictac[row][col] == 0:
                        tictac[row][col] = "O"
                        draw_mark()
                        pygame.display.flip()
                        if win(tictac):

                            score2 = score2 + 1


                            msg.send(f"{col},{row}")


                            pygame.display.flip()
                            time.sleep(0.5)
                            msg.flush_messages()
                            msg.send("RESTART")
                            print("Game restarted")
                            restart()
                        elif draw(tictac):

                            msg.send(f"{col},{row}")

                            pygame.display.flip()
                            time.sleep(0.5)
                            msg.flush_messages()
                            msg.send("RESTART")
                            print("Game restarted")
                            restart()
                        else:
                            msg.send(f"{col},{row}")
                            oturn = False

                            pygame.draw.rect(screen, (0, 0, 0), (5, 260, 200, 20))
                            waiting_label = font.render("Waiting for Player 1 (X)", 1, (255, 0, 0))
                            screen.blit(waiting_label, (5, 260))

            if not oturn:
                check_opponent_move()

            pygame.display.flip()
            clock.tick(60)
    except Exception as e:
        print(f"Game error: {e}")
    finally:

        cursor.close()
        database.close()
        pygame.quit()