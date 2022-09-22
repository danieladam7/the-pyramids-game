import time
import random
import pygame

# GENERAL INSTRUCTIONS
# use only these 3 libraries and nothing else!!
# don't use OOP
# for coding use only: conditions, loops, functions, strings, lists and arrays


pygame.font.init()


###         global vars and constants           ###
display_HEIGHT = 500
display_WIDTH = 500
CELL_SIZE = 40
matrix_height = 5 * CELL_SIZE # 40 * 5 cells = 200
matrix_width = 9 * CELL_SIZE   # 40 * 9 cells = 360

# start point of matrix on display
top_left_x = (display_HEIGHT-matrix_width)//2
top_left_y = (display_HEIGHT-matrix_height)//2



###         define colors           ###
PINK = (255, 192, 203)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
CELL_COLORS = [PINK, YELLOW, BLUE]
# Background and lines
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# limit to 60 frames per second
FPS = 60



display = pygame.display.set_mode((display_WIDTH, display_HEIGHT))
pygame.display.set_caption('The Pyramids Game')
nitzanim_logo = pygame.image.load("Nitzanim_logo.png")



###         draw functions          ###

def draw_display(matrix):
    display.fill(WHITE)
    display.blit(nitzanim_logo, (0, 10))
    draw_matrix(matrix)
    draw_matrix_frame()
    draw_pyramid_frame()
    pygame.display.update()

def draw_timeout(text, size, color):
    font = pygame.font.SysFont('ariel', size, bold=False)
    label = font.render(text, 1, color)
    display.blit(label, (top_left_x + 90, top_left_y + 90))
    pygame.display.update()

def draw_not_succeded(text, size, color):
    font = pygame.font.SysFont('arial', size, bold=False)
    label = font.render(text, 1, color)
    display.blit(label, (top_left_x + 20, top_left_y + matrix_height + 30))
    pygame.display.update()

def draw_succeded(text, size, color):
    font = pygame.font.SysFont('arial', size, bold=False)
    label = font.render(text, 1, color)
    display.blit(label, (top_left_x + 5, top_left_y + matrix_height + 30))
    pygame.display.update()

def draw_goodbye(text, size, color):
    font = pygame.font.SysFont('arial', size, bold=False)
    label = font.render(text, 1, color)
    display.blit(label, (top_left_x + 135, top_left_y + matrix_height + 80))
    pygame.display.update()

def draw_welcome(text, size, color):
    font_welcome = pygame.font.SysFont('arial', size, bold=False)
    welcome = font_welcome.render(text, 1, color)
    display.blit(welcome, (top_left_x + 35, top_left_y + matrix_height + 30))
    pygame.display.update()

def draw_game_start(text, size, color):
    font_pyramid = pygame.font.SysFont('arial', size, bold=False)
    pyramid_to_solve = font_pyramid.render(text, 1, color)
    display.blit(pyramid_to_solve, (top_left_x + 70, top_left_y + matrix_height + 75))
    pygame.display.update()

def draw_matrix(matrix):
    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            if within_pyramid(row, column):
                pygame.draw.rect(display, matrix[row][column], (top_left_x + column * CELL_SIZE,
                                                               top_left_y + row * CELL_SIZE , 40, 40), 0)
            else:
                pygame.draw.rect(display, WHITE, (top_left_x + column * CELL_SIZE ,
                                                 top_left_y + row * CELL_SIZE, 40, 40), 0)

    pygame.display.update()

def draw_matrix_frame():
    # draw outerline for matrix
    pygame.draw.lines(display, BLACK, True, ((top_left_x, top_left_y), (top_left_x + matrix_width, top_left_y),
                                            (top_left_x + matrix_width, top_left_y + matrix_height),
                                            (top_left_x, top_left_y + matrix_height)), 4)
    pygame.display.update()

def draw_pyramid_frame():
    # draw innerlines around pyramid
    #start: (top_left_x + 0 * Cell, top_left_y+ 4 * Cell) -> (top_x + 1*CELL_SIZE, top_y + 4*Cell) ...
    # for right horizontal use same coordinates and add distance to x to reach right side
    j = 8
    for i in range(5):
        # draw left horizontal lines for frame
        pygame.draw.lines(display, BLACK, False, ((top_left_x + (i)*CELL_SIZE, top_left_y + (4-i)*CELL_SIZE),
                                                 (top_left_x + (i+1)*CELL_SIZE, top_left_y + (4-i)*CELL_SIZE)), 2)

        # draw right horizontal lines for frame
        pygame.draw.lines(display, BLACK, False, ((top_left_x + (j-i)*CELL_SIZE, top_left_y + (4 - i) * CELL_SIZE),
                                                 (top_left_x + (j-i+1)*CELL_SIZE, top_left_y + (4 - i) * CELL_SIZE)),2)
    j = 9
    for i in range(1,5):
        #draw left vertical lines for frame
        pygame.draw.lines(display, BLACK, False, ((top_left_x + i * CELL_SIZE, top_left_y + (5-i) * CELL_SIZE),
                                                 (top_left_x + i * CELL_SIZE, top_left_y + (4 - i) * CELL_SIZE)), 2)
        # draw right vertical lines for frame
        pygame.draw.lines(display, BLACK, False, ((top_left_x + (j-i) * CELL_SIZE, top_left_y + (5 - i) * CELL_SIZE),
                                                 (top_left_x + (j-i) * CELL_SIZE, top_left_y + (4 - i) * CELL_SIZE)), 2)
    pygame.display.update()

    
    
###         game handling functions          ###

