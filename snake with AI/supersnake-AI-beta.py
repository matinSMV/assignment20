import time
import random
import arcade

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

class Snake(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.width = 16
        self.height = 16
        self.color = arcade.color.BLUE
        self.color2 = arcade.color.YELLOW
        self.x = 0
        self.y = 0
        self.score = 0
        self.center_x = SCREEN_WIDTH // 2 
        self.center_y = SCREEN_HEIGHT // 2 
        self.speed = 16
        self.body = []
        self.body.append([self.center_x , self.center_y])

    def move(self):
        for i in range(len(self.body)-1,0,-1):
            self.body[i][0] = self.body[i-1][0]
            self.body[i][1] = self.body[i-1][1]

        self.center_x += self.speed * self.x
        self.center_y += self.speed * self.y
        time.sleep(0.035)

        if self.body:
            self.body[0][0] += self.speed * self.x
            self.body[0][1] += self.speed * self.y
            time.sleep(0.035)

    def eat(self,wte):
        match wte:
            case 0:
                self.score += 1
                self.body.append([self.body[len(self.body)-1][0] , self.body[len(self.body)-1][1]])
            case -1:
                self.score -= 1
                self.body.pop()


    def draw(self):
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width , self.height, self.color)

        for i in range(len(self.body)):
            if i % 2 == 0:
                arcade.draw_rectangle_filled(self.body[i][0] , self.body[i][1] , self.width , self.height , self.color2)
            else:
                arcade.draw_rectangle_filled(self.body[i][0]  , self.body[i][1] , self.width , self.height , self.color)

class Apple(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 16
        self.height = 16
        self.color = arcade.color.RED
        self.r = 8
        self.center_x = random.randint(10, SCREEN_WIDTH - 10)
        self.center_y = random.randint(10 , SCREEN_HEIGHT - 10)

    def draw(self):
        arcade.draw_circle_filled(self.center_x , self.center_y ,self.r ,self.color)

class Poo(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 16
        self.height = 16
        self.color = arcade.color.BROWN
        self.r = 8
        self.center_x = random.randint(10, SCREEN_WIDTH - 10)
        self.center_y = random.randint(10 , SCREEN_HEIGHT - 10)

    def draw(self):
        arcade.draw_circle_filled(self.center_x , self.center_y ,self.r ,self.color)

class Game(arcade.Window):
    def __init__(self):
        super().__init__(width =SCREEN_WIDTH , height =SCREEN_HEIGHT,title="SuperSnake")
        arcade.set_background_color(arcade.color.DARK_GREEN)
        self.snake = Snake()
        self.apple = Apple()
        self.poo = Poo()

        

    def on_update(self, delta_time: float):

        if self.snake.center_y < self.apple.center_y:
            self.snake.y = 1
        elif self.snake.center_y > self.apple.center_y:
            self.snake.y = -1
        else:
            self.snake.y = 0
        if self.snake.center_x < self.apple.center_x:
            self.snake.x = 1 
        elif self.snake.center_x > self.apple.center_x:
            self.snake.x = -1
        else:
            self.snake.x = 0
        


        self.snake.move()
        if arcade.check_for_collision(self.snake , self.apple):
            self.snake.eat(0)
            self.apple = Apple()
        elif arcade.check_for_collision(self.snake , self.poo):
            self.snake.eat(-1)
            self.poo = Poo()



    def on_draw(self):
        arcade.start_render()
        self.snake.draw()
        self.apple.draw()
        self.poo.draw()
        arcade.draw_text("Score:", 20 , SCREEN_HEIGHT - 25, arcade.color.WHITE)
        arcade.draw_text(str(self.snake.score), 100, SCREEN_HEIGHT -25, arcade.color.WHITE)
        if self.snake.score == -1 or self.snake.center_x<0 or self.snake.center_x > SCREEN_WIDTH or self.snake.center_y < 0 or self.snake.center_y > SCREEN_HEIGHT:
            arcade.draw_text("Game Over!" , SCREEN_WIDTH // 2 - 80 ,SCREEN_HEIGHT // 2, arcade.color.RED, bold=True, font_size=20)
            arcade.exit()

    

my_game = Game()
arcade.run()
    