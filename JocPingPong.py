import pygame
import sys
from tkinter import *
import sqlite3
pygame.init()
LATIME, INALTIME = 700, 500
WIN = pygame.display.set_mode((LATIME, INALTIME))
pygame.display.set_caption("PingPong")

FPS = 60

ALB = (255,255,255)
NEGRU = (0, 0, 0)
ALBASTRU  = (0, 0, 255)
VERDE = (48, 25, 52)
LATIME_PALETA, INALTIME_PALETA = 20, 100
RAZA_MINGE = 7

FONT_SCOR = pygame.font.SysFont("comicsans", 30)
SCOR_FINAL = 3

baza = Tk()
baza.title("PingPong")
width = 400
height = 280
screen_width = baza.winfo_screenwidth()
screen_height = baza.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
baza.geometry("%dx%d+%d+%d" % (width, height, x, y))
baza.resizable(0, 0)

USERNAME = StringVar()
PASSWORD = StringVar()

Top = Frame(baza, bd=2,  relief=RIDGE)
Top.pack(side=TOP, fill=X)
Form = Frame(baza, height=200)
Form.pack(side=TOP, pady=20)
 
lbl_title = Label(Top, text = "Autentificare Joc", font=('arial', 15))
lbl_title.pack(fill=X)
lbl_username = Label(Form, text = "Username:", font=('arial', 14), bd=15)
lbl_username.grid(row=0, sticky="e")
lbl_password = Label(Form, text = "Password:", font=('arial', 14), bd=15)
lbl_password.grid(row=1, sticky="e")
lbl_text = Label(Form)
lbl_text.grid(row=2, columnspan=2)
 
username = Entry(Form, textvariable=USERNAME, font=(14))
username.grid(row=0, column=1)
password = Entry(Form, textvariable=PASSWORD, show="*", font=(14))
password.grid(row=1, column=1)

