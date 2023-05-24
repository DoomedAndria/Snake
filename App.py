import pygame
import time
import random
import sys
import os

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

class App:

    def __init__(self):
        self.running = False
        self.clock = None
        self.screen = None
        self.snake = None
        self.background = None
        self.upperMenu = None
        self.space = None
        self.food = None
        self.sound = True
        self.superfood = None
        self.point = 0
        self.rand = 999
        self.superfoodappearence = False
        self.escX = 0
        self.escY = 0
        self.startingscreen = True

    def run(self):
        self.init()
        pygame.mixer.init()
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(os.path.join(base_path, "sounds", "rick.mp3")), -1)
        pygame.mixer.Channel(0).set_volume(0.3)
        while self.running:
            self.update()
            self.render()
        self.cleanUp()

    def init(self):
        self.running = True
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Rick-Snake")
        self.snake = Snake(540, 340, 5)
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load(os.path.join(base_path, "images", "back.png"))
        self.upperMenu = pygame.image.load(os.path.join(base_path, "images", "upperMenu.jpg"))
        self.space = pygame.image.load(os.path.join(base_path, "images", "space.png"))
        self.food = Food()
        self.superfood = superFood()

    def update(self):
        if self.wallCollides() or self.selfCollides():
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(os.path.join(base_path, "sounds", "crash.mp3")))
            time.sleep(4)
            self.running = False

        if self.foodCollides():
            self.rand = random.randint(1, 5)
            pygame.mixer.Channel(2).play(pygame.mixer.Sound(os.path.join(base_path, "sounds", "eating.mp3")))
            self.snake.px.append(self.snake.px[self.snake.length - 1])
            self.snake.py.append(self.snake.py[self.snake.length - 1])
            self.snake.length += 1
            self.food.update()
            for i in range(self.snake.length):
                if self.snake.px[i] == self.food.x and self.snake.py[i] == self.food.y:
                    self.food.update()

        if self.superfoodCollides():
            self.rand = random.randint(1, 4)
            pygame.mixer.Channel(2).play(pygame.mixer.Sound(os.path.join(base_path, "sounds", "eating.mp3")))
            self.superfood.update()
            for i in range(self.snake.length):
                if self.snake.px[i] == self.superfood.x and self.snake.py[i] == self.superfood.y:
                    self.superfood.update()

        self.events()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed(3)[0]:
                    pos = pygame.mouse.get_pos()
                    if self.startingscreen:
                        if 100 <= pos[0] <= 350 and 350 <= pos[1] <= 550:
                            self.snake.difficulty = 0.3
                            self.startingscreen = False
                            pygame.mixer.init()
                            pygame.mixer.Channel(3).play(pygame.mixer.Sound(os.path.join(base_path, "sounds", "bababoi.mp3")))

                        if 450 <= pos[0] <= 750 and 350 <= pos[1] <= 550:
                            self.snake.difficulty = 0.09
                            self.startingscreen = False
                            pygame.mixer.init()
                            pygame.mixer.Channel(3).play(pygame.mixer.Sound(os.path.join(base_path, "sounds", "bababoi.mp3")))

                        if 850 <= pos[0] <= 1100 and 350 <= pos[1] <= 550:
                            self.snake.difficulty = 0.01
                            self.startingscreen = False
                            pygame.mixer.init()
                            pygame.mixer.Channel(3).play(pygame.mixer.Sound(os.path.join(base_path, "sounds", "bababoi.mp3")))

                    if 880 <= pos[0] <= 952 and 20 <= pos[1] <= 80:
                        if self.sound is True:
                            self.sound = False
                            pygame.mixer.Channel(0).pause()
                        else:
                            self.sound = True
                            pygame.mixer.init()
                            pygame.mixer.Channel(0).play(pygame.mixer.Sound(os.path.join(base_path, "sounds", "rick.mp3")))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.escX = self.snake.sx
                    self.escY = self.snake.sy
                    if self.snake.moves is True:
                        self.snake.moves = False
                        self.snake.sx = 0
                        self.snake.sy = 0

                if event.key == pygame.K_SPACE:
                    if self.startingscreen is False:
                        if self.snake.moves is False:
                            self.snake.moves = True
                            if self.escX == 0 and self.escY == 0:
                                self.snake.sy = 0
                                self.snake.sx = self.snake.speed
                            else:
                                self.snake.sy = self.escY
                                self.snake.sx = self.escX

                if self.snake.moves is True:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        if self.snake.sy != self.snake.speed:
                            self.snake.sx = 0
                            self.snake.sy = - self.snake.speed
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        if self.snake.sy != -self.snake.speed:
                            self.snake.sx = 0
                            self.snake.sy = self.snake.speed
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        if self.snake.sx != self.snake.speed:
                            self.snake.sy = 0
                            self.snake.sx = -self.snake.speed
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        if self.snake.sx != -self.snake.speed:
                            self.snake.sy = 0
                            self.snake.sx = self.snake.speed

        self.snake.update()

    def render(self):
        self.screen.blit(self.background, [0, 0])
        self.food.render(self.screen)
        if self.rand == 4:
            self.superfood.render(self.screen)
        self.snake.render(self.screen)
        if self.snake.moves is False:
            self.screen.blit(self.space, [400, 400])
        if self.startingscreen is True:
            self.screen.blit(pygame.image.load(os.path.join(base_path, "images", "startbackground.jpg")), [0, 100])
            self.screen.blit(pygame.image.load(os.path.join(base_path, "images", "difficulty.png")), [300, 200])
            self.screen.blit(pygame.image.load(os.path.join(base_path, "images", "easy.png")), [100, 350])
            self.screen.blit(pygame.image.load(os.path.join(base_path, "images", "normal.png")), [450, 350])
            self.screen.blit(pygame.image.load(os.path.join(base_path, "images", "hard.png")), [850, 350])

        self.screen.blit(self.upperMenu, [0, 0])
        if self.sound is True:
            self.screen.blit(pygame.image.load(os.path.join(base_path, "images", "sound.png")), (880, 20))
        else:
            self.screen.blit(pygame.image.load(os.path.join(base_path, "images", "nosound.png")), (880, 20))
        self.Score()
        self.screen.blit(pygame.image.load(os.path.join(base_path, "images", "title.png")), [10, 10])
        self.screen.blit(pygame.image.load(os.path.join(base_path, "images", "pause.png")), [630, 10])
        if self.selfCollides() or self.wallCollides():
            self.screen.blit(pygame.image.load(os.path.join(base_path, "images", "die.png")), [332, 300])
        pygame.display.flip()
        self.clock.tick(60)

    def wallCollides(self):
        return self.snake.py[0] + 30 > 700 or self.snake.py[0] < 100 or \
               self.snake.px[0] + 30 > 1200 or self.snake.px[0] < 0

    def foodCollides(self):
        return (self.snake.py[0] == self.food.y and self.snake.px[0] == self.food.x) or \
               (self.snake.px[0] == self.food.x and self.snake.py[0] == self.food.y)

    def superfoodCollides(self):
        return (self.snake.py[0] == self.superfood.y and self.snake.px[0] == self.superfood.x) or \
               (self.snake.px[0] == self.superfood.x and self.snake.py[0] == self.superfood.y)

    def selfCollides(self):
        for i in range(1, self.snake.length):
            if self.snake.py[0] == self.snake.py[i] and \
                    self.snake.px[0] == self.snake.px[i]:
                return True

    def Score(self):
        if self.foodCollides():
            self.point += 1
        if self.superfoodCollides():
            self.point += 5
        pygame.font.init()
        a = pygame.font.SysFont('arial', 40)
        score = a.render(f"Score: {self.point}", True, (89, 0, 179))
        self.screen.blit(score, (1050, 25))

    def cleanUp(self):
        pass