def create_matrix():
      matrix = [[0 for _ in range(9)] for _ in range(5)]
      matrix[0][4] = 1
      row = 1
      col = 4
      while col-row >=0 and col+row <len(matrix[row]):
          matrix[row][col] = 1
          matrix[row][col-1] = 1
          matrix[row][col+1] = 1
          row+=1
      color_matrix(matrix)
      return matrix


def color_matrix(matrix):
    for row in range(5):
        for column in range(9):
            if not within_pyramid(row, column):
                matrix[row][column] = WHITE
            else:
                matrix[row][column] = randomize_color()

def randomize_color():
    return random.choice(CELL_COLORS)

def within_pyramid(row, column):
    if row == 4:
        return True
    elif row == 3 and column in range(1,8):
        return True
    elif row == 2 and column in range(2,7):
        return True
    elif row == 1 and column in range(3, 6):
        return True
    elif row == 0 and column == 4:
        return True
    else: return False




###         game rules          ###
# 1. blue can't be on borders of pyramid. if blue cell at border -> randomize new color for that cell
# 2. pink can't be around blue cell except diagonalized - > randomize  new color for the !!pink!! cell
# 3. if row has are more than 4 yellow cells -> randomize new colors for whole row


def all_rules_valid(matrix):
    return rule1_valid(matrix) and rule2_valid(matrix) and rule3_valid(matrix)

def verify_rules(matrix):
    verify_rule1(matrix)
    verify_rule2(matrix)
    verify_rule3(matrix)

# around rule 1
def rule1_valid(matrix):
    matrix_center = (len(matrix))-1
    for row in range(len(matrix)):
        # for last row check all cells
        if row == len(matrix)-1:
            for cell in range(len(matrix[row])):
                if matrix[row][cell] == BLUE:
                    return False
        else:
            if matrix[row][matrix_center -row] == BLUE or matrix[row][matrix_center +row] == BLUE:
                return False
    return True

def verify_rule1(matrix):
    # pyramid_border_indexes = [(0,4), (1,3), (1,5), (2,2), (2,6), (3,1), (3,7), whole 4th row]
    matrix_center = (len(matrix))-1
    for row in range(len(matrix)):
        # for last row check all cells
        if row == len(matrix) - 1:
            for cell in range(len(matrix[row])):
                if matrix[row][cell] == BLUE:
                    matrix[row][cell] = randomize_color()
        else:
            if matrix[row][matrix_center-row] == BLUE:
                matrix[row][matrix_center-row] = randomize_color()
            elif matrix[row][matrix_center+row] == BLUE:
                matrix[row][matrix_center +row] = randomize_color()

# around rule 2
def rule2_valid(matrix):
    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            # check if cell is pink
            if matrix[row][column] == PINK:
                # check if pink cell has blue neighbour
                if cell_has_blue_neighbour(matrix, row, column):
                    return False
    return True

def verify_rule2(matrix):
    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            # check if cell is pink
            if matrix[row][column] == PINK:
                # check if pink cell has blue neighbour
                if cell_has_blue_neighbour(matrix, row, column):
                    recolor_Pink_cell(matrix, row, column)

def cell_has_blue_neighbour(matrix, row, column):
    row_neighbours = [row-1, row+1] # upper and lower neighbours
    column_neighbours = [column-1, column+1]# left and right neighbours
    for row_ng in row_neighbours:
        if row_ng in range(len(matrix)):
            if matrix[row_ng][column] == BLUE:
                return True
    for col_ng in column_neighbours:
        if col_ng in range(len(matrix[row])):
            if matrix[row][col_ng] == BLUE:
                return True
    return False

def recolor_Pink_cell(matrix, row, column):
    matrix[row][column] = randomize_color()


# around rule 3
def rule3_valid(matrix):
    for row in range(2,len(matrix)):
        yellow_cells_in_row = 0
        for column in range(len(matrix[row])):
            if matrix[row][column] == YELLOW:
                yellow_cells_in_row += 1
                if yellow_cells_in_row > 4:
                    return False
    return True

def verify_rule3(matrix):
    for row in range(2,len(matrix)):
        yellow_cells_ctr = 0
        for column in range(len(matrix[row])):
            if matrix[row][column] == YELLOW:
                yellow_cells_ctr += 1
                if yellow_cells_ctr > 4:
                    recolor_row(matrix, row)

def recolor_row(matrix, row):
    for column in range(len(matrix[row])):
        matrix[row][column] = randomize_color()


###         main menu for game control flow         ###

def main():
    clock = pygame.time.Clock()
    matrix = create_matrix()
    draw_display(matrix)
    draw_welcome('Welcome to the Pyramids Game!', 25, BLACK)
    time.sleep(1) # wait one sec to welcome user
    draw_game_start('Game starts right now!', 25, BLACK)
    time.sleep(1.5) # to display pyramid to solve for a moment
    run = True
    start_ticks = pygame.time.get_ticks()  # start time for timeout. end game after 5 secs

    while run:
        clock.tick(FPS) # 60 frames/sec
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()

        # handling all actions/logics of the game
        while not all_rules_valid(matrix):
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # calculate how many seconds
            timeout = seconds > 5
            if timeout:
                break
            verify_rules(matrix)
            draw_display(matrix)

        if timeout:
            draw_timeout('Timeout!', 60, BLACK)
            draw_not_succeded('Pyramid not succeeded to be solved', 25, BLACK)
            time.sleep(1) # to not display on display both at same time
            draw_goodbye('Goodbye!', 25, BLACK)
            run = False

        else:
            draw_succeded('Great! Pyramid succeeded to be solved', 25, BLACK)
            time.sleep(1) # to not display on display both at same time
            draw_goodbye('Goodbye!', 25, BLACK)
            run = False


        time.sleep(2) # close game after 2 secs


    pygame.quit() # end pygame



###         start game          ###
if __name__ == "__main__":
    main()


