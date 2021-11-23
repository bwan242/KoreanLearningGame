import pygame as pg
import math
import sys

# 1000x800 canvas
width = 1000
height = 800

# set up scree
screen = pg.display.set_mode((width, height))

# default, main menu
gamemode = 0

question_counter = 0

# sets title of window
pg.display.set_caption("Korean Learning Game")

# stores data for the player
class Player:
    def __init__(self, name, grammar, vocabulary):
        self.name = name
        self.grammar = grammar
        self.vocabulary = vocabulary

    # string representation of a Player's stats
    def __str__(self):
        return self.name + " " + str(self.grammar) + " " + str(self.vocabulary)

    # resets a players stat's back to 0 for the next game
    def reset(self):
        self.grammar = 0
        self.vocabulary = 0

    # takes input, sets the vocab score to that number
    def set_vocab_score(self, num):
        self.vocabulary = num

    # takes input, sets the grammar score to that number
    def set_grammar_score(self, num):
        self.grammar = num

# stores question data
class Question:
    # text is string, answers is a list of strings
    def __init__(self, prompt, choices, correct_ans,q_type):
        self.prompt = prompt
        self.choices = choices # ans choices
        self.correct_ans = correct_ans # index of right answer
        self.q_type = q_type #vocab or grammar question

# draws the text and button of the main menu
def draw_main_menu():
    #print("loading main menu")
    pg.font.init()
    font = pg.font.Font("2615-UnBatang_0613.ttf", 45)

    # load the picture
    image = pg.image.load("Background.jpg")

    # image, horizontal_flip, vertical_flip
    image = pg.transform.flip(image, True, True)

    # scale the image so it fits the width/height
    image = pg.transform.scale(image, (width, height))

    # put the image on the scream
    screen.blit(image, (0, 0))

    #background rectangle for title text
    pg.draw.rect(screen, (128, 128, 128), (275, 25, 500, 100))

    # title text
    text = font.render("Korean Learning Game", 1, (0, 100, 0))
    screen.blit(text, (300, 50))

    pg.draw.rect(screen, (255, 255, 255), (20, 680, 300, 100))

    # creator name
    text = font.render("Brandon Wan", 1, (0, 0, 200))
    screen.blit(text, (25, 680))

    # class name
    text = font.render("CSE 323", 1, (0, 0, 200))
    screen.blit(text, (25, 725))

    # start button
    rect = pg.draw.rect(screen, (128, 128, 128), (325, 575, 400, 100))

    if rect.collidepoint(pg.mouse.get_pos()):
        rect = pg.draw.rect(screen, (255, 0, 0), (325, 575, 400, 100))

    text = font.render("Start/시작하기", 1, (0, 100, 0))
    screen.blit(text, (375, 600))

# handles events that occur while in the main menu
def handle_menu():
    global gamemode

    mouse_pos = pg.mouse.get_pos()

    start_rect = pg.draw.rect(screen, (128, 128, 128), (325, 575, 400, 100))

    if start_rect.collidepoint(mouse_pos):
        gamemode = 1

# handles events that occur during a question
def handle_question(question_list, player):
    global question_counter
    global gamemode

    # perform check to see if we can keep asking questions
    if question_counter < len(question_list):

        # make list of buttons
        btn_list = []
        btn_list.append((pg.draw.circle(screen, (0, 0, 200), (150, 675), 75), 0))
        btn_list.append((pg.draw.circle(screen, (0, 0, 200), (350, 675), 75), 1))
        btn_list.append((pg.draw.circle(screen, (0, 0, 200), (550, 675), 75), 2))
        btn_list.append((pg.draw.circle(screen, (0, 0, 200), (750, 675), 75), 3))

        # get mouse coordinates
        mouse_pos = pg.mouse.get_pos()

        for b in btn_list:
            # if mouse is on the circular button
            if distance(mouse_pos, b[0].center) <= 75:
                # if the question mode is still going o
                    # the question being asked right now
                    q = question_list[question_counter]

                    # if the user selects the button corresponding to the correct answer
                    if b[1] == q.correct_ans:
                        print("correct!")
                        if q.q_type == "v":
                            player.set_vocab_score(player.vocabulary + 1)
                        elif q.q_type == "g":
                            player.set_grammar_score(player.grammar + 1)

                    print(player)
                    question_counter += 1


# draws the buttons, text for the end of the game
def draw_end_game(player):

    #print("loading end menu")
    pg.font.init()
    font = pg.font.Font("2615-UnBatang_0613.ttf", 100)

    # load jeju picture
    image = pg.image.load("jeju_beach.jpg")

    # image, horizontal_flip, vertical_flip
    #image = pg.transform.flip(image, True, True)

    # scale the image so it fits the width/height
    image = pg.transform.scale(image, (width, height))

    # put the image on the scream
    screen.blit(image, (0, 0))

    text = font.render("잘했어요!!", 1, (0, 100, 0))
    screen.blit(text, (300, 50))

    play_again_btn = pg.draw.rect(screen, (128, 128, 128), (275, 650, 500, 125))

    if play_again_btn.collidepoint(pg.mouse.get_pos()):
        play_again_btn = pg.draw.rect(screen, (255, 0, 0), (275, 650, 500, 125))

    # display ending message string
    end_msg = [player.name,
               "Vocab Score: " + str(player.vocabulary) + "/10",
               "Grammar Score: " + str(player.grammar) + "/5"]

    text_y = 200
    text_x = 100
    i = 0

    # render the ending player msg
    while i < len(end_msg):
        text = font.render(end_msg[i], 1, (250, 200, 200))
        screen.blit(text, (text_x, text_y))
        text_y += 100
        i += 1

    text = font.render("Play Again", 1, (0, 100, 0))
    screen.blit(text, (300, 650))


    # the player will receive feedback on their performance
    feedback = ""

    # perfect score
    if player.grammar == 5 and player.vocabulary == 10:
        feedback = "Perfect!"
    else:
        # good score on both
        if player.grammar > 3 and player.vocabulary > 7:
            feedback = "Great job! Try to get a perfect score next time"
        else:
            feedback = "Areas to improve on: "

            # poor grammar
            if player.grammar < 3:
                feedback += " grammar"

                # poor grammar and vocabulary
                if player.vocabulary < 7:
                    feedback += ", vocabulary"

            # poor performance on both
            if player.vocabulary < 7 and player.grammar > 3:
                feedback += "vocabulary"

    # render the feedback, in a smaller font
    font = pg.font.Font("2615-UnBatang_0613.ttf", 50)
    text = font.render(feedback, 1, (0, 0, 100))
    screen.blit(text, (50, 550))

