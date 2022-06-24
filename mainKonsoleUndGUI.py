import scipy.stats as stats
import random
import time
import copy
import pygame
import sys
import time

while (True):

    # ----------------------------------------------------------------------
    #                                Konsole Code
    # ----------------------------------------------------------------------

    # Dictionary für das Spielfeld

    spielfeld = {}  # Key = (spalte, zeile), Wert = 'O' oder 'X' für den Stein des Spielers

    SPALTEN = 7
    ZEILEN = 6
    ZELLEN = ZEILEN * SPALTEN

    RICHTUNGEN = [
        (0, -1),  # S
        (1, -1),  # SO
        (1, 0),  # O
        (1, 1),  # NO #!3
        (0, 1),  # N
        (-1, 1),  # NW
        (-1, 0),  # W
        (-1, -1)  # SW #!7
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
            # pygame.quit()
            return True
        return False


    def suche_gewinner(feld):
        gewinner = False
        for zeile in reversed(range(6)):
            for spalte in range(7):
                checkpoint = (spalte, zeile)
                if checkpoint in spielfeld:  # Position Prüfen

                    for r in RICHTUNGEN:
                        # print(checkpoint, "Check")
                        move = checkpoint
                        reihe = 0
                        for i in range(1, 4):
                            move = addiere_tupelpaar(move, r)

                            if (move in spielfeld):
                                if (spielfeld[checkpoint] == spielfeld[move]):
                                    reihe += 1
                                    # print(move)
                                else:
                                    break
                        # print("richtung", r, "Gewinn:", reihe)
                        # print("")
                        if (reihe == 3):
                            break
                    if (reihe == 3):
                        gewinner = True
                        print("Gewonnen hat Spieler: ", spielfeld[checkpoint])
                        break
            if (gewinner == True):
                break
        return gewinner, checkpoint, r


    def suche_gewinner_bot(feld):  #
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
        print(move)
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
        return round(
            SPALTEN * stats.truncnorm.rvs((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma, size=N)[0])

        # ----------------------------------------------------------------------
        #                           Gewinner Suche
        # ----------------------------------------------------------------------


    def suche_gewinner_move():
        gewinner = -2
        for player in range(2):
            for col in range(SPALTEN):
                try:
                    temp_spielfeld = copy.deepcopy(spielfeld)
                    zeile = finde_tiefste_zeile(col)
                    temp_spielfeld[(col, zeile)] = 'X' if player == 0 else 'O'

                    if suche_gewinner_bot(temp_spielfeld):
                        gewinner -= player
                        print(gewinner)
                        return (col, gewinner)  # -2 = Bot gewinnt, -3 = spieler gewinnt
                except:
                    pass

        return (-1, "error_move")


    # ----------------------------------------------------------------------
    #                                GUI Code
    # ----------------------------------------------------------------------

    # initialize basic classes and modify general settings
    pygame.init()
    screen = pygame.display.set_mode([1270, 900])
    # don't use set_mode to create other surfaces, they wont show up on the screen
    background_surface = pygame.Surface([1270, 900])
    stone_surface = pygame.Surface([1270, 900])
    # initial_screen = pygame.display.set_mode([1270, 900])

    clock = pygame.time.Clock()
    pygame.display.set_caption("Super krasses 4-gewinnt was dein Leben verÃ¤ndern wird")


    def drop_stone(dest_pos_index):
        # use global keyword because i want to override y and current_stone here, otherwise this would result in an Unboundlocalerror
        # you have to explicitly type the global keyword to make clear which variable you want to use and that you don't want to create a new one in the function scope
        global y
        global current_stone
        y_copy = y
        acceleration = 1

        while y != (dest_pos_index * y_spacing_for_76 + y_copy):
            # dirty fix to make sure we reach the end of the loop, accelaration makes it comlicated
            if y >= (dest_pos_index * y_spacing_for_76 + y_copy):
                break

            acceleration = acceleration * 1.09
            y += 1 + acceleration
            draw_screen_surface()

        # make stoneposition permanent, switch player and reset y (and maybe x in the future, so that the initial position is 4)
        y = dest_pos_index * y_spacing_for_76 + y_copy
        background_surface.blit(current_stone, (x, y))
        current_stone = switch_stone(current_stone)
        y = y_copy


    def draw_screen_surface():
        screen.blit(background_surface, (0, 0))
        screen.blit(current_stone, (x, y))
        screen.blit(spielfeld_GUI, (0, 180))
        # display our drawings
        pygame.display.update()


    def draw_winning_surface(pos_endstein, r):
        print(pos_endstein)
        richtung = finde_richtung(r)
        if (richtung == 3):
            a = convert_spalte_x[pos_endstein[0] - 3]
            b = convert_zeile_y[pos_endstein[1]]
            print(a, b)
        else:
            a = convert_spalte_x[pos_endstein[0]]
            b = convert_zeile_y[pos_endstein[1]]
            print(a, b)

        screen.blit(background_surface, (0, 0))
        screen.blit(spielfeld_GUI, (0, 180))
        if (richtung == 0):
            screen.blit(linie_0, (a, b))
        elif (richtung == 1):
            screen.blit(linie_1, (a, b))
        elif (richtung == 2):
            screen.blit(linie_2, (a, b))
        elif (richtung == 3):
            screen.blit(linie_3, (a, b))
        else:
            print("error_draw_winning_surface")
        # display our drawings
        pygame.display.update()


    def draw_initial_surface():
        pass


    def switch_stone(current_stone):
        if current_stone == gelber_stein:
            current_stone = roter_stein
        else:
            current_stone = gelber_stein
        return current_stone


    ##definition stuff
    # import graphics
    spielfeld_GUI = pygame.image.load("re_Spielfeld.png")
    initial_spielfeld = spielfeld_GUI.copy()
    roter_stein = pygame.image.load("re_rot.png")
    initial_roter_stein = roter_stein.copy()
    gelber_stein = pygame.image.load("re_gelb.png")

    linie_0 = pygame.image.load("re_Linie0.png")
    initial_spielfeld = linie_0.copy()
    linie_1 = pygame.image.load("re_Linie1.png")
    initial_spielfeld = linie_1.copy()
    linie_2 = pygame.image.load("re_Linie2.png")
    initial_spielfeld = linie_2.copy()
    linie_3 = pygame.image.load("re_Linie3.png")
    initial_spielfeld = linie_3.copy()

    first_field_coordinates = (-283, -34)

    # color variables shortcuts
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    # some variables for moving elements around and keep track of the actual position of the current stone
    x_spacing_for_76 = 95
    y_spacing_for_76 = 87
    x = 313 + 3 * x_spacing_for_76
    y = 240 - y_spacing_for_76
    x_index = 4

    # this will be player one or two - the right side is the default value aka player which makes the first move
    current_stone = roter_stein

    # static stuff - do that once instead of doing that every frame inside the loop
    background_surface.fill(WHITE)

    # ----------------------------------------------------------------------
    #                       Kombination Konsole-GUI
    # ----------------------------------------------------------------------
    convert_zeile_dropStone = [i for i in range(6, 0, -1)]

    convert_spalte_x = {}
    shift = 38
    for i in range(7):
        convert_spalte_x[i] = 313 + shift
        shift += 95  # x_spacing_for_76

    convert_zeile_y = {}
    shift = 40
    for i in reversed(range(6)):
        convert_zeile_y[i] = 240 + shift
        shift += 87  # y_spacing_for_76

    convert_spalte_x_bot = {}
    shift = 0
    for i in range(7):
        convert_spalte_x_bot[i] = 313 + shift
        shift += x_spacing_for_76

    convert_zeile_y_bot = {}
    shift = 40
    for i in reversed(range(6)):
        convert_zeile_y_bot[i] = 240 + shift
        shift += y_spacing_for_76


    def finde_richtung(r):
        # senkrecht
        if (RICHTUNGEN[0] == r or RICHTUNGEN[4] == r):
            return 0
        # waagerecht
        if (RICHTUNGEN[2] == r or RICHTUNGEN[6] == r):
            return 1
        # diagonal gut
        if (RICHTUNGEN[5] == r or RICHTUNGEN[1] == r):
            return 2
        # diagonal schlecht
        if (RICHTUNGEN[3] == r or RICHTUNGEN[7] == r):
            return 3
        else:
            print("error Richtung")
            return -1


    # ----------------------------------------------------------------------
    #                                Game
    # ----------------------------------------------------------------------
    anfang = random.randint(0, 1)
    spieler = True if anfang == 0 else False  # True: Spieler 1; False: Spieler 2
    bot = True  # True: Bot aktiviert (1 Spieler); False: 2 Spieler
    bot_schwierigkeit = 1  # 0 = Easy ; 1 = Normal ; 2 = Hard
    running = True  # 'e' als Input zum Beenden des Spiels
    gewinner = False
    unentschieden = False

    # counter is sometimes useful for fixing things
    counter = 0

    while (running):

        # standard exit/break out the loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pressed_button_vert = pygame.key.get_pressed()
        if pressed_button_vert[pygame.K_RIGHT]:
            x_index += 1
            if x_index > 7:
                x_index -= 1
            else:
                x += x_spacing_for_76
                # sleep because otherwise a click is more than click and we don't want that #dirty fix
                time.sleep(0.07)

        if pressed_button_vert[pygame.K_LEFT]:
            x_index -= 1
            if x_index < 1:
                x_index += 1
            else:
                x -= x_spacing_for_76
                time.sleep(0.07)

        if pressed_button_vert[pygame.K_RETURN] or (bot and not spieler):

            # --------------------------------------------------
            if bot and not spieler:
                if bot_schwierigkeit == 0:
                    spalte = bot_easy_move()
                elif bot_schwierigkeit == 1:
                    spalte = bot_normal_move()
                else:
                    spalte = bot_hard_move()
            else:
                spalte = x_index - 1

            if spalte_gueltig(spalte):

                print("x: ", x, ", spalte: ", spalte)
                x = convert_spalte_x_bot[spalte]  # Achtung hier können noch fehler auftreten! Keine Ahnung wie?

                zeile = finde_tiefste_zeile(spalte)
                print(spalte, zeile)
                spielfeld[(spalte, zeile)] = 'O' if spieler else 'X'

                print_spielfeld()
                print_spalten_nummern()

                spieler = not spieler
                if (suche_gewinner(spielfeld)[0]):
                    running = False
                    gewinner = True
                if check_unentschieden():
                    running = False
                    unentschieden = True
                # --------------------------------------------------

                # Achtung hier können noch fehler auftreten! Keine Ahnung wie?
                drop_stone(convert_zeile_dropStone[zeile])  # Number of Falling Rows
                x = convert_spalte_x_bot[x_index - 1]
                print(x, "|", y)

        if (gewinner):
            pos_endstein = suche_gewinner(spielfeld)[1]
            richtung = suche_gewinner(spielfeld)[2]
            draw_winning_surface(pos_endstein, richtung)
            # pygame.quit()
        elif (unentschieden):
            pass
        else:
            draw_screen_surface()

        # 60 frames per second refresh rate
        clock.tick(60)
        counter += 1
        # print(counter)
        # -------------------------------------------
    pygame.time.wait(5000)

    counter += 1
    # print(counter)
    '''
    spalte = input("Beenden: ")
    if spalte == 'j':
        pygame.quit()
        break
    else:
        pass
    '''