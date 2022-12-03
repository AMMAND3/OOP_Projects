import pygame, math, random


# User-defined functions

def main(): # main function
    # initialize all pygame modules (some need initialization)
    pygame.init()
    # create a pygame display window
    pygame.display.set_mode((400, 400))
    # set the title of the display window
    WHITE = (255,255,255)
    pygame.display.set_caption('Pong')   
    # get the display surface
    w_surface = pygame.display.get_surface() 
    # create a game object
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.play() 
    # quit pygame and clean up the pygame window
    pygame.quit() 


# User-defined classes

class Game: # Game class
    # An object in this class represents a complete game

    def __init__(self, surface):
        # Initialize a Game.
        # - self is the Game to initialize
        # - surface is the display window surface object
        # We also initialize a background with a black color

        # === objects that are part of every game that we will discuss
        self.surface = surface
        self.bg_color = pygame.Color('black')

        # Frame rate that we will keep the game at. pygame.time.Clock() helps enable this. 
        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        
        # Variables we will use to decide to continue game or not.
        self.close_clicked = False
        self.continue_game = True

        # === game specific objects. I have incorporated them individually so that they pass through the Game object.
        
        # The 2 paddles left position.
        self.paddle1left = 100
        self.paddle2left = 300

        # The 2 paddles top position 
        self.paddle1top = 175
        self.paddle2top = 175

        # The first paddles width and height
        self.paddle1width = 10
        self.paddle1height = 50

        # The second paddles width and height
        self.paddle2width = 10
        self.paddle2height = 50

        # Now for the ball's attributes which are its radius, center and velocity.
        self.ball_radius = 10
        self.ball_center = [random.randint(180,220), random.randint(180,220)]
        self.ball_velocity = [6,2]
        
        # These attributes help to maintain the scores for player A and B
        self.scoreA = 0
        self.scoreB = 0

        # Finally, using the above attributes we create the paddles and the ball.
        self.paddleA = Paddle(self.surface, self.paddle1left, self.paddle1top, self.paddle1width, self.paddle1height)
        self.paddleB = Paddle(self.surface, self.paddle2left, self.paddle2top, self.paddle2width, self.paddle2height)
        self.ball = Ball(self.ball_radius, self.ball_center, self.ball_velocity, self.surface)

        
                 
    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()

            if self.continue_game:
                self.draw()
                self.update()
                self.decide_continue()
                

            self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True

    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw

        self.surface.fill(self.bg_color) # clear the display surface first
        
        # Draw the paddles
        self.paddleA.draw()
        self.paddleB.draw()
        
        # Draw the ball
        self.ball.draw()
        
        # Update the ball as well, as per where is the position of it.
        self.ball.update()
        
        # The following code helps represent the players score each time frame is updated
        WHITE = (255,255,255)
        font = pygame.font.Font(None, 65)
        text = font.render(str(self.scoreA), 1, WHITE)
        self.surface.blit(text, (10,10))
        text = font.render(str(self.scoreB), 1, WHITE)
        self.surface.blit(text, (350,10))        

        pygame.display.update() # make the updated surface appear on the display

    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update
        
        # The following code changes the position of the paddles as per the players input
        # Notice we have used only if statements so that both players can play at the same time
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_q]:
            self.paddleA.moveUp(5)
        if keys[pygame.K_a]:
            self.paddleA.moveDown(5)
        if keys[pygame.K_p]:
            self.paddleB.moveUp(5)
        if keys[pygame.K_l]:
            self.paddleB.moveDown(5)

        # The following code detects the collision between the paddle and the ball.
        # Since the ball has to pass to through the paddles from the opposite sides, logically we know that for example
        # if the ball enters the paddle A from the left, then its horizontal velocity is greater than 0. Thus to make sure it passes
        # through and we don't detect for collison unless so, we keep the condition when only if the ball meets the paddle A
        # from the right, then only detect for collision that is when horizontal component of velocity is less than 0.
        # We keep the same logic for paddle B except, here horizontal component of velocity should be greater than 0.
        if self.ball_velocity[0] < 0:
            
            #This part of the code detects the collision. When I used collidepoint() I am considering the center of the ball as the point.
            # However, I have included horizontal center of ball minus 10 since that is the ball's radius.
            # In addition, I considered the vertical center of the ball for both plus and minus 10 since, the ball can hit the two paddles vertically
            # from either the top or the bottom, unlike for the horizontal part.
            if self.paddleA.collide(self.ball_center[0] - 10, self.ball_center[1] - 10) == True or self.paddleA.collide(self.ball_center[0] - 10, self.ball_center[1] + 10) == True:
                self.ball_velocity[0] = -self.ball_velocity[0]
                self.ball_velocity[1] = -random.randint(-2,3)
            
        if self.ball_velocity[0] > 0:
            
            if self.paddleB.collide(self.ball_center[0] + 10, self.ball_center[1] - 10) == True or self.paddleB.collide(self.ball_center[0] + 10, self.ball_center[1] + 10) == True:
                self.ball_velocity[0] = -self.ball_velocity[0]
                self.ball_velocity[1] = -random.randint(-2,3)
        
        # This code changes the scores based of whether that ball hits the edge of the opponents screen.    
        #if self.ball_center[0] >= pygame.display.get_surface().get_height() - self.ball_radius:
        if self.ball_center[0] >= self.surface.get_height() - self.ball_radius:
            self.scoreA+=1

        if self.ball_center[0] <= 10:
            self.scoreB+=1
            
    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check

        if self.scoreA == 11 or self.scoreB == 11 :
            self.draw()
            self.update()            
            self.continue_game = False    

