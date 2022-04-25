
from multiprocessing.context import SpawnContext
from tkinter import *
from random import *
from time import sleep, time
from PIL import Image, ImageTk

# GUI
H = 500
B = 800
window = Tk()
window.title("Blaster")
c = Canvas(window, width=B, height = H, bg = "lightblue")
c.pack()

# draw spaceship
img = PhotoImage(file="spaceship.png")
sp = c.create_image(B/2, H/2, image=img)
SP_R = 45

# Spaceship moves
SP_GESCHW = 10
def sp_bewegen(event):
    x, y = c.coords(sp)
    if event.keysym == "Up":
        if y >= SP_GESCHW:
            c.move(sp, 0, -SP_GESCHW)
    elif event.keysym == "Down":
        if y <= H - SP_GESCHW:
            c.move(sp, 0, SP_GESCHW)
    elif event.keysym == "Left":
        if x >= SP_GESCHW:
            c.move(sp, -SP_GESCHW, 0)
    elif event.keysym == "Right":
        if x <= B - SP_GESCHW:
            c.move(sp, SP_GESCHW, 0)
c.bind_all("<Key>", sp_bewegen)

# Enemy erzeugen
enemy_img = PhotoImage(file="Enemy.png")
EN_R = 25
en_id = []
en_geschw = []
MAX_EN_GESCHW = 10
GAP = 100



def erzeuge_enemy():
    x = B + GAP
    y = randint(0, H)
    v = randint(1, MAX_EN_GESCHW)
    id_num = c.create_image(x, y, image = enemy_img)
    en_id.append(id_num)
    en_geschw.append(v)

    # Enemy moves
def move_enemy():
    for i in range(len(en_id)):
        c.move(en_id[i], -en_geschw[i], 0)

# HAUPTSCHLEIFE
#while True:
    #if randint(1, 10) == 1:
   #     erzeuge_enemy()
   # move_enemy()
    #window.update()
    #sleep(0.01)
    
    # delete enemies
def delete_enemy(i):
    c.delete(en_id[i])
    del en_id[i]
    del en_geschw[i]
    
    # delete enemies when out of bounce
def entferne_enemies():
    for i in range(len(en_id)-1, -1, -1):
        x, y = c.coords(en_id[i])
        if x < -GAP:
            delete_enemy(i)
            
# HAUPTSCHLEIFE
#while True:
 #   if randint(1, 1) == 1:
  #     erzeuge_enemy()
   #    move_enemy()
    #   entferne_enemies()
     #  window.update()
      # sleep(0.01)
      
# Entfernung zwischen Punkten
from math import sqrt
def abstand(sp, id_en):
    x1, y1 = c.coords(sp)
    x2, y2 = c.coords(id_en)
    a = sqrt((x2-x1)**2 + (y2-y1)**2)
    return a - 100                 


# Bubbles platzen lassen (wenn sie vom U-Boot getroffen werden)
def treffer():
    punkte = 0
    for i in range(len(en_id)-1, -1, -1):
        if abstand(sp, en_id[i]) < (SP_R + EN_R):
            punkte += (EN_R + en_geschw[i])
            delete_enemy(i)
    return punkte

# HAUPTSCHLEIFE
#score = 0
#hile True:
#    if randint(1, 10) == 1:
#       erzeuge_enemy()
#       move_enemy()
#       entferne_enemies()
#       score += treffer()
#       print (score)
#       window.update()
#       sleep(0.01)
       
# Zeit und Punkte anzeigen
c.create_text(50, 30, text = "ZEIT", fill="white")
c.create_text(150, 30, text = "PUNKTE", fill="white")
time_text = c.create_text(50, 50, fill="white")
score_text = c.create_text(150, 50, fill="white")
def zeige_punkte(score):
    c.itemconfig(score_text, text = str(score))
def zeige_zeit(time_left):
    c.itemconfig(time_text, text=str(time_left)) 

# HAUPTSCHLEIFE
score = 0
TIME_LIMIT = 30
ende = time() + TIME_LIMIT
while time() < ende:
    if randint(1, 10) == 1:
        erzeuge_enemy()
    move_enemy()
    entferne_enemies()
    score += treffer()
    zeige_punkte(score)
    zeige_zeit(int(ende-time()))
    window.update()
    sleep(0.01)

c.create_text(B/2, H/2, text = "GAME OVER", \
              fill = "white", font=("Helvetica", 30))
c.create_text(B/2, H/2 + 30, \
              text = "Punkte: " + str(score), fill = "white")    

window.mainloop()