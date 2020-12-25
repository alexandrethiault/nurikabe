# coding: utf-8

import os
import time
import ctypes
import pygame
if pygame.__version__ >= "2":
    from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEWHEEL, Rect
else:
    from pygame.locals import QUIT, MOUSEBUTTONDOWN, Rect


## Global parameters

if os.name == "nt":
    ctypes.windll.shcore.SetProcessDpiAwareness(2)

pygame.init()
info = pygame.display.Info()
SCREEN_W, SCREEN_H = info.current_w, info.current_h
RATIO = min(SCREEN_W/1236, SCREEN_H/1080)
pygame.quit()

WHITE, BLACK = (255,255,255), (0,0,0)
GRAY1, GRAY2, GRAY3 = (220,220,220), (190,190,190), (150,150,150)
BLUE, BEIGE, RED, PURPLE = (208,250,249), (255,244,223), (255,0,0), (255,0,255)

WIDTH, HEIGHT = int(1030*RATIO), int(900*RATIO)
SQUARE_DEFAULT = int(60*RATIO)
EPS = int(5*RATIO)
BOTTOM_TEXT_HEIGHT = int(150*RATIO)
COLUMNS_WIDTH = int(150*RATIO)
BUTTONS_PER_COLUMN = 21
FONT_S, FONT_L = int(20*RATIO), int(30*RATIO)

COLUMNS_HEIGHT = HEIGHT - BOTTOM_TEXT_HEIGHT
NURIKABE_SPACE_WIDTH = WIDTH - 2*COLUMNS_WIDTH
NURIKABE_WIDTH = NURIKABE_SPACE_WIDTH - 2*EPS
NURIKABE_SPACE_HEIGHT = HEIGHT - BOTTOM_TEXT_HEIGHT
NURIKABE_HEIGHT = NURIKABE_SPACE_HEIGHT - 2*EPS
NURIKABE_SIZE = min(NURIKABE_WIDTH, NURIKABE_HEIGHT)
BUTTON_SPACE_HEIGHT = (HEIGHT - BOTTOM_TEXT_HEIGHT - EPS) // BUTTONS_PER_COLUMN
BUTTON_HEIGHT = BUTTON_SPACE_HEIGHT - EPS
CHECKMARK_SIZE = BUTTON_HEIGHT # Should approximate actual size of resource image
CHECKMARK_X_DEB = COLUMNS_WIDTH - CHECKMARK_SIZE - EPS
BUTTON_WIDTH = CHECKMARK_X_DEB - 2*EPS

"""
If RATIO is exactly one, these are going to be the window dimensions:
<150><-------730--------><150>
______________________________ ^
|    |                  |    | |
|    |                  |    | |
|    |                  |    | |
|    |                  |    | |
|    |                  |    | |
|    |                  |    | | 750
|    |                  |    | |
|    |                  |    | |
|    |                  |    | |
|    |                  |    | |
|____|__________________|____| v
|                            | ^
|                            | | 150
|____________________________| v
Columns' 150 = 5+105+5 + 30 + 5 :
5 for spacings, 105 for buttons, 30 for checkmarks
"""

## Reading of grids from Grids folder once and for all

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
            raise ValueError("Un fichier de grille valide doit renseigner le nombre de lignes et le nombre\nde colonnes dans les deux premières lignes du fichier, de la façon suivante :\n... lignes\n... colonnes\n...")
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

## Text stuff