class Ball: # Ball class
    # An object in this class represents a Ball that moves 

    def __init__(self, ball_radius, ball_center, ball_velocity, surface):
        # Initialize a Ball.
        # - self is the Ball to initialize
        # - color is the pygame.Color of the ball
        # - center is a list containing the x and y int coords of the center of the ball
        # - radius is the int pixel radius of the ball
        # - velocity is a list containing the x and y components
        # - surface is the window's pygame.Surface object

        self.color = pygame.Color("white")
        self.radius = ball_radius
        self.center = ball_center
        self.velocity = ball_velocity
        self.surface = surface

    def update(self):
        
        # The following code updates the position of the ball. First, we add the
        # velocity to both components of the center.
        for i in range(0,2):
            self.center[i] = (self.center[i] + self.velocity[i])          

        # Next we ensure that when the ball touches the edge of the screen we
        # change the velocity by making it negative, for both the components

        for i in range(0,2):
            if self.center[i] >= 390:
                self.velocity[i] = -self.velocity[i]
                
            if self.center[i] <= 10:
                self.velocity[i] = -self.velocity[i]

    def draw(self):
        # Draw the ball on the surface
        # - self is the Ball
        
        pygame.draw.circle(self.surface, self.color, self.center, self.radius)


class Paddle: # Let us now make the paddle class
    
    # An object here represents the paddle that moves
    def __init__(self, surface, left, top, width, height):
        
        # Initialize a paddle.
        # - self is the Paddle to initialize
        # - color is the pygame.Color of the paddle
        # - left is the left coordinate of the paddlec
        # - top is the top coordinate of the paddle
        # - width and height as well
        # - surface is the window's pygame.Surface object        
        self.surface = surface
        self.color = pygame.Color("white")
        self.left = left
        self.top = top
        self.width = width
        self.height = height
    
    # This code helps to move the paddles up based on input called pixels    
    def moveUp(self, pixels):
        self.top -= pixels
        #Check that you are not going too far (off the screen)
        if self.top < 10:
            self.top = 0
    
    # This code helps to move the paddles down based on input called pixels
    def moveDown(self, pixels):
        self.top += pixels
        #Check that you are not going too far (off the screen)
        if self.top > 350:
            self.top = 350

    def draw(self):

        # We use the pygame.draw.rect() function to draw the paddles as rectangles.
        pygame.draw.rect(self.surface, self.color, pygame.Rect(self.left, self.top, self.width, self.height))
        
    def collide(self, pointx, pointy):
        
        # We use the collidpoint() function to help detect collision of a point with the paddles.
        return pygame.Rect(self.left, self.top, self.width, self.height).collidepoint(pointx, pointy)
        

main()
