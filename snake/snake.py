import pygame, sys, random
import math

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

size = width, height = 600, 600
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Snake')

GREENBLOCKSIDE = 15
SPEEDINCREASE = 0.05 #Speed increased when the snake eats the apple

class GreenBlock():

    def __init__(self, positionX, positionY, speed, direction):
        self.COLOR = GREEN
        self.SIDE = GREENBLOCKSIDE
        self.position = {"x": positionX, "y": positionY}
        self.speedXY = {"speedX": speed["speedX"], "speedY": speed["speedY"]}
        self.direction = direction
        self.directionChange = []  # Store the direction changes
        self.directionChangeCounter = []  # Counter that determines when to change direction

    def setDirection(self, direction, speed):
        if direction == "UP":
            if self.direction != "DOWN":  # It wont be possible to move the snake down while it's been moving up
                self.direction = direction
                self.speedXY["speedX"], self.speedXY["speedY"] = 0, -speed

        elif direction == "DOWN":
            if self.direction != "UP":
                self.direction = direction
                self.speedXY["speedX"], self.speedXY["speedY"] = 0, speed

        elif direction == "RIGHT":
            if self.direction != "LEFT":
                self.direction = direction
                self.speedXY["speedX"], self.speedXY["speedY"] = speed, 0

        elif direction == "LEFT":
            if self.direction != "RIGHT":
                self.direction = direction
                self.speedXY["speedX"], self.speedXY["speedY"] = -speed, 0

        else:
            raise Exception("Invalid direction!")

        if direction == self.direction:  # direction changed
            if len(self.directionChangeCounter) == 0:
                self.directionChangeCounter.append(0)

            self.directionChange.append(direction)
            self.directionChangeCounter.append(0)

    def increaseSpeed(self, speed):
        if self.direction == "UP": self.speedXY['speedY'] -= speed
        elif self.direction == "DOWN": self.speedXY['speedY'] += speed
        elif self.direction == "LEFT": self.speedXY['speedX'] -= speed
        else: self.speedXY['speedX'] += speed

    def draw(self):
        pygame.draw.rect(screen, self.COLOR, (self.position["x"], self.position["y"], self.SIDE, self.SIDE))


class Snake():
    def __init__(self):
        self.size = 1
        self.speed = 0.2
        self.position = {"x": 50, "y": 50}
        # Snake is created by default moving to down and speed = 0.5
        self.blockList = [GreenBlock(self.position["x"], self.position["y"], {"speedX": 0, "speedY": self.speed}, "DOWN")]

    def addBlock(self):
        lastBlock = self.blockList[-1]
        #Cleaning direction changes from the last block
        lastBlock.directionChange = []
        lastBlock.directionChangeCounter = []
        newBlock = GreenBlock(lastBlock.position["x"], lastBlock.position["y"], lastBlock.speedXY, lastBlock.direction)
        # newBlock.setDirection(lastBlock.direction, self.speed)

        if lastBlock.direction == "UP":
            newBlock.position["y"] += newBlock.SIDE

        elif lastBlock.direction == "DOWN":
            newBlock.position["y"] -= newBlock.SIDE

        elif lastBlock.direction == "LEFT":
            newBlock.position["x"] += newBlock.SIDE

        else:
            newBlock.position["x"] -= newBlock.SIDE

        self.blockList.append(newBlock)

    def setDirection(self, direction):
        self.blockList[0].setDirection(direction,
                                       self.speed)  # Setting the first block of the snake will set the snake's direction

    def move(self):
        for i in range(0, len(self.blockList)):
            if i == 0:
                pass

            else:
                lastBlock = self.blockList[i - 1]
                lastBlockChanges = len(lastBlock.directionChange)
                # print("Bloco " + str(i) + " " + str(lastBlock.directionChangeCounter))
                if lastBlockChanges > 0:
                    lastBlock.directionChangeCounter[0] += 1

                    try:
                        lastBlock.directionChangeCounter[lastBlockChanges] += 1
                    except:
                        pass

                    if lastBlock.directionChangeCounter[0] >= lastBlock.SIDE / self.speed:
                        self.blockList[i].setDirection(lastBlock.directionChange[0], self.speed)
                        lastBlock.directionChangeCounter.pop(0)
                        lastBlock.directionChange.pop(0)

                        if len(lastBlock.directionChangeCounter) > 0 and lastBlock.directionChangeCounter[0] >= 0:
                            lastBlock.directionChangeCounter[0] = (lastBlock.SIDE / self.speed) - \
                                                                  lastBlock.directionChangeCounter[0]
                            if lastBlock.directionChangeCounter[0] <= 0:
                                lastBlock.directionChangeCounter.pop(0)

                else:
                    if lastBlock.direction == "UP" or lastBlock.direction == "DOWN":
                        self.blockList[i].position["x"] = lastBlock.position["x"]

                    else:
                        self.blockList[i].position["y"] = lastBlock.position["y"]

            self.blockList[i].position["x"] += self.blockList[i].speedXY["speedX"]
            self.blockList[i].position["y"] += self.blockList[i].speedXY["speedY"]

            self.blockList[i].position["x"] = round(self.blockList[i].position["x"], 2)
            self.blockList[i].position["y"] = round(self.blockList[i].position["y"], 2)

    def increaseSpeed(self):
        self.speed += SPEEDINCREASE
        # Updating speed of blocks
        for block in self.blockList: block.increaseSpeed(SPEEDINCREASE)

    def draw(self):
        self.move()
        for block in self.blockList:
            block.draw()


