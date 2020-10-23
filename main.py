import random
import pygame


class Colors():
    def __init__(self):
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)


class Bank():
    def __init__(self):
        self.balance = 0

    def add(self, amount):
        self.balance += amount

    def subtract(self, amount):
        self.balance -= amount

    def set_balance(self, balance):
        self.balance = balance

    def get_balance(self):
        return self.balance


class Button():
    def __init__(self, window, font, bg, fg, text, x, y, width, height, action, args):
        self.window = window
        self.font = font
        self.bg = bg
        self.fg = fg
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        self.args = args

    def draw(self):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.window, self.bg, rect)
        label = self.font.render(self.text, 1, self.fg)
        self.window.blit(label, (self.x + self.width/2 - label.get_width() /
                                 2, self.y + self.height/2 - label.get_height()/2))

    def check_click(self, click):
        if click.x > self.x and click.x < self.x + self.width and click.y > self.y and click.y < self.y + self.height:
            self.action(self.args)


class Game():
    def __init__(self):
        self.run = True
        self.FPS = 60
        pygame.font.init()
        self.main_font = pygame.font.SysFont("Arial", 24)
        self.clock = pygame.time.Clock()
        self.colors = Colors()
        self.WIDTH, self.HEIGHT = 1280, 720
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("incremental")

        self.bank = Bank()

        self.buttons = []
        header = 32
        xs = 16
        ys = 8
        g = 8
        w = (self.WIDTH-g*(xs+1))/xs
        h = (self.HEIGHT-header-g*(ys+1))/ys

        for y in range(ys):
            for x in range(xs):
                value = 0
                self.buttons.append(Button(self.WIN, self.main_font,
                                           self.colors.WHITE, self.colors.BLACK, str(value), x*(w+g)+g, y*(h+g)+g+header, w,  h, self.bank.add, value))

        self.level = 0
        self.max = None
        self.level_up()

    def start(self):
        self.main()

    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan)

    def level_up(self):
        self.level += 1
        self.max = 10 ** self.level
        for i in range(len(self.buttons)):
            self.buttons[i].text = str(10*i)
            self.buttons[i].args = 10*i

    def redraw_window(self):
        self.WIN.fill((51,51,51))

        fps_label = self.main_font.render(
            f"FPS: {int(self.clock.get_fps())}", 1, self.colors.WHITE)
        self.WIN.blit(fps_label, (2, 2))

        token_label = self.main_font.render(
            f"Tokens: {self.bank.get_balance()}", 1, self.colors.WHITE)
        self.WIN.blit(token_label, (self.WIDTH/2 -
                                    token_label.get_width() / 2, 2))

        for button in self.buttons:
            button.draw()

        pygame.display.flip()

    def main(self):

        while self.run:
            self.clock.tick(self.FPS)
            self.redraw_window()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Quit Game
                    self.run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Left Click
                    for button in self.buttons:
                        button.check_click(
                            pygame.Vector2(pygame.mouse.get_pos()))

            balance = self.bank.get_balance()
            if balance == self.max:
                self.level_up()
            elif balance > self.max:
                self.bank.set_balance(0)
                self.level = 0
                self.level_up()

                # keys = pygame.key.get_pressed()
                # if keys[pygame.K_a]:  # left
                #     p.add_acl(pygame.Vector2(-acl, 0))
                # if keys[pygame.K_d]:  # right
                #     p.add_acl(pygame.Vector2(acl, 0))
                # if keys[pygame.K_w]:  # up
                #     p.add_acl(pygame.Vector2(0, -acl))
                # if keys[pygame.K_s]:  # down
                #     p.add_acl(pygame.Vector2(0, acl))


if __name__ == "__main__":
    game = Game()
    game.start()