def fill_white(x, y, w, h):
    pygame.draw.rect(display, WHITE, (x, y, w, h))

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
    pygame.draw.rect(display, WHITE, (0,COLUMNS_HEIGHT, WIDTH,BOTTOM_TEXT_HEIGHT))
    message_display(text, size, WIDTH//2, HEIGHT-BOTTOM_TEXT_HEIGHT//2)

def show_rules():
    text = "Il y a une grille de carrés, dont certains contiennent un nombre. Le but est de déterminer pour chaque\ncarré s'il est rivière ou terre ferme. Les cases de rivière forment le nurikabe (courant en japonais) : elles\ndoivent toutes être contigües par un côté, ne doivent pas contenir de nombre et ne doivent contenir aucun\nbloc 2x2 ou plus grand (de tels blocs sont appelés bassins). Les cases de terre ferme forment les îles :\nchaque nombre doit faire partie d'un îlot d'autant de cases de terre ferme. Chaque case de terre\nferme ne doit appartenir qu'à une seule île et chaque île ne contient qu'un nombre."
    bottom_message_display(text, FONT_S)

def show_help():
    text = "Cliquez sur un des boutons à gauche pour charger une nouvelle \ngrille de nurikabe. Faites un clic droit sur un carré de la grille pour\nle noter comme terre ou un clic gauche pour le noter comme rivière.\nLa molette permet de passer en mode gommage."
    bottom_message_display(text, FONT_L)

## Actions and buttons stuff

def button(msg, x, y, w, h, ic, ac, action=None, actionname=None):
    global last_clicked
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(display, ac,(x,y,w,h))
        if click[0] == 1 and action is not None:
            if actionname not in last_clicked: last_clicked[actionname] = -1
            dt = time.time() - last_clicked[actionname]
            if dt > 0.250:
                action()
                last_clicked[actionname] = time.time()
    else:
        pygame.draw.rect(display, ic,(x,y,w,h))
    message_display(msg, FONT_S, x+w//2, y+h//2)

def undo():
    if len(states)>1:
        states.pop()
        print_grid()

def set_checkpoint():
    global checkpoints
    checkpoints[current_grid] = [state[:] for state in states]

def get_checkpoint():
    global checkpoints, states
    states = [state[:] for state in checkpoints[current_grid]]
    print_grid()

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
    parent = [i for i in range(n*m)]
    for i in range(n-1):
        for j in range(m):
            if states[-1][i*m+j] == states[-1][i*m+m+j]:
                union(i*m+j, i*m+m+j)
    for i in range(n):
        for j in range(m-1):
            if states[-1][i*m+j] == states[-1][i*m+j+1]:
                union(i*m+j, i*m+j+1)
    find = [find(i) for i in range(n*m)]
    island_seen=set()
    water_seen = {}
    correct = True
    states.append(states[-1][:])
    for i in range(n):
        for j in range(m):
            if states[-1][i*m+j] == 1: # rivière
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
            if states[-1][i*m+j] == states[-1][i*m+j+1] == states[-1][i*m+j+m] == states[-1][i*m+j+m+1] == 1:
                correct = False # Bassin (2*2 d'eau)
                for x in [i*m+j,i*m+j+1,i*m+j+m,i*m+j+m+1]:
                    states[-1][x] = 4 # PURPLE
    if correct:
        won.add(current_grid)
        states.pop()
        set_checkpoint()
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
    if (current_page+1)*(BUTTONS_PER_COLUMN-1) <= len(grilles):
        current_page += 1

def print_new_grid(num):
    global current_grid, checkpoints
    fill_white(0, COLUMNS_HEIGHT, WIDTH, BOTTOM_TEXT_HEIGHT)
    if current_grid is not None and len(states)>1 and current_grid not in checkpoints:
        set_checkpoint()
    current_grid = num
    n, m, grille = grilles[num]
    states.clear()
    states.append([0]*(n*m))
    #time.sleep(0.1)
    print_grid()

def print_grid():
    fill_white(COLUMNS_WIDTH, 0, NURIKABE_SPACE_WIDTH, NURIKABE_SPACE_HEIGHT)
    n, m, grille = grilles[current_grid]
    sq_len = min(NURIKABE_WIDTH//m, NURIKABE_HEIGHT//n, SQUARE_DEFAULT)
    xdeb = WIDTH//2 - sq_len * m // 2
    ydeb = NURIKABE_SPACE_HEIGHT//2 - sq_len * n // 2
    xfin = xdeb + sq_len * m
    yfin = ydeb + sq_len * n
    for i in range(n+1):
        pygame.draw.line(display, (0,0,0), (xdeb,ydeb+sq_len*i), (xfin,ydeb+sq_len*i), 2)
    for i in range(m+1):
        pygame.draw.line(display, (0,0,0), (xdeb+sq_len*i,ydeb), (xdeb+sq_len*i,yfin), 2)
    for i in range(n):
        for j in range(m):
            color = (WHITE, BLUE, BEIGE, RED, PURPLE)[states[-1][i*m+j]]
            pygame.draw.rect(display, color, Rect(xdeb+j*sq_len+2, ydeb+i*sq_len+2, sq_len-2, sq_len-2))
            if grille[i][j].isdigit():
                message_display(grille[i][j], sq_len-2, xdeb+j*sq_len+sq_len//2, ydeb+i*sq_len+sq_len//2)

## Button positions and management of click events

def onclick(b, x, y):
    global write
    if b in [2, 4, 5]: # Scroll
        write = not write
        if write: pygame.mouse.set_cursor(*cursor_write)
        else: pygame.mouse.set_cursor(*cursor_erase)
    elif COLUMNS_WIDTH <= x <= WIDTH-COLUMNS_WIDTH and y <= NURIKABE_SPACE_HEIGHT:
        n, m, grille = grilles[current_grid]
        sq_len = min(NURIKABE_WIDTH//m, NURIKABE_HEIGHT//n, SQUARE_DEFAULT)
        xdeb = WIDTH//2 - sq_len * m // 2
        ydeb = NURIKABE_SPACE_HEIGHT//2 - sq_len * n // 2
        xfin = xdeb + sq_len * m
        yfin = ydeb + sq_len * n
        if xdeb<=x<=xfin and ydeb<=y<=yfin:
            j = (x-xdeb)//sq_len
            i = (y-ydeb)//sq_len
            states.append(states[-1][:])
            if b == 1: # Left click
                states[-1][i*m+j] = 1*write
                if write and grille[i][j].isdigit():
                    states[-1][i*m+j] = 3
            elif b == 3: # Right click
                states[-1][i*m+j] = 2*write
        print_grid()

def show_buttons():
    # Left size buttons: 20 grids and two page change buttons
    xbtn = ybtn = EPS
    page = current_page
    fill_white(0,0, COLUMNS_WIDTH,COLUMNS_HEIGHT)
    for i in list(grilles.keys())[page*(BUTTONS_PER_COLUMN-1):(page+1)*(BUTTONS_PER_COLUMN-1)]:
        button(i, xbtn,ybtn, BUTTON_WIDTH,BUTTON_HEIGHT, GRAY1 if i!=current_grid else GRAY3,GRAY3, lambda:print_new_grid(i) if i!=current_grid else None, f"print{i}")
        if i in won:
            display.blit(checkmark, (CHECKMARK_X_DEB, ybtn))
        ybtn += BUTTON_SPACE_HEIGHT
    ybtn = BUTTON_SPACE_HEIGHT*(BUTTONS_PER_COLUMN-1) + EPS
    button("<", xbtn,ybtn, BUTTON_WIDTH//2-EPS,BUTTON_HEIGHT, GRAY1 if page>0 else WHITE,GRAY3 if page>0 else WHITE, prev_page, "prev_page")
    button(">", xbtn+BUTTON_WIDTH//2+EPS,ybtn, BUTTON_WIDTH//2-EPS,BUTTON_HEIGHT, GRAY1 if (page+1)*(BUTTONS_PER_COLUMN-1)<=len(grilles) else WHITE,GRAY3 if (page+1)*(BUTTONS_PER_COLUMN-1)<=len(grilles) else WHITE, next_page, "next_page")
    # Right size buttons: rules, commands, checkpoint, undo, verify
    xbtn, ybtn = WIDTH - EPS - BUTTON_WIDTH, EPS
    button("Règles", xbtn,ybtn, BUTTON_WIDTH,BUTTON_HEIGHT, GRAY2,GRAY3, show_rules, "show_rules")
    ybtn += BUTTON_SPACE_HEIGHT
    button("Aide", xbtn,ybtn, BUTTON_WIDTH,BUTTON_HEIGHT, GRAY2,GRAY3, show_help, "show_help")
    ybtn += 2*BUTTON_SPACE_HEIGHT
    if len(states)>1:
        button("Retour à 0", xbtn,ybtn, BUTTON_WIDTH,BUTTON_HEIGHT, GRAY1,GRAY3, lambda:print_new_grid(current_grid), f"print{current_grid}")
    else:
        fill_white(xbtn,ybtn, BUTTON_WIDTH,BUTTON_HEIGHT)
    ybtn += BUTTON_SPACE_HEIGHT
    if len(states)>1:
        button("Annuler 1", xbtn,ybtn, BUTTON_WIDTH,BUTTON_HEIGHT, GRAY1,GRAY3, undo, "undo")
    else:
        fill_white(xbtn,ybtn, BUTTON_WIDTH,BUTTON_HEIGHT)
    ybtn += 2*BUTTON_SPACE_HEIGHT
    if len(states)>1 and current_grid not in won:
        button("Mémoriser", xbtn,ybtn, BUTTON_WIDTH,BUTTON_HEIGHT, GRAY1,GRAY3, set_checkpoint, "checkpoint")
    else:
        fill_white(xbtn,ybtn, BUTTON_WIDTH,BUTTON_HEIGHT)
    ybtn += BUTTON_SPACE_HEIGHT
    if current_grid in checkpoints or current_grid in won:
        button("Solution" if current_grid in won else "Mémoire", xbtn,ybtn, BUTTON_WIDTH,BUTTON_HEIGHT, GRAY2,GRAY3, get_checkpoint, "checkpoint")
    else:
        fill_white(xbtn,ybtn, BUTTON_WIDTH,BUTTON_HEIGHT)
    ybtn += 2*BUTTON_SPACE_HEIGHT
    if states[-1].count(0)+states[-1].count(3)+states[-1].count(4)==0:
        button("Vérifier", xbtn,ybtn, BUTTON_WIDTH,BUTTON_HEIGHT, GRAY2,GRAY3, verify, "verify")
    else:
        fill_white(xbtn,ybtn, BUTTON_WIDTH,BUTTON_HEIGHT)
    ybtn += BUTTON_SPACE_HEIGHT

## Main function : initialization and then event loop

def main():
    global grilles, display, clock, current_page, current_grid, states, write, cursor_write, cursor_erase, checkmark, won, last_clicked, checkpoints

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
    cursor_write = ((24,24), (0,0)) + cursor_write
    cursor_erase = ((24,24), (0,0)) + cursor_erase
    pygame.mouse.set_cursor(*cursor_write)

    checkmark = pygame.image.load(os.path.join("Icones", "correct_icon.png"))
    rect = checkmark.get_rect()
    checkmark = pygame.transform.scale(checkmark, (CHECKMARK_SIZE, CHECKMARK_SIZE*rect.h//rect.w))

    write = True
    won = set()
    states = []
    grilles = {}
    last_clicked = {}
    checkpoints = {}
    try:
        load_grids()
    except Exception as e:
        message_display(str(e), FONT_S)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return 0
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
            elif pygame.__version__ >= "2" and event.type == MOUSEWHEEL:
                onclick(4, 0, 0)

        show_buttons()
        pygame.display.update()
        clock.tick(16)


if __name__ == "__main__":
    try:
        main()
    except:
        pygame.quit()
        raise
