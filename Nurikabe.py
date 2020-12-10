# coding: utf-8

import ctypes
import pygame
import time
import os
from pygame.locals import *

if os.name == "nt":
    ctypes.windll.shcore.SetProcessDpiAwareness(2) # Ignorer le zoom

WIDTH, HEIGHT = 1000, 900
SQUARE_DEFAULT = 60
WHITE, BLACK = (255,255,255), (0,0,0)
GRAY1, GRAY2, GRAY3 = (220,220,220), (190,190,190), (150,150,150)
BLUE, BEIGE, RED, PURPLE = (208,250,249), (255,244,223), (255,0,0), (255,0,255)

def load_grid(num):
    grille = []
    with open(f"Grilles/{num}.txt") as f:
        try:
            ligne_1 = f.readline().split()
            assert ligne_1[1].startswith("ligne")
            n = int(ligne_1[0])
            ligne_2 = f.readline().split()
            assert ligne_2[1].startswith("colonne")
            m = int(ligne_2[0])
        except:
            raise ValueError("Un fichier de grille valide doit renseigner le nombre de lignes et le nombre de colonnes dans les deux premières lignes du fichier, de la façon suivante :\n... lignes\n... colonnes\n...")
        for i in range(n):
            try:
                grille.append(f.readline().split())
                assert len(grille[-1]) == m
            except AssertionError:
                raise ValueError(f"Le nombre de colonnes ({m}) n'est pas respecté sur la ligne {i+1}")
        if f.readline():
            raise ValueError(f"Il y a plus de lignes que les {n} promises")
    return n, m, grille

def load_grids():
    erreur = ""
    if "Grilles" not in os.listdir():
        erreur += "Problème dans le dossier Nurikabe :\nIl n'y a pas de dossier Grilles pour contenir les grilles.\nLe dossier a peut-être été renommé, déplacé, ou supprimé.\nS'il est introuvable vous devrez réinstaller l'application.\n"
        raise FileNotFoundError(erreur)
    no_grid = True

    def cmp(i):
        if i.endswith(".txt"): i = i[:-4]
        t = i.split(" ")
        for i,elt in enumerate(t):
            if elt.isdigit():
                t[i] = "0"*max(0,9-len(elt))+elt
        return ''.join(t)

    for name in sorted(os.listdir("Grilles"), key=cmp):
        if name.endswith(".txt"):
            try:
                grilles[name[:-4]] = load_grid(name[:-4])
                no_grid = False
            except ValueError as e:
                erreur += f"Problème sur la grille {name[:-4]} :\n{e}\n"
        else:
            erreur += f"Problème dans le dossier Grilles :\nLe fichier {name} n'a pas pour extension .txt donc n'est pas considéré comme une grille.\n"
    if no_grid:
        erreur += "Problème dans le dossier Grilles :\nIl n'y a aucune grille.\n"
    if erreur:
        raise Exception(erreur)

