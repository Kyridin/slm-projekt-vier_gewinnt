import scipy.stats as stats
import random
import time
import copy

# Dictionary für das Spielfeld

spielfeld = {}  # Key = (spalte, zeile), Wert = 'O' oder 'X' für den Stein des Spielers

SPALTEN = 7
ZEILEN = 6
ZELLEN = ZEILEN * SPALTEN

RICHTUNGEN = [
    (0, -1),  # S
    (1, -1),  # SO
    (1, 0),  # O
    (1, 1),  # NO
    (0, 1),  # N
    (-1, 1),  # NW
    (-1, 0),  # W
    (-1, -1)  # SW
]


def spalte_gueltig(spalte):
    if ((spalte, ZEILEN - 1) in spielfeld):
        return False
    if spalte >= 0 and spalte < SPALTEN:
        return True


def finde_tiefste_zeile(spalte):
    for zeile in range(ZEILEN):
        if (spalte, zeile) not in spielfeld:
            return zeile


def print_spielfeld():
    for zeile in reversed(range(6)):
        for spalte in range(7):
            pos = (spalte, zeile)
            if pos in spielfeld:  # Position Prüfen
                print(spielfeld[pos], end=' ')
            else:
                print('.', end=' ')
        print()


def print_spalten_nummern():
    anz_spalten = [str(i) for i in range(SPALTEN)]
    print(" ".join(anz_spalten))


def addiere_tupelpaar(a, b):
    c = (a[0] + b[0], a[1] + b[1])
    return c


def check_unentschieden():
    spielfeld_gefuellt = list()
    for i in range(SPALTEN + 1):
        if spalte_gueltig(i):
            spielfeld_gefuellt.append(1)
        else:
            spielfeld_gefuellt.append(0)

    if len(set(spielfeld_gefuellt)) == 1:
        print("\nUNENTSCHIEDEN")
        return True
    return False


def suche_gewinner(feld):
    gewinner = False
    for stein in range(1, len(feld) + 1):
        checkpoint = list(feld)[-stein]

        for r in RICHTUNGEN:
            move = checkpoint
            reihe = 0
            for i in range(1, 4):
                move = addiere_tupelpaar(move, r)

                if (move in feld):
                    if (feld[checkpoint] == feld[move]):
                        reihe += 1
                    else:
                        break
            if (reihe == 3):
                break

        if (reihe == 3):
            gewinner = True
            print("Gewonnen hat Spieler: ", feld[checkpoint])
            break
    return gewinner


# ----------------------------------------------------------------------
#                                BOT Stuff
# ----------------------------------------------------------------------

def bot_easy_move():
    """Bot, der zufällige moves wählt"""
    for i in range(3):
        print('.', end=' ')
        time.sleep(.2)
    print('\n')
    spalte = random.randint(0, 6)
    print(spalte)
    return spalte


def bot_normal_move():
    """
    Bot der einen garantierten Gewinnerzug macht, wenn möglich und
    Gewinnerzüge vom Gegner verhindert.
    Falls es keine Gewinnerzüge gibt, wird der move zufällig aus
    der Normalverteilung gewählt (mittlere Spalten werden minimal bevorzugt)
    """
    # check ob Bot oder Spieler gewinnen kann und setze in die Spalte einen Stein
    move = suche_gewinner_move()[0]
    if move != -1:
        return move

    return normal_distribution()


def bot_hard_move():
    pass


def normal_distribution():
    lower = 0
    upper = 1
    mu = 0.5
    sigma = 0.3
    N = 1
    return round(SPALTEN * stats.truncnorm.rvs((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma, size=N)[0])


def suche_gewinner_move():
    gewinner = -2
    for player in range(2):
        for col in range(SPALTEN):
            try:
                temp_spielfeld = copy.deepcopy(spielfeld)
                zeile = finde_tiefste_zeile(col)
                temp_spielfeld[(col, zeile)] = 'X' if player == 0 else 'O'

                if suche_gewinner(temp_spielfeld):
                    gewinner -= player
                    return (col, gewinner)  # -2 = Bot gewinnt, -3 = spieler gewinnt
            except:
                pass

    return (-1, None)


# ----------------------------------------------------------------------
#                                  Game
# ----------------------------------------------------------------------

anfang = random.randint(0, 1)
spieler = True if anfang == 0 else False  # True: Spieler 1; False: Spieler 2
bot = True  # True: Bot aktiviert (1 Spieler); False: 2 Spieler
bot_schwierigkeit = 1  # 0 = Easy ; 1 = Normal ; 2 = Hard
running = True  # 'e' als Input zum Beenden des Spiels

while (running):
    while (running):
        if bot and not spieler:
            if bot_schwierigkeit == 0:
                spalte = bot_easy_move()
            elif bot_schwierigkeit == 1:
                spalte = bot_normal_move()
            else:
                spalte = bot_hard_move()
        else:
            spalte = input("Ihr Zug(Spalte 0-{}): ".format(SPALTEN))  # Wahrung Fehlt bei Eingabe von Text
        if spalte == 'e':
            running = False
            break
        try:
            spalte = int(spalte)
            if spalte_gueltig(spalte):
                break
        except:
            pass
    if spalte == 'e':
        print_spielfeld()
        break

    zeile = finde_tiefste_zeile(spalte)
    print(spalte, zeile)
    spielfeld[(spalte, zeile)] = 'O' if spieler else 'X'

    print_spielfeld()
    print_spalten_nummern()

    spieler = not spieler
    running = not suche_gewinner(spielfeld)

    if check_unentschieden():
        running = False
        break


# ----------------------------------------------------------------------
#                         Alpha-Beta-Pruning
# ----------------------------------------------------------------------

# Reference: https://github.com/KeithGalli/Connect4-Python/blob/master/connect4_with_ai.py
