import cv2
import numpy as np
import time
import pyautogui as pg
import math
import chess_ai
import mss.tools
from screeninfo import get_monitors
import os.path

white_figures = {"Pawns" : [], "Knights" : [], "Rooks" : [], "Bishops" : [], "Queen" : [], "King" : []} # array for the standart layout of the white figures
black_figures = {"Pawns" : [], "Knights" : [], "Rooks" : [], "Bishops" : [], "Queen" : [], "King" : []} # array for the standart layout of the black figures

letters = ["A", "B", "C", "D", "E", "F", "G", "H"]

fields = {}

own_color = None
white_color = None
black_color = None

def nothing(x): # nothing
    pass

def createSliders(): # creates sliders window
    cv2.namedWindow("Sliders")
    cv2.createTrackbar("X-Coord", "Sliders", 0, screen_width, nothing)
    cv2.createTrackbar("Y-Coord", "Sliders", 0, screen_height, nothing)
    cv2.createTrackbar("X-Offset", "Sliders", 0, screen_width, nothing)
    cv2.createTrackbar("Y-Offset", "Sliders", 0, screen_height, nothing)
    cv2.createTrackbar("Confidence", "Sliders", 70, 100, nothing)
    cv2.createTrackbar("minDistance", "Sliders", 10, 50, nothing)
    cv2.createTrackbar("W->B", "Sliders", 0, 1, nothing)
    cv2.createTrackbar("Off->On", "Sliders", 0, 1, nothing)
    cv2.createTrackbar("calc", "Sliders", 0, 1, nothing)
    cv2.resizeWindow("Sliders", 300, 100)

def get_slider_pos(): # get positions from the sliders
    return cv2.getTrackbarPos("X-Coord", "Sliders"), cv2.getTrackbarPos("Y-Coord", "Sliders"), cv2.getTrackbarPos("X-Offset", "Sliders"), cv2.getTrackbarPos("Y-Offset", "Sliders")

def findFigures(img): # search chess figures in the given image
    global white_figures, black_figures, white_color, black_color

    confidence = cv2.getTrackbarPos("Confidence", "Sliders") / 100
    minDist = cv2.getTrackbarPos("minDistance", "Sliders")

    # for Black Figures    
    for blackFig in black_figures.keys():
        black_figures[blackFig] = []
        for fig in pg.locateAll(haystackImage=img, needleImage=f"black\{blackFig}.png", confidence=confidence):
            noise = False
            for coord in black_figures[blackFig]:
                dist = distance((coord.left, coord.top), (fig.left, fig.top))
                if dist < minDist and not dist == 0:
                    noise = True
            if noise == False:
                black_figures[blackFig].append(fig)
                cv2.rectangle(
                    img,
                    (fig.left, fig.top),
                    (fig.left + fig.width, fig.top + fig.height),
                    black_color,
                    2
                )

    # for White Figures
    for whiteFig in white_figures.keys():
        white_figures[whiteFig] = []
        for fig in pg.locateAll(haystackImage=img, needleImage=f"white\{whiteFig}.png", confidence=confidence):
            noise = False
            for coord in white_figures[whiteFig]:
                dist = distance((coord.left, coord.top), (fig.left, fig.top))
                if dist < minDist and not dist == 0:
                    noise = True
            if noise == False:
                white_figures[whiteFig].append(fig)
                cv2.rectangle(
                    img,
                    (fig.left, fig.top),
                    (fig.left + fig.width, fig.top + fig.height),
                    white_color,
                    2
                )

def draw_pattern(img, offx, offy): # draws the 8x8 pattern on the image
    field_x = offx / 8
    field_y = offy / 8

    for x in range(1, 8):
        x_coord = field_x * x

        cv2.line(img=img, pt1=(int(x_coord),0), pt2=(int(x_coord),int(offy)), color=(255,0,0), thickness=1)

    for y in range(1, 8):
        y_coord = field_y * y
        cv2.line(img=img, pt1=(0,int(y_coord)), pt2=(int(offx),int(y_coord)), color=(255,0,0), thickness=1)

    get_field_coords(img, offx, offy)

def get_field_coords(img, offx, offy): # calculates the position of every chess square and stores it in the field array
    global fields

    field_x = offx / 8 # calculates the offset of one chess square
    field_y = offy / 8

    num_list = [7,6,5,4,3,2,1,0]

    for letter in letters:
        for number in [1,2,3,4,5,6,7,8]:
            letter_number = letters.index(letter)

            x = int(field_x * letter_number + field_x / 2)
            y = int(field_y * num_list[number - 1] + field_y / 2)
            fields[f"{letter}{number}"] = (x,y)

def get_middle_pos(figure): # calculates center of a figure
    x = figure.left + figure.width / 2
    y = figure.top + figure.height / 2
    return x, y