# deal with events that occur at the end of the game
def handle_end_game(player):
    mouse_pos = pg.mouse.get_pos()
    global gamemode
    global question_counter

    # back to main menu button
    rect = pg.draw.rect(screen, (128, 128, 128), (275, 650, 500, 125))

    if rect.collidepoint(mouse_pos):
        gamemode = 0
        question_counter = 0
        player.reset()

# calculate 2D distance between two points
def distance(p1, p2):
    x1, x2 = p1[0], p2[0]
    y1, y2 = p1[1], p2[1]

    return math.sqrt((x2 - x1)**2 + (y2-y1)**2)

# read through each line
# parse the data into a prompt, questions, and the right answer
def import_questions(filename):
    questions = []

    f = open(filename, "r", encoding="utf-8")

    line = f.readline()

    # process questions
    while line:
        data = line.split(",") # parse the question into parts
        prompt = data[0]
        choices = data[1:5]
        correct_ans = int(data[5])
        q_type = data[6].strip()

        ques = Question(prompt, choices, correct_ans,q_type)
        questions.append(ques)

        line = f.readline()

    # close text file after reading
    f.close()
    print("Questions imported..")

    return questions

def draw_question(ques):
    global question_counter

    # debug
    # print("drawing question", question_counter)

    # Korean font downloaded from unifont.org
    pg.font.init()
    font = pg.font.Font("2615-UnBatang_0613.ttf", 45)

    # draw prompt
    text = font.render(ques.prompt, 1, (0, 100, 0))
    screen.blit(text, (300, 50))

    # draw choices
    ans1 = font.render("1) " + ques.choices[0], 1, (100,0,0))
    screen.blit(ans1, (50,200))

    ans2 = font.render("2) " + ques.choices[1], 1, (100, 0,0))
    screen.blit(ans2, (50, 300))

    ans3 = font.render("3) " + ques.choices[2], 1, (100, 0, 0))
    screen.blit(ans3, (50, 400))

    ans4 = font.render("4) " + ques.choices[3], 1, (100, 0, 0))
    screen.blit(ans4, (50, 500))

    # draw buttons
    mouse_pos = pg.mouse.get_pos()

    # button1
    radius = 75
    if distance(mouse_pos, (150, 675)) <= radius:
        pg.draw.circle(screen, (0, 0, 200), (150, 675), 75)
    else:
        pg.draw.circle(screen, (128, 128, 128), (150, 675), 75)
    btn1 = font.render("1", 1, (100, 0, 0))
    screen.blit(btn1, (140, 645))

    # button 2
    if distance(mouse_pos, (350, 675)) <= radius:
        pg.draw.circle(screen, (0, 0, 200), (350, 675), 75)
    else:
        pg.draw.circle(screen, (128, 128, 128), (350, 675), 75)
    btn2 = font.render("2", 1, (100, 0, 0))
    screen.blit(btn2, (340, 645))

    # button 3
    if distance(mouse_pos, (550, 675)) <= radius:
        pg.draw.circle(screen, (0, 0, 200), (550, 675), 75)
    else:
        pg.draw.circle(screen, (128, 128, 128), (550, 675), 75)
    btn3 = font.render("3", 1, (100, 0, 0))
    screen.blit(btn3, (540, 645))

    # button 4
    if distance(mouse_pos, (750, 675)) <= radius:
        pg.draw.circle(screen, (0, 0, 200), (750, 675), 75)
    else:
        pg.draw.circle(screen, (128, 128, 128), (750, 675), 75)
    btn4 = font.render("4", 1, (100, 0, 0))
    screen.blit(btn4, (740, 645))

def redraw_window(window, player, questions):
    global gamemode
    screen.fill((255, 255, 255))

    if question_counter == len(questions):
        gamemode = 2

    if gamemode == 0:
        draw_main_menu()
    elif gamemode == 1:
        draw_question(questions[question_counter])
    elif gamemode == 2:
        draw_end_game(player)

    pg.display.update()

def main():
    global question_counter
    questions = import_questions("questions.txt")

    continue_game = True

    print("initializing player")
    player1 = Player("Player1", 0, 0)
    clock = pg.time.Clock()

    while continue_game:
        clock.tick(15)

        for game_event in pg.event.get():
            if game_event.type == pg.QUIT:
                run = False
                pg.quit()
                print("Ending game..")
                sys.exit()
            if game_event.type == pg.MOUSEBUTTONDOWN:
                if gamemode == 0:
                    handle_menu()
                elif gamemode == 1:
                    handle_question(questions, player1)
                elif gamemode == 2:
                    handle_end_game(player1)

        redraw_window(screen, player1, questions)

main()