import scipy.stats as stats
import random
import time
import copy
import pygame
import sys
import time

# Spieleinstellungen die nur bei Beginn einmal eingestellt werden
bot = False  # True: Bot aktiviert (1 Spieler); False: 2 Spieler
bot_schwierigkeit = 1  # 0 = Easy ; 1 = Normal ; 2 = Hard
spielen_auswahl = False
schwierigkeit_auswahl = False

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
        # for i in range(3):
        #    print('.', end=' ')
        time.sleep(0.5)
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
        time.sleep(0.5)
        print(move)
        if move != -1:
            return move

        return normal_distribution()


    def bot_hard_move():
        move = suche_gewinner_move()[0]
        time.sleep(0.5)
        print(move)
        if move != -1:
            return move
        return normal_distribution()


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

        return (-1, print("error_move"))


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
    pygame.display.set_caption("4-gewinnt Spiel")


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
    # current_stone = roter_stein #nach unten verschoben! damit Stein abhänig vonder Konsole ist

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
    #                          Zugabe Buttons
    # ----------------------------------------------------------------------

    buttons_transparent = pygame.image.load("Buttons_Transparent.png")
    hauptmenue_1 = pygame.image.load("Hauptmenue_1.png")
    schwierigkeitsauswahl = pygame.image.load("Schwierigkeitsauswahl.png")
    abschluss = pygame.image.load("Abschluss.png")

    gelb_win = pygame.image.load("gelb_win.png")
    rot_win = pygame.image.load("rot_win.png")
    du_win = pygame.image.load("du_win.png")
    com_win = pygame.image.load("com_win.png")
    unent_win = pygame.image.load("unentschieden.png")
    spalte_button = pygame.image.load("Spalte.png")


    def draw_hauptmenue_surface():
        screen.blit(background_surface, (0, 0))
        # screen.blit(buttons_transparent, (366, 193))
        screen.blit(hauptmenue_1, (366, 193))
        pygame.display.update()


    def draw_schwierigkeit_surface():
        screen.blit(background_surface, (0, 0))
        screen.blit(schwierigkeitsauswahl, (366, 193))
        pygame.display.update()


    def draw_abschluss_surface(anzeige_0):
        screen.blit(abschluss, (366, 193))
        if (anzeige_0 == 0):
            screen.blit(gelb_win, (400, 267))
            screen.blit(gelber_stein, (600, 100))
        elif (anzeige_0 == 1):
            screen.blit(rot_win, (400, 267))
            screen.blit(roter_stein, (600, 100))
        elif (anzeige_0 == 2):
            screen.blit(com_win, (400, 267))
            screen.blit(roter_stein, (600, 100))
        elif (anzeige_0 == 3):
            screen.blit(unent_win, (400, 267))
            screen.blit(gelber_stein, (400, 100))
            screen.blit(roter_stein, (800, 100))
        elif (anzeige_0 == 4):
            screen.blit(du_win, (400, 267))
            screen.blit(gelber_stein, (600, 100))
        pygame.display.update()


    def button(screen, position, text, size, colors="white on blue"):
        fg, bg = colors.split(" on ")
        font = pygame.font.SysFont("Arial", size)
        text_render = font.render(text, 1, fg)
        x, y, w, h = text_render.get_rect()
        x, y = position
        pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w, y), 5)
        pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
        pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w, y + h), 5)
        pygame.draw.line(screen, (50, 50, 50), (x + w, y + h), [x + w, y], 5)
        pygame.draw.rect(screen, bg, (x, y, w, h))
        print(screen.blit(text_render, (x, y)))
        return screen.blit(text_render, (x, y))


    b1 = button(screen, (403, 375), "          ", 60, "red on yellow")
    b2 = button(screen, (569, 375), "          ", 60, "blue on green")
    b3 = button(screen, (735, 375), "          ", 60, "white on blue")


    def button2(screen, position, text, size, colors="white on blue"):
        x, y = position
        w = 80
        h = 800
        return screen.blit(spalte_button, (x, y))


    s0 = button2(screen, (326 - 10, 120), "", 20, "white on blue")
    s1 = button2(screen, (421 - 10, 120), "", 20, "white on yellow")
    s2 = button2(screen, (515 - 10, 120), "", 20, "white on green")
    s3 = button2(screen, (609 - 10, 120), "", 20, "white on blue")
    s4 = button2(screen, (703 - 10, 120), "", 20, "white on yellow")
    s5 = button2(screen, (796 - 10, 120), "", 20, "white on green")
    s6 = button2(screen, (891 - 10, 120), "", 20, "white on blue")


    def start():
        time.sleep(0.5)


    # ----------------------------------------------------------------------
    #                                Game
    # ----------------------------------------------------------------------

    # Einstellungen die immer wieder zurückgesetzt werden
    anfang = random.randint(0, 1)
    spieler = True if anfang == 0 else False  # True: Spieler 1; False: Spieler 2
    current_stone = gelber_stein if spieler else roter_stein
    mouse_pressed = False
    running = True
    gewinner = False
    unentschieden = False
    abschluss_auswahl = False
    anzeige_1 = -1
    counter = 0

    pygame.K_RIGHT, pygame.K_UP, pygame.K_LEFT
    while (running):

        while (not spielen_auswahl):
            for event in pygame.event.get():
                pfeil_links = False
                pfeil_oben = False
                if (event.type == pygame.QUIT):
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RIGHT:
                        pygame.quit()
                    elif event.key == pygame.K_s or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        pfeil_oben = True
                    elif event.key == pygame.K_LEFT:
                        pfeil_links = True
                if event.type == pygame.MOUSEBUTTONDOWN or pfeil_links or pfeil_oben:
                    # check when you click if the coordinates of the pointer are in the rectangle of the buttons
                    if b1.collidepoint(pygame.mouse.get_pos()) or pfeil_links:
                        start()
                        bot = True
                        bot_schwierigkeit = 1
                        spielen_auswahl = True
                        break
                    elif b2.collidepoint(pygame.mouse.get_pos()) or pfeil_oben:
                        start()
                        bot = False
                        spielen_auswahl = True
                        schwierigkeit_auswahl = True
                        break
                    elif b3.collidepoint(pygame.mouse.get_pos()):
                        pygame.quit()
            draw_hauptmenue_surface()

        while (not schwierigkeit_auswahl):
            for event in pygame.event.get():
                pfeil_links = False
                pfeil_oben = False
                pfeil_rechts = False
                if (event.type == pygame.QUIT):
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        pfeil_rechts = True
                    elif event.key == pygame.K_s or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        pfeil_oben = True
                    elif event.key == pygame.K_LEFT:
                        pfeil_links = True
                if event.type == pygame.MOUSEBUTTONDOWN or pfeil_links or pfeil_oben or pfeil_rechts:
                    # check when you click if the coordinates of the pointer are in the rectangle of the buttons
                    if b1.collidepoint(pygame.mouse.get_pos()) or pfeil_links:
                        start()
                        bot_schwierigkeit = 0
                        schwierigkeit_auswahl = True
                        break
                    elif b2.collidepoint(pygame.mouse.get_pos()) or pfeil_oben:
                        start()
                        bot_schwierigkeit = 1
                        schwierigkeit_auswahl = True
                        start()
                        break
                    elif b3.collidepoint(pygame.mouse.get_pos()) or pfeil_rechts:
                        bot_schwierigkeit = 2
                        schwierigkeit_auswahl = True
                        start()
            draw_schwierigkeit_surface()

        # standard exit/break out the loop
        for event in pygame.event.get():
            pfeil_unten = False
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    pfeil_unten = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            # check when you click if the coordinates of the pointer are in the rectangle of the buttons
            if s0.collidepoint(pygame.mouse.get_pos()):
                mouse_pressed = True
                spalte = 0
            elif s1.collidepoint(pygame.mouse.get_pos()):
                mouse_pressed = True
                spalte = 1
            elif s2.collidepoint(pygame.mouse.get_pos()):
                mouse_pressed = True
                spalte = 2
            elif s3.collidepoint(pygame.mouse.get_pos()):
                mouse_pressed = True
                spalte = 3
            elif s4.collidepoint(pygame.mouse.get_pos()):
                mouse_pressed = True
                spalte = 4
            elif s5.collidepoint(pygame.mouse.get_pos()):
                mouse_pressed = True
                spalte = 5
            elif s6.collidepoint(pygame.mouse.get_pos()):
                mouse_pressed = True
                spalte = 6

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

        if pressed_button_vert[pygame.K_RETURN] or (bot and not spieler) or mouse_pressed or pfeil_unten:

            # --------------------------------------------------
            if bot and not spieler:
                if bot_schwierigkeit == 0:
                    spalte = bot_easy_move()
                elif bot_schwierigkeit == 1:
                    spalte = bot_normal_move()
                else:
                    spalte = bot_hard_move()
            elif mouse_pressed:
                pass
            else:
                spalte = x_index - 1

            mouse_pressed = False

            if spalte_gueltig(spalte):

                print("x: ", x, ", spalte: ", spalte)
                x = convert_spalte_x_bot[spalte]

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
    pygame.time.wait(2500)

    if (unentschieden):
        anzeige_1 = 3
    elif (bot and spieler):
        anzeige_1 = 2
    elif (bot):
        anzeige_1 = 4
    elif (not spieler):
        anzeige_1 = 0
    elif (spieler):
        anzeige_1 = 1

    while (not abschluss_auswahl):
        for event in pygame.event.get():
            pfeil_links = False
            pfeil_oben = False
            if (event.type == pygame.QUIT):
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RIGHT:
                    pygame.quit()
                elif event.key == pygame.K_s or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    pfeil_oben = True
                elif event.key == pygame.K_LEFT:
                    pfeil_links = True
            if event.type == pygame.MOUSEBUTTONDOWN or pfeil_oben or pfeil_links:
                # check when you click if the coordinates of the pointer are in the rectangle of the buttons
                if b1.collidepoint(pygame.mouse.get_pos()) or pfeil_links:
                    spielen_auswahl = True
                    schwierigkeit_auswahl = True
                    abschluss_auswahl = True
                    break

                elif b2.collidepoint(pygame.mouse.get_pos()) or pfeil_oben:
                    spielen_auswahl = False
                    schwierigkeit_auswahl = False
                    abschluss_auswahl = True
                    break

                elif b3.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()

        draw_abschluss_surface(anzeige_1)

    # counter += 1
    # print(counter)