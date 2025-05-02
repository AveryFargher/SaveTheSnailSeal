"""
Avery Fargher and Ally Daigle
bfargher@uvm.edu, avdaigle@uvm.edu
CS 1210
TrapTheCat-Like Game
"""

import turtle
import random
import math

#--------------------------------------------------------------------------------------------------------------constants

#Radius is for the clickable area of spots
RADIUS = 17

#Spot gaps are to space out the spots that make up the board
SPOT_GAP_X = 40
SPOT_GAP_Y = 30

#--------------------------------------------------------------------------------------------------------------variables

#width and height are the dimensions of the board
width = 12
height = 15
padding = 20
score_padding = 60
score_color = "magenta"

#--------------------------------------------------------------------------------------------------------------functions


#initializes or re-initializes the game
def start_game():
    global spots, cat, cat_spot, cat_origin, score, spots_blocked, screen_height, game_over
    spots_blocked = 0 
    game_over = False
    turtle.clearscreen()

    turtle.addshape("hex.gif")
    turtle.addshape("hexBlocked.gif")
    turtle.addshape("mudSeal1.gif")
    turtle.addshape("mudSeal2.gif")
    turtle.addshape("mudSeal3.gif")
    turtle.addshape("mudSeal4.gif")
    turtle.addshape("mudSeal5.gif")
    turtle.addshape("mudSeal6.gif")
    turtle.onscreenclick(block_spot)

    spots = create_board(width, height)

    cat = turtle.Turtle()
    cat.shape("mudSeal1.gif")
    cat.penup()

    origin_offset = random.randint(-2, 2)
    cat_origin = spots[int(height/2) + origin_offset][int(width/2 + origin_offset)]
    cat_spot = cat_origin
    cat.goto(cat_spot[0].pos())

    score = turtle.Turtle()
    score.hideturtle()
    score.penup()
    score.color(score_color)
    score.goto(0, ((.5 * screen_height) - score_padding))
    score.write(f"Spots blocked: {spots_blocked}", align="center", font=("Times New Roman", 20))

    screen.update()
    screen.tracer(1)

#creates the board and a list of the spots with relevant info about the spot-states
def create_board(width, height):
    global screen, screen_height
    screen = turtle.Screen()
    screen.bgpic("bg.gif")
    screen_width = (width + .8) * SPOT_GAP_X + 2 * padding
    screen_height = (height + 2.2) * SPOT_GAP_Y + 2 * padding
    screen.setup(width=screen_width, height=screen_height)
    screen.tracer(0)

    #A list containing the rows of spots in the grid
    spots = []

    for y in range(height):

        #makes a new row of spots
        spots_row = []

        for x in range(width):
            #for each new spot, makes edge true if it's an edge spot, if cat makes it to an edge spot you lose
            edge = False
            if x in [0, width-1] or y in [0, height-1]:
                edge = True

            #creates the turtle for the spot and sends it to the proper coordinates based on its x and y 
            spot = turtle.Turtle()
            spot.shape("hex.gif")
            spot.penup()
            x_origin = -(.5 * screen_width) + (.5 * SPOT_GAP_X) + padding
            y_origin = -(.5 * screen_height) + (1.5 * SPOT_GAP_Y) + padding
            x_offset = y % 2 * .5 * SPOT_GAP_X
            spot.goto(x_origin + ((x) * SPOT_GAP_X) + x_offset, y_origin + ((y) * SPOT_GAP_Y))

            ''' each spot is a list containing 
                0: The actual spot (turtle)
                1: Whether it's an edge or not (boolean)
                2: Whether it's blocked or not (boolean)
                3: its x coordinate in the grid
                4: its y coordinate in the grid '''
            
            #adds the new spot to the row of spots
            spots_row.append([spot, edge, False, x, y])

            #hides the edges
            if edge:
                spot.hideturtle()

        #adds the row of spots to the list spots
        spots.append(spots_row)
    return spots

