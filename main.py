import random
import pygame

class Cube:

    rows = 20
    w = 500
    def __init__(self, start, dirnx = 1, dirny = 0, color = (255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes = False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis - 2, dis - 2))     # Drawing inside squares

        if eyes:
            center = dis // 2
            radius = 3
            circle_middle = (i*dis+center-radius, j*dis+8)
            circle_middle1 = (i*dis+dis-radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circle_middle, radius)
            pygame.draw.circle(surface, (0,0,0), circle_middle1, radius)


class Snake:

    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        # Keeping track of head at position
        self.head = Cube(pos)
        self.body.append(self.head)
        # Directions for moving snake
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # Holding the key values that can be pressed
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    # Setting key (current head) == where we turned
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                if keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    # Setting key (current head) == where we turned
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                if keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    # Setting key (current head) == where we turned
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                if keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    # Setting key (current head) == where we turned
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]    # position
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                # If on last cube, remove turn
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                # Checking whether we are on edge of screen
                if c.dirnx == -1 and c.pos[0] <= 0:     # if on left side edge, come through right side edge
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:   # if on right side edge, come through left side
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:   # if on down side edge, come through up side edge
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:   # if on up side edge, come through down side edge
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)    # else keep moving

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        # Checking direction of the tail so cube can be added properly
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))      # Right
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))      # Left
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))      # Down
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))      # Up

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def draw_grid(width, rows, surface):
    size_between = width // rows

    x = 0
    y = 0

    for line in range(rows):
        x += size_between
        y += size_between

        # Draw lines for each iteration of loop
        pygame.draw.line(surface, (255,255,255), (x,0), (x, width))  # vertical line
        pygame.draw.line(surface, (255, 255, 255), (0, y), (width, y))  # horizontal line


def redraw_window(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    draw_grid(width, rows, surface)
    pygame.display.update()


def random_snack(rows, item):

    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        # Checking if positions are == current position of snake from a filtered list
        # Making sure the snack will not be inside of current snake
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:   # will continue if (values are == to positions) and
            continue                                                    # greater than 0 using filter and lambda function
        else:
            break

    return (x,y)


def main():
    global width, rows, s, snack
    pygame.init()
    pygame.display.set_caption("Snake")
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    flag = True

    # Starting in the middle
    s = Snake((255, 0, 0), (10, 10))
    snack = Cube(random_snack(rows, s), color = (0,255,0))
    clock = pygame.time.Clock()

    while flag:
        # Delaying the game so it's not as fast
        pygame.time.delay(50)
        clock.tick(10)  # limiting to 10 fps
        s.move()
        if s.body[0].pos == snack.pos:
            s.add_cube()
            snack = Cube(random_snack(rows, s), color = (0,255,0))

        # Checking for the collision
        for i in range(len(s.body)):
            # Using map to apply function lambda (variable z) to each item in s.body list
            if s.body[i].pos in list(map(lambda z:z.pos, s.body[i + 1:])):
                print("Score:", len(s.body))
                flag = False

        redraw_window(win)

    pass

main()