def distance(p0, p1): # calculates the distance between two (x,y) tupels
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def get_figure_field(): # checks in which field, which figure is
    global white_figures, black_figures, white_figures_pos, black_figures_pos

    white_figures_pos = {"Pawns" : [], "Knights" : [], "Rooks" : [], "Bishops" : [], "Queen" : [], "King" : []}
    black_figures_pos = {"Pawns" : [], "Knights" : [], "Rooks" : [], "Bishops" : [], "Queen" : [], "King" : []}

    # White Figures
    for whiteFig in white_figures.keys():
        figures = white_figures[whiteFig]
        for figure in figures:
            closest_distance = 1000000
            closest_field = ""

            figure_x, figure_y = get_middle_pos(figure)
            for field in fields.keys():
                dist = distance(fields[field], (figure_x, figure_y))
                if dist < closest_distance:
                    closest_distance = dist
                    closest_field = field

            white_figures_pos[whiteFig].append(closest_field)
        white_figures_pos[whiteFig] = sorted(set(white_figures_pos[whiteFig]))

    # Black Figures
    for blackFig in black_figures.keys():
        figures = black_figures[blackFig]
        for figure in figures:
            closest_distance = 1000000
            closest_field = ""

            figure_x, figure_y = get_middle_pos(figure)
            for field in fields.keys():
                dist = distance(fields[field], (figure_x, figure_y))
                if dist < closest_distance:
                    closest_distance = dist
                    closest_field = field

            black_figures_pos[blackFig].append(closest_field)
        black_figures_pos[blackFig] = sorted(set(black_figures_pos[blackFig]))

    # writes the position
    for catagory in black_figures_pos.keys():
        for figure in black_figures_pos[catagory]:
            cv2.putText(img, f'{catagory} : {figure}', (int((fields[figure][0] - (offx / 8) / 2)),int(fields[figure][1])), cv2.QT_FONT_NORMAL, thickness=1, color= (255, 255, 255), fontScale=0.5)

    for catagory in white_figures_pos.keys():
        for figure in white_figures_pos[catagory]:
            cv2.putText(img, f'{catagory} : {figure}', (int((fields[figure][0] - (offx / 8) / 2)),int(fields[figure][1])), cv2.QT_FONT_NORMAL, thickness=1, color= (0, 0, 0), fontScale=0.5)

def draw_arrow(img, pt1, pt2): # draws arrow on image
    cv2.arrowedLine(img=img, pt1=pt1, pt2=pt2, color=(255,233,0), thickness=3)

def get_own_color(): # checks own color and adjust the colors
    global white_color, black_color, own_color
    if cv2.getTrackbarPos("W->B", "Sliders") == 0:
        own_color = "W"
        white_color = (0,255,0)
        black_color = (0,0,255)
    else:
        own_color = "B"
        white_color = (0,0,255)
        black_color = (0,255,0)

def check_for_error():
    for figure in ["Pawns", "Knights", "Rooks", "Bishops", "Queen", "King"]:
        for folder in ["black", "white"]:
            if not os.path.isfile(f"{folder}\{figure}.png"):
                print(f"The {figure} inside the {folder} folder is missing")

    if not os.path.isfile(f"config.json"):
        print("The config.json is missing")


# checking for errors
check_for_error()

# Get Monitor
monitor_sizes = []
for m in get_monitors():
    monitor_sizes.append(m)
monitor_num = int(input("Select Monitor: "))
screen_width = monitor_sizes[monitor_num - 1].width
screen_height = monitor_sizes[monitor_num - 1].height
print(f"] Monitor resolution is: {screen_width}*{screen_height}")

createSliders()

while True:
    x, y, offx, offy = get_slider_pos()

    mon = mss.mss().monitors[monitor_num]
    monitor = {
        "top": mon["top"] + y,  # 100px from the top
        "left": mon["left"] + x,  # 100px from the left
        "width": offx,
        "height": offy,
        "mon": monitor_num,
    }
    img  = mss.mss().grab(monitor)
    img = np.array(img)

    get_own_color()

    if img.size > 0:

        draw_pattern(img, offx, offy)
        cv2.imshow("preview", img)

        while cv2.getTrackbarPos("Off->On", "Sliders") == 1:
            if cv2.getTrackbarPos("calc", "Sliders") == 1:
                try:
                    mon = mss.mss().monitors[monitor_num]
                    monitor = {
                        "top": mon["top"] + y,
                        "left": mon["left"] + x,
                        "width": offx,
                        "height": offy,
                        "mon": monitor_num,
                    }
                    img  = mss.mss().grab(monitor) # grabs image from selected monitor
                    img = np.array(img)

                    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) # RGB to BGR  | If I didn't add that,
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # BGR to RGB  | it doesn't work. Idk

                    draw_pattern(img, offx, offy)

                    findFigures(img)

                    get_figure_field()

                    if own_color == "W": # sends the figures to the stackfish ai, to check the best move
                        start, end = chess_ai.get_best_move(white_figures_pos, black_figures_pos)
                    else:
                        start, end = chess_ai.get_best_move(black_figures_pos, white_figures_pos)

                    draw_arrow(img, fields[start], fields[end])

                    cv2.imshow("preview", img)

                    cv2.setTrackbarPos("calc", "Sliders", 0)

                except Exception as e:
                    print(f"] ERROR: {e}")

                    cv2.putText(img, "ERROR", (10,30), cv2.QT_FONT_NORMAL, thickness=3, color= (0, 0, 255), fontScale=0.7)

                    cv2.imshow("preview", img)

                    cv2.setTrackbarPos("calc", "Sliders", 0)
            
            cv2.waitKey(10)

    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()