'''Blocks the spot clicked on by the user (if it's not already blocked, an edge, or where the cat currently is), 
changing its appearance and rendering it inacessible to the cat. Then, after the player's turn, it calls the 
cat_move function.
'''
def block_spot(x, y):
    global cat_spot, spots_blocked, game_over

    if game_over == "win" or game_over == "loss":
        return 

    for row in spots:
        for spot in row:
            distance = math.sqrt((spot[0].xcor() - x) ** 2 + (spot[0].ycor() - y) ** 2)
            if distance < RADIUS and spot[1] == False and spot[2] == False and spot != cat_spot:
                spot[0].shape("hexBlocked.gif")
                spot[2] = True
                spots_blocked += 1
                score.clear()
                score.write(f"Spots blocked: {spots_blocked}", align="center", font=("Times New Roman", 20))
                screen.update()
                cat_spot = cat_move(cat_spot)
                screen.update()

#attempts to move the cat to a new spot and updates cat_spot (the current spot of the cat)
def cat_move(cat_spot):
    next_spot = choose_spot(adjacent_spots(cat_spot))

    if game_over == "loss":
        angle = cat.towards(next_spot[0])
        cat.setheading(angle)
        cat.shape(f"mudSeal{int((angle // 56) + 1)}.gif")
        cat.goto(next_spot[0].pos())

        screen.tracer(1)
        cat.forward(1000)
        score.clear()
        score.write("you lost D: click to restart, q to quit", align="center", font=("Times New Roman", 20))
        screen.onscreenclick(lambda x, y: start_game())
        turtle.listen()
        turtle.onkeypress(turtle.bye, "q")
        return next_spot

    if game_over == "win":
        score.clear()
        score.write(f"you won in {spots_blocked} turns :D click to restart, q to quit", align="center", font=("Times New Roman", 20))
        screen.onscreenclick(lambda x, y: start_game())
        turtle.listen()
        turtle.onkeypress(turtle.bye, "q")
        return next_spot

    # Normal movement
    angle = cat.towards(next_spot[0])
    cat.setheading(angle)
    cat.shape(f"mudSeal{int((angle // 56) + 1)}.gif")
    cat.goto(next_spot[0].pos())

    return next_spot

#returns a list of spots adjacent to a spot
def adjacent_spots(spot):
    
    #gets the x and y coordinate of the spot from its list
    y = spot[4]
    x = spot[3]

    adjacent_spots = []

    #Adjacent spots are determined by whether the y coordinate is odd or even
    offset = 2 * (y % 2) - 1


    adjacent_spots.append(spots[y][x-1])
    adjacent_spots.append(spots[y][x+1])
    adjacent_spots.append(spots[y+1][x + offset])
    adjacent_spots.append(spots[y+1][x])
    adjacent_spots.append(spots[y-1][x + offset])
    adjacent_spots.append(spots[y-1][x])

    
    return adjacent_spots

#chooses a spot for the cat to move to out of all adjacent spots
def choose_spot(adjacent_spots):
    global game_over
    possible_spots = []
    for spot in adjacent_spots:

        #if the spot is an edge (spot[1] is true), the cat will immediately pick it
        if spot[1]:
            game_over = "loss"
            return spot
        
        #adds spot to the list of possible spots if it's not blocked (spot[2] is false)
        elif spot[2] == False:
            possible_spots.append(spot)
    return best_spot(possible_spots)

'''if there are multiple possible spots and no edges for the cat to escape to,
this function determines the best spot out of all possible spots for the cat to move to'''

def best_spot(possible_spots):
    global game_over

    goodness_dict = {}
    highest_goodness = 0

    for i in range(100):
        goodness_dict[i] = []

    if possible_spots:
        for spot in possible_spots:
            goodness = spot_goodness(adjacent_spots(spot))
            goodness_dict[goodness].append(spot)
    
        for goodness in goodness_dict:
            if goodness_dict[goodness]:
                highest_goodness = goodness

        return random.choice(goodness_dict[highest_goodness])
    
    game_over = "win"

def spot_goodness(adjacent_spots):
    global cat_origin

    goodness = 0
    for spot in adjacent_spots:

        distance_from_origin = int(math.sqrt((spot[3] - cat_origin[3]) ** 2 + (spot[4] - cat_origin[4]) ** 2))
        if spot[1]:
            goodness += 10
        elif not spot[2]:
            goodness += distance_from_origin
    return goodness

#calls the function block_spot when the user clicks on the screen
turtle.onscreenclick(block_spot)

#--------------------------------------------------------------------------------------------------------------game loop
if __name__ == "__main__":
    start_game()
    turtle.mainloop()
    