class Snake:
    def __init__(self, px, py, length):
        self.py = [py] * length
        self.px = [px, px - 30, px - 60, px - 90, px - 120]
        self.sx = 0
        self.sy = 0
        self.speed = 30
        self.length = length
        self.rick = pygame.image.load(os.path.join(base_path, "images", "rick.png"))
        self.coolrick = pygame.image.load(os.path.join(base_path, "images", "coolrick.png"))
        self.moves = False
        self.difficulty = 0.2

    def update(self):
        if self.moves:
            for i in range(self.length - 1, 0, -1):
                self.py[i] = self.py[i - 1]
                self.px[i] = self.px[i - 1]
        self.px[0] += self.sx
        self.py[0] += self.sy
        time.sleep(self.difficulty)

    def render(self, screen):
        screen.blit(self.coolrick, [self.px[0], self.py[0]])
        for i in range(1, self.length):
            screen.blit(self.rick, [self.px[i], self.py[i]])


class Food:
    def __init__(self):
        self.x = random.randint(0, 39) * 30
        self.y = random.randint(0, 19) * 30 + 100
        self.food = pygame.image.load(os.path.join(base_path, "images", "money.png"))

    def render(self, screen):
        screen.blit(self.food, [self.x, self.y])

    def update(self):
        x = random.randint(0, 39) * 30
        y = random.randint(0, 19) * 30 + 100
        self.x = x
        self.y = y


class superFood:
    def __init__(self):
        self.x = random.randint(0, 40) * 30
        self.y = random.randint(0, 19) * 30 + 100
        self.superfood = pygame.image.load(os.path.join(base_path, "images", "food.png"))

    def render(self, screen):
        screen.blit(self.superfood, [self.x, self.y])

    def update(self):
        x = random.randint(0, 39) * 30
        y = random.randint(0, 19) * 30 + 100
        self.x = x
        self.y = y


if __name__ == "__main__":
    app = App()
    app.run()