def logare(event=None):
    Baza_date()
    if USERNAME.get() == "" or PASSWORD.get() == "":
        lbl_text.config(text="Completeaza campurile de mai sus!", fg="red")
    else:
        cursor.execute("SELECT * FROM member WHERE username = ? AND password = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            fereastra_home()
            USERNAME.set("")
            PASSWORD.set("")
            lbl_text.config(text="")
        else:
            lbl_text.config(text="Invalid username or password", fg="red")
            USERNAME.set("")
            PASSWORD.set("")   
    cursor.close()
    conn.close()
 
def fereastra_home():
    global Home
    baza.withdraw()
    Home = Toplevel()
    Home.title("PingPong")
    width = 600
    height = 500
    screen_width = baza.winfo_screenwidth()
    screen_height = baza.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    baza.resizable(0, 0)
    Home.geometry("%dx%d+%d+%d" % (width, height, x, y))
    main()
    sys.exit()
 
def Back():
    Home.destroy()
    baza.deiconify()
 
btn_login = Button(Form, text="Logare", width=45, command=logare)
btn_login.grid(pady=25, row=3, columnspan=2)
btn_login.bind('<Return>', logare)
def Baza_date():
    global conn, cursor
    conn = sqlite3.connect("pythontut.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS member (mem_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, username TEXT, password TEXT)")       
    cursor.execute("SELECT * FROM member WHERE username = 'admin' AND password = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO member (username, password) VALUES('admin', 'admin')")
        conn.commit()
    
'''def vizualizare_db():
    Baza_date() 
    cursor.execute("SELECT * FROM member")
    records = cursor.fetchall()

    print("Conținut Database:")
    
    for record in records:
        print(record)

    cursor.close()
    conn.close()'''

def adauga_membru(username, password):
    conn = sqlite3.connect("pythontut.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO member (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()
class Paleta:
    CULOARE = ALB
    VIT = 4

    def __init__(self, x, y, latime, inaltime):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.latime = latime
        self.inaltime = inaltime
    def desen (self, win):
        pygame.draw.rect(win, self.CULOARE, (self.x, self.y, self.latime, self.inaltime))
    
    def move(self, up=True):
        if up:
            self.y -= self.VIT
        else:
            self.y += self.VIT

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y



class Minge:
    MAX_VIT = 5
    CULOARE = ALB
    def __init__(self, x, y, raza):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.raza = raza
        self.x_vel = self.MAX_VIT
        self.y_vel = 0
    def desen(self, win):
        pygame.draw.circle(win, self.CULOARE, (self.x, self.y), self.raza)
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


def desen(win, palete, minge, scor_stanga, scor_dreapta, cul):
    background_color, paddle_color, ball_color, line_color = get_color(cul)

    win.fill(background_color)

    scor_stanga_text = FONT_SCOR.render(f"{scor_stanga}", 1, ALB)
    scor_dreapta_text = FONT_SCOR.render(f"{scor_dreapta}", 1, ALB)
    win.blit(scor_stanga_text, (LATIME//4 - scor_stanga_text.get_width()//2, 20))
    win.blit(scor_dreapta_text, (LATIME * (3/4) - scor_dreapta_text.get_width()//2, 20))

    for paleta in palete:
        paleta.CULOARE = paddle_color
        paleta.desen(win)

    for i in range(10, INALTIME, INALTIME//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, line_color, (LATIME//2 - 5, i, 10, INALTIME//20))

    minge.CULOARE = ball_color
    minge.desen(win)
    pygame.display.update()


def coliziune(minge, paleta_stanga, paleta_dreapta):
    if minge.y + minge.raza >= INALTIME:
        minge.y_vel *= -1
    elif minge.y - minge.raza <= 0:
        minge.y_vel *= -1
    
    if minge.x_vel < 0:
        if minge.y >= paleta_stanga.y and minge.y <= paleta_stanga.y + paleta_stanga.inaltime:
            if minge.x - minge.raza <= paleta_stanga.x + paleta_stanga.latime:
                minge.x_vel *= -1

                mijloc_y = paleta_stanga.y + paleta_stanga.inaltime / 2
                diferenta_in_y = mijloc_y - minge.y
                fact_reduc = (paleta_stanga.inaltime / 2) / minge.MAX_VIT
                y_vel = diferenta_in_y / fact_reduc
                minge.y_vel = -1 * y_vel


    else: 
        if minge.y >= paleta_dreapta.y and minge.y <= paleta_dreapta.y + paleta_dreapta.inaltime:
            if minge.x + minge.raza >= paleta_dreapta.x:
                minge.x_vel *= -1

                mijloc_y = paleta_dreapta.y + paleta_dreapta.inaltime / 2
                diferenta_in_y = mijloc_y - minge.y
                fact_reduc = (paleta_dreapta.inaltime / 2) / minge.MAX_VIT
                y_vel = diferenta_in_y / fact_reduc
                minge.y_vel = -1 * y_vel



def miscare_paleta(keys, paleta_stanga, paleta_dreapta):
    if keys[pygame.K_w] and paleta_stanga.y - paleta_stanga.VIT >=0:
        paleta_stanga.move(up=True)
    if keys[pygame.K_s] and paleta_stanga.y + paleta_stanga.VIT + paleta_stanga.inaltime <= INALTIME:
        paleta_stanga.move(up=False)

    if keys[pygame.K_UP] and paleta_dreapta.y - paleta_dreapta.VIT >=0:
        paleta_dreapta.move(up=True)
    if keys[pygame.K_DOWN] and paleta_dreapta.y + paleta_dreapta.VIT + paleta_dreapta.inaltime <= INALTIME:
        paleta_dreapta.move(up=False)


def select_difficulty():
    run = True
    clock = pygame.time.Clock()
    font_large = pygame.font.SysFont("arial.ttf", 40)
    font_small = pygame.font.SysFont("arial.ttf", 30)
    difficulty_options = ["Easy", "Medium", "Hard", "Quit"]
    selected_difficulty = None

    while run:
        clock.tick(FPS)
        WIN.fill(NEGRU)

        message = font_large.render("Selectati dificultatea folosind sagetile", 1, ALB)
        WIN.blit(message, (LATIME // 2 - message.get_width() // 2, INALTIME // 8))

        for i, option in enumerate(difficulty_options):
            text = font_small.render(option, 1, ALBASTRU if selected_difficulty == option else ALB)
            WIN.blit(text, (LATIME // 2 - text.get_width() // 2, INALTIME // 2 - len(difficulty_options) * text.get_height() // 2 + i * 60))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and selected_difficulty is not None:
                    if selected_difficulty == "Quit":
                        pygame.quit()
                        sys.exit()
                    else:
                        run = False
                elif event.key == pygame.K_UP:
                    selected_difficulty = difficulty_options[0] if selected_difficulty is None else difficulty_options[(difficulty_options.index(selected_difficulty) - 1) % len(difficulty_options)]
                elif event.key == pygame.K_DOWN:
                    selected_difficulty = difficulty_options[0] if selected_difficulty is None else difficulty_options[(difficulty_options.index(selected_difficulty) + 1) % len(difficulty_options)]

    return selected_difficulty

def get_color(cul):
    if cul == "Pachetul 1":
        return NEGRU, ALB, ALB, ALBASTRU
    elif cul == "Pachetul 2":
        return (169, 169, 169), (0, 128, 0), (0, 128, 0), (0, 128, 0)
    elif cul == "Pachetul 3":
        return (255, 182, 193), (255, 255, 0), (255, 255, 0), (255, 255, 0)
    else:
        return NEGRU, ALB, ALB, ALBASTRU
    
def pagina_start():
    run = True
    clock = pygame.time.Clock()
    font_large = pygame.font.SysFont("arial.ttf", 60)
    font_small = pygame.font.SysFont("arial.ttf", 40)

    while run:
        clock.tick(FPS)
        WIN.fill(VERDE)

        title = font_large.render("Ping-Pong", 1, ALB)
        WIN.blit(title, (LATIME // 2 - title.get_width() // 2, INALTIME // 4))

        start_text = font_small.render("Press ENTER to start", 1, ALBASTRU)
        exit_text = font_small.render("Press ESC to exit", 1, ALBASTRU)
        WIN.blit(start_text, (LATIME // 2 - start_text.get_width() // 2, INALTIME // 2))
        WIN.blit(exit_text, (LATIME // 2 - exit_text.get_width() // 2, INALTIME // 2 + 40))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def select_culoare():
    run = True
    clock = pygame.time.Clock()
    font_large = pygame.font.SysFont("arial.ttf", 40)
    font_small = pygame.font.SysFont("arial.ttf", 30)
    color_options = ["Pachetul 1", "Pachetul 2", "Pachetul 3", "Back"]
    culoare_selectata = None

    while run:
        clock.tick(FPS)
        WIN.fill(NEGRU)

        message = font_large.render("Selectati un pachet de culori folosind sagetile", 1, ALB)
        WIN.blit(message, (LATIME // 2 - message.get_width() // 2, INALTIME // 8))

        for i, option in enumerate(color_options):
            text = font_small.render(option, 1, ALBASTRU if culoare_selectata == option else ALB)
            WIN.blit(text, (LATIME // 2 - text.get_width() // 2, INALTIME // 2 - len(color_options) * text.get_height() // 2 + i * 60))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run = False
                elif event.key == pygame.K_UP:
                    culoare_selectata = color_options[0] if culoare_selectata is None else color_options[(color_options.index(culoare_selectata) - 1) % len(color_options)]
                elif event.key == pygame.K_DOWN:
                    culoare_selectata = color_options[0] if culoare_selectata is None else color_options[(color_options.index(culoare_selectata) + 1) % len(color_options)]

    return culoare_selectata
    
def main():
    pagina_start()

    while True:
        cul = select_culoare()
        if cul == "Back":
            pagina_start()
        else:
            break

    difficulty = select_difficulty()
    if difficulty == "Easy":
        Minge.MAX_VIT = 5
    elif difficulty == "Medium":
        Minge.MAX_VIT = 7
    elif difficulty == "Hard":
        Minge.MAX_VIT = 10
    run = True
    clock = pygame.time.Clock()

    paleta_stanga = Paleta(10, INALTIME//2 - INALTIME_PALETA//2, LATIME_PALETA, INALTIME_PALETA)
    paleta_dreapta = Paleta(LATIME - 10 - LATIME_PALETA, INALTIME//2 - INALTIME_PALETA//2, LATIME_PALETA, INALTIME_PALETA)
    minge = Minge(LATIME//2, INALTIME//2, RAZA_MINGE)

    scor_stanga = 0
    scor_dreapta = 0
    while run:
        clock.tick(FPS)
        desen(WIN, [paleta_stanga, paleta_dreapta], minge,scor_stanga, scor_dreapta, cul)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
   
        keys = pygame.key.get_pressed()
        miscare_paleta(keys, paleta_stanga, paleta_dreapta)

        minge.move()
        coliziune(minge, paleta_stanga, paleta_dreapta)

        if minge.x < 0:
            scor_dreapta += 1
            minge.reset()
        elif minge.x > LATIME:
            scor_stanga += 1
            minge.reset()


        w = False
        if scor_stanga > SCOR_FINAL:
           w = True
           text = "Stanga a castigat!"

        elif scor_dreapta > SCOR_FINAL:
            w = True
            text = "Dreapta a castigat!"
        if w:
            text1 = FONT_SCOR.render(text, 1, ALB)
            WIN.blit(text1, (LATIME//2 - text1.get_width()//2, INALTIME//2 - text1.get_height()//2))
            pygame.display.update()
            pygame.time.delay(3000)
            minge.reset()
            paleta_stanga.reset()
            paleta_dreapta.reset()
            scor_stanga = 0
            scor_dreapta = 0
    pygame.quit()


if __name__ == '__main__':
    #adauga_membru("user1","parola1")
    #vizualizare_db()
    baza.mainloop()