class Apple():
    def __init__(self):
        self.color = RED
        self.active = True
        self.size = 50
        self.position = {"x": random.randint(0, width - self.size),
                         "y": random.randint(0, height - self.size)}
        apple_image = pygame.image.load('../image/apple.png')
        apple_image = pygame.transform.scale(apple_image, (self.size, self.size))
        apple_rect = apple_image.get_rect()
        apple_rect.center = (self.position["x"], self.position["y"])
        screen.blit(apple_image, apple_rect)
        self.appleRect = pygame.Rect(self.position["x"], self.position["y"], self.size, self.size)

    def draw(self):
        apple_image = pygame.image.load('../image/apple.png')
        apple_image = pygame.transform.scale(apple_image, (self.size, self.size))
        apple_rect = apple_image.get_rect()
        apple_rect.center = (self.position["x"] + self.size / 2, self.position["y"] + self.size / 2)
        screen.blit(apple_image, apple_rect)


def checkAppleCollision(apple, snake):
    appleRect = pygame.Rect(apple.position['x'], apple.position['y'], apple.size, apple.size)
    snakeHead = pygame.Rect(snake.blockList[0].position['x'], snake.blockList[0].position['y'], snake.blockList[0].SIDE,
                            snake.blockList[0].SIDE)
    return pygame.Rect.colliderect(appleRect, snakeHead)


def checkSnakeCollision(snake):
    head = pygame.Rect(snake.blockList[0].position['x'], snake.blockList[0].position['y'], snake.blockList[0].SIDE / 2,
                       snake.blockList[0].SIDE / 2)

    for i in range(1, len(snake.blockList)):
        blockRect = pygame.Rect(snake.blockList[i].position['x'], snake.blockList[i].position['y'],
                                snake.blockList[i].SIDE / 2, snake.blockList[i].SIDE / 2)

        if i == 1:
            pass

        elif pygame.Rect.colliderect(head, blockRect):
            return pygame.Rect.colliderect(head, blockRect)

    return False


def checkWallCollision(snake):
    head = snake.blockList[0]
    headX, headY = head.position['x'], head.position['y']

    if headX < 0 or headY < 0:
        return True
    if (headX + head.SIDE) > width or (headY + head.SIDE) > height:
        return True

    return False


def checkGameOver(snake):
    return checkSnakeCollision(snake) or checkWallCollision(snake)


def gameOver(snake):
    # print GAME OVER
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    textsurface = myfont.render('GAME OVER', False, (255, 0, 0))
    # Centering the text
    screen.blit(textsurface, ((width / 2 - 3 * 30), (height / 2 - 3 * 30)))
    for block in snake.blockList:
        block.COLOR = RED

    snake.draw()


snake = Snake()
apple = Apple()

while 1:
    screen.fill(WHITE)
    snake.draw()
    apple.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: sys.exit()
            if event.key == pygame.K_UP: snake.setDirection("UP")
            if event.key == pygame.K_DOWN: snake.setDirection("DOWN")
            if event.key == pygame.K_LEFT: snake.setDirection("LEFT")
            if event.key == pygame.K_RIGHT: snake.setDirection("RIGHT")

    if not apple.active:
        apple = Apple()

    # Checking if the snake has eaten the apple
    appleCollision = checkAppleCollision(apple, snake)
    if appleCollision:
        apple.active = False
        snake.increaseSpeed()
        snake.addBlock()

    # Checking gameOver
    if checkGameOver(snake):
        gameOver(snake)
        pygame.display.update()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

    pygame.display.update()