def message_display(text, size, xc=WIDTH//2, yc=HEIGHT//2):
    lines = text.split("\n")
    y = yc - (len(lines)-1)*size//2
    font = pygame.font.SysFont("comicsansms",size)
    for line in lines:
        surface = font.render(line, True, BLACK)
        rectangle = surface.get_rect()
        rectangle.center = (xc, y)
        display.blit(surface, rectangle)
        y+=size

def bottom_message_display(text, size):
    pygame.draw.rect(display, WHITE, (0,HEIGHT-150, WIDTH,150))
    message_display(text, size, WIDTH//2, HEIGHT-75)

def show_rules():
    text = "Il y a une grille de carrés, dont certains contiennent un nombre. Le but est de déterminer pour chaque\ncarré s'il est rivière ou terre ferme. Les cases de rivière forment le nurikabe (courant en japonais) : elles\ndoivent toutes être contigües par un côté, ne doivent pas contenir de nombre et ne doivent contenir aucun\nbloc 2x2 ou plus grand (de tels blocs sont appelés bassins). Les cases de terre ferme forment les îles :\nchaque nombre doit faire partie d'un îlot d'autant de cases de terre ferme. Chaque case de terre\nferme ne doit appartenir qu'à une seule île et chaque île ne contient qu'un nombre."
    bottom_message_display(text, 20)

def show_help():
    text = "Cliquez sur un des boutons à gauche pour charger une nouvelle \ngrille de nurikabe. Faites un clic droit sur un carré de la grille pour\nle noter comme terre ou un clic gauche pour le noter comme rivière.\nLa molette permet de passer en mode gommage."
    bottom_message_display(text, 30)

def show_new():
    text = "Vous pouvez aussi ajouter d'autres grilles grâce à grille_vide.exe !"
    bottom_message_display(text, 30)

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(display, ac,(x,y,w,h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(display, ic,(x,y,w,h))
    message_display(msg, 20, x+w//2, y+h//2)

def undo():
    if len(states)>1:
        states.pop()
        print_grid()
        show_buttons(True)
        time.sleep(0.2)

def verify():
    if current_grid is None: return
    def find(x):
        while parent[parent[x]] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(x,y):
        parent[find(x)]=find(y)
    n, m, grille = grilles[current_grid]
    parent=[i for i in range(n*m)]
    for i in range(n-1):
        for j in range(m):
            if states[-1][i*m+j] == states[-1][i*m+m+j]:
                union(i*m+j, i*m+m+j)
    for i in range(n):
        for j in range(m-1):
            if states[-1][i*m+j] == states[-1][i*m+j+1]:
                union(i*m+j, i*m+j+1)
    find=[find(i) for i in range(n*m)]
    island_seen=set()
    water_seen = {}
    correct = True
    states.append(states[-1][:])
    for i in range(n):
        for j in range(m):
            if states[-1][i*m+j]==1: # rivière
                if find[i*m+j] not in water_seen: water_seen[find[i*m+j]] = []
                water_seen[find[i*m+j]].append((i,j))
            elif grille[i][j].isdigit(): # and state[-1][i*m+j] == 2, terre
                k = int(grille[i][j])
                ile = [x for x in range(n*m) if find[x]==find[i*m+j] and x!=i*m+j]
                if len(ile) != k-1 or any(grille[x//m][x%m].isdigit() for x in ile):
                    correct = False # Taille pas bonne ou plusieurs iles regroupées
                    for x in ile+[i*m+j]:
                        states[-1][x] = 3 # RED
                island_seen.add(find[i*m+j])
    for i in range(n):
        for j in range(m):
            if states[-1][i*m+j] == 2 and find[i*m+j] not in island_seen:
                correct = False # Ile pas rattachée à un chiffre
                ile = [x for x in range(n*m) if find[x]==find[i*m+j]]
                for x in range(n*m):
                    if find[x]==find[i*m+j]:
                         states[-1][x] = 3 # RED
    if len(water_seen) > 1:
        correct = False # rivière pas connexe
        w=max(water_seen)
        for i in range(n):
            for j in range(m):
                if not grille[i][j].isdigit():
                    if find[i*m+j] == w:
                        states[-1][i*m+j] = 4 # PURPLE
    for i in range(n-1):
        for j in range(m-1):
            if states[-1][i*m+j]==states[-1][i*m+j+1]==states[-1][i*m+j+m]==states[-1][i*m+j+m+1]==1:
                correct = False # Bassin (2*2 d'eau)
                for x in [i*m+j,i*m+j+1,i*m+j+m,i*m+j+m+1]:
                    states[-1][x] = 4 # PURPLE
    if correct:
        won.add(current_grid)
    else:
        print_grid()
        show_rules()
        states.pop()


def prev_page():
    global current_page
    if current_page > 0:
        current_page -= 1

def next_page():
    global current_page
    if current_page*20 + 20 <= len(grilles):
        current_page += 1

def print_new_grid(num):
    global current_grid
    current_grid = num
    n, m, grille = grilles[num]
    states.clear()
    states.append([0]*(n*m))
    time.sleep(0.1)
    print_grid()

def print_grid():
    display.fill(WHITE)
    n, m, grille = grilles[current_grid]
    sq_len = min(720//max(n,m), SQUARE_DEFAULT)
    xdeb = WIDTH//2 - sq_len * m // 2
    ydeb = (HEIGHT-150)//2 - sq_len * n // 2
    xfin = xdeb + sq_len * m
    yfin = ydeb + sq_len * n
    for i in range(n+1):
        pygame.draw.line(display, (0,0,0), (xdeb,ydeb+sq_len*i), (xfin,ydeb+sq_len*i), 2)
    for i in range(m+1):
        pygame.draw.line(display, (0,0,0), (xdeb+sq_len*i,ydeb), (xdeb+sq_len*i,yfin), 2)
    for i in range(n):
        for j in range(m):
            color = [WHITE, BLUE, BEIGE, RED, PURPLE][states[-1][i*m+j]]
            pygame.draw.rect(display, color, Rect(xdeb+j*sq_len+2, ydeb+i*sq_len+2, sq_len-2, sq_len-2))
            if grille[i][j].isdigit():
                message_display(grille[i][j], sq_len-2, xdeb+j*sq_len+sq_len//2, ydeb+i*sq_len+sq_len//2)

def onclick(b, x, y):
    global write
    if b in [2, 4, 5]:
        write = not write
        if write: pygame.mouse.set_cursor(*cursor_write)
        else: pygame.mouse.set_cursor(*cursor_erase)
    elif 100 <= x <= WIDTH-100:
        n, m, grille = grilles[current_grid]
        sq_len = min(720//max(n,m), SQUARE_DEFAULT)
        xdeb = WIDTH//2 - sq_len * m // 2
        ydeb = (HEIGHT-150)//2 - sq_len * n // 2
        xfin = xdeb + sq_len * m
        yfin = ydeb + sq_len * n
        if xdeb<=x<=xfin and ydeb<=y<=yfin:
            j = (x-xdeb)//sq_len
            i = (y-ydeb)//sq_len
            states.append(states[-1][:])
            if b == 1:
                states[-1][i*m+j] = 1*write
                if write and grille[i][j].isdigit():
                    states[-1][i*m+j] = 3
            elif b == 3:
                states[-1][i*m+j] = 2*write
        print_grid()

def show_buttons(from_undo=False):
    xbtn = ybtn = 5
    page = current_page
    button("", 0,0, 135,35*21+5, WHITE,WHITE)
    for i in list(grilles.keys())[page*20:page*20+20]:
        button(i, xbtn,ybtn, 90,30, GRAY1 if i!=current_grid else GRAY3,GRAY3, lambda:print_new_grid(i))
        if i in won:
            display.blit(checkmark, (xbtn + 95 + 1, ybtn))
        ybtn+=35
    ybtn = 35*20+5
    button("<", xbtn,ybtn, 40,30, GRAY1 if page>0 else WHITE,GRAY3 if page>0 else WHITE, prev_page)
    button(">", xbtn+50,ybtn, 40,30, GRAY1 if page*20+20<=len(grilles) else WHITE,GRAY3 if page*20+20<=len(grilles) else WHITE, next_page)
    xbtn, ybtn = WIDTH - 90 - 5, 5
    button("Règles", xbtn,ybtn, 90,30, GRAY2,GRAY3, show_rules)
    button("Aide", xbtn,ybtn+35, 90,30, GRAY2,GRAY3, show_help)
    if len(states)>1 and not from_undo:
        button("Undo", xbtn,ybtn+140, 90,30, GRAY2,GRAY3, undo)
    else:
        button("", xbtn,ybtn+140, 90,30, WHITE,WHITE)
    if states[-1].count(0)+states[-1].count(3)+states[-1].count(4)==0:
        button("Vérifier", xbtn,ybtn+175, 90,30, GRAY2,GRAY3, verify)
    else:
        button("", xbtn,ybtn+175, 90,30, WHITE,WHITE)


def main():
    global grilles, display, clock, current_page, current_grid, states, write, cursor_write, cursor_erase, checkmark, won

    pygame.init()
    display = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Nurikabe")
    icon = pygame.image.load(os.path.join("Icones", "app_icon.png"))
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()
    display.fill(WHITE)
    pygame.display.flip()

    cursor_bin = []
    with open(os.path.join("Icones", "cursor_icon.txt")) as f:
        for line in f.readlines():
            cursor_bin.append(line.split('"')[1])
    cursor_write = pygame.cursors.compile(cursor_bin)
    cursor_erase = pygame.cursors.compile([string[::-1] for string in cursor_bin[::-1]])
    #if pygame.__version__ < "2":
    cursor_write = ((24,24), (0,0)) + cursor_write
    cursor_erase = ((24,24), (0,0)) + cursor_erase
    pygame.mouse.set_cursor(*cursor_write)

    checkmark = pygame.image.load(os.path.join("Icones", "correct_icon.png"))
    write = True
    won = set()
    states = []
    grilles = {}
    try:
        load_grids()
    except Exception as e:
        message_display(str(e), 20)
        pygame.display.update()
        raise
    current_page = 0
    current_grid = None
    print_new_grid(os.listdir("Grilles")[0][:-4]) # current_grid = "04x04 1"

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return 0
            if event.type == MOUSEBUTTONDOWN:
                onclick(event.button, event.pos[0], event.pos[1])

        show_buttons()
        pygame.display.update()
        clock.tick(16)

if __name__ == "__main__":
    main()