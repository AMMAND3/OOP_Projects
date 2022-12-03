import pygame, random


def main():
    # initialize all pygame modules (some need initialization)
    pygame.init()
    # create a pygame display window
    pygame.display.set_mode((560, 450))
    # set the title of the display window
    pygame.display.set_caption('Memory')   
    # get the display surface
    w_surface = pygame.display.get_surface() 
    # create a game object
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.play() 
    # quit pygame and clean up the pygame window
    pygame.quit() 


# User-defined classes

class Game:
   # An object in this class represents a complete game.

    def __init__(self, surface):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object
      
      # === objects that are part of every game that we will discuss
        self.surface = surface
        self.bg_color = pygame.Color('black')
        
        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True
        
        # === game specific objects
        
        # list containing images in system
        imageTitles = ["image1.bmp", "image2.bmp", "image3.bmp", "image4.bmp", "image5.bmp", "image6.bmp", "image7.bmp", "image8.bmp"]
        # images will contain all the images, but twice and then it will be shuffled
        images = []
        for imageTitle in imageTitles:
           #image = pygame.image.load(imageTitle)
            images.append(imageTitle)
            images.append(imageTitle)
        random.shuffle(images) # shuffle images
        
        self.images = images
        
        # self.tile1 will represent the first tile and
        # self.tile2 the second tile
        self.tile1 = None
        self.tile2 = None
        # self.timing will help keep count of timing between turns
        self.timing = 0
        # self.tilecount will keep track of number of exposed tiles
        self.tilecount = 0
        
        # self.score will help keep track of the time as a score
        self.score = [0]
        
        # self.turn will help keep track of player turns for each tile
        self.turn = 0
        # the strings below will give the image name for both tiles
        self.turn_str1 = ""
        self.turn_str2 = ""
        
        # the following image will be the cover image needed
        self.image0 = "image0.bmp"
        
        # the below variables give the tile height a width needed
        tile_height = self.surface.get_height() // 4 # each tile height
        tile_width = 3/4*self.surface.get_width() // 4 # each tile width        
        
        # Create the board
        # self.board wil contain the tiles as a nested list
        self.board = []
        for row in range(0, 4):
            rows = []
            for column in range(0, 4):
        
                x = column * tile_width # this gives x position of tile as on surface 
                y = row * tile_height # this gives y position of tile as on surface
                tilePosition = [x, y, tile_width, tile_height] # create the tile
                # using random.choice() let us again randomly select an image
                image = random.choice(images)
                self.images.remove(image)     
                # finally the image variable is used as the picture for this specific tile
                # at its position
                tile = Tile(tilePosition, self.image0, image, surface)
                # let us now draw the card, since it is initially not exposed I have hidden
                # it by using image0
                tile.hide_card()
                # finally append the tile to rows
                rows.append(tile)
        
            self.board.append(rows) # at the end of each row append it to the whole self.board

    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.
    
        while not self.close_clicked:  # until player clicks close box
           # play frame
            self.handle_events()
            
            if self.continue_game:
                self.update()
                self.decide_continue()
                self.draw()
                pygame.display.update()
              
            self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled
    
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
    
            if event.type == pygame.MOUSEBUTTONUP:
                # ie if mousebuttonup is pressed then we use handle_mouse_up function
                self.handle_mouse_up(event.pos)         

    def draw(self):
      # The following code will be used to draw the score at the top corner.
        if self.continue_game == True:
            ticks = pygame.time.get_ticks()
            self.score[0] = (ticks // 1000) - 1
            fg_color = pygame.Color('white')
            # 2.create the font object
            font = pygame.font.SysFont('', 60)
            # 3 Create a text box by rendering the font
            text_box = font.render(str(self.score[0]), True, fg_color, self.bg_color)
            surface_height = self.surface.get_width()
            text_box_height = text_box.get_width()
            location = (surface_height - text_box_height, 0)
            self.surface.blit(text_box, location)
      
            #pygame.display.flip() # make the updated surface appear on the display
        

    def handle_mouse_up(self, mousePosition): # if the mouse button up is pressed we carry out the following method

        for row in self.board:
            for tile in row:
                # if a tile is selected then True will be returned if it is not exposed
                # else if it already is then False is returned
                if tile.select(mousePosition):
                    # if True and self.turn is an integer
                    if type(self.turn) == int:
                        # also, if self.turn <= 2
                        if self.turn <= 2:
                            # let us first add 1 to self.turn
                            self.turn += 1
                            # if self.turn == 1 it means it is first click
                            if self.turn == 1:
                                # first draw the tile
                                tile.draw_card()
                                # also using str_name() method we add its image name to self.turn_str1
                                self.turn_str1 += tile.str_name()
                                # finally, also assign tile1 to this tile
                                self.tile1 = tile
                            # if self.turn ==2 it means it is second click
                            elif self.turn == 2:
                                # we carry same procedure as above
                                tile.draw_card()
                                self.turn_str2 += tile.str_name()
                                self.tile2 = tile
                                self.timing = pygame.time.get_ticks() + 1000
                                # we also make self.turn a None object
                                self.turn = None                

        pygame.display.update()    

    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update
        # first let us get the current time using get_ticks()
        current_time = pygame.time.get_ticks()

        # to ensure we only have turns, let us make sure self.turn is equal to None
        if self.turn == None:
            # moreover, if the current time is greater than or equal to self.timing
            # which ensures 1 second have passed
            if current_time >= self.timing:
                # now, if the image names for both images are equal we keep them uncovered
                if self.turn_str1 == self.turn_str2:
                    # add 2 to tile count
                    self.tilecount += 2
                    # restart the whole process
                    self.turn_str1 = ""
                    self.turn_str2 = ""
                    self.tile1 = None
                    self.tile2 = None
                    self.turn = 0

                # however if the names are not equal we cover them using their methods
                elif self.turn_str1 != self.turn_str2:
                    # hide both the cards
                    self.tile1.hide_card()
                    self.tile2.hide_card()
                    # restart the whole process
                    self.turn_str1 = ""
                    self.turn_str2 = ""
                    self.tile1 = None
                    self.tile2 = None
                    self.turn = 0

        pygame.display.update()

    def decide_continue(self):
        # Check and remember if the game should continue
        # Here, if total tiles uncovered is 16 we stop the game
        if self.tilecount == 16:
            self.continue_game = False


class Tile: # this is the tile class

    def __init__(self, tilePosition, image0, image, surface):

        # left self.x and self.y be the centers of the Tile
        self.x = tilePosition[0]
        self.y = tilePosition[1]
        # using the parameters we also get the width and height
        self.width = tilePosition[2]
        self.height = tilePosition[3]
        # also, assign image0 and image to a variable so that we can keep them aside
        self.image0 = image0
        self.image = image
        # game surface
        self.surface = surface
        # create the Tile as a rectangle  
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # The below is a color for the tile border
        self.color = pygame.Color("black")
        # initially tile is covered, so it is True
        self.covered = True
      
    def str_name(self): # this method returns image name of a tile
        return self.image

    def draw_card(self): # this method draws the tile
        # first load the image, then draw it and blit the image at the position
        # of the rectangle. We also have a border of width 6 which is black in color
        theimage = pygame.image.load(self.image)
        pygame.draw.rect(self.surface,self.color,self.rect,6)
        self.surface.blit(theimage,self.rect)
        # since the tile is exposed, self.covered == False
        self.covered = False

    def hide_card(self): # this method reverses tile to original state, ie covered
        # first load the image an draw, blit it in rectangles position
        notimage = pygame.image.load(self.image0)
        pygame.draw.rect(self.surface,self.color,self.rect,6)
        self.surface.blit(notimage,self.rect)       
        # since it is now covered, self.covered == True
        self.covered = True
      
    def select(self, mousePosition): # this method will decide if a tile is already exposed or not
        # assign a boolean False to valid_click
        valid_click = False
        # now using the mouse position, we will find if the click is on the tile
        # we assign first and second positions of the list of mousePosition, which gives
        # the mouse click's position
        mouseX = mousePosition[0]
        mouseY = mousePosition[1]

        # we then check if the click position is in between the tile
        if mouseX >= self.x and mouseX <= self.x + self.width:
            if mouseY >= self.y and mouseY <= self.y + self.height:
                # moreover, we must also check if tile is already covered or not
                # if it is finally using valid_click return True
                if self.covered == True:
                    valid_click = True
                # if however it is not covered then return False
                else:
                    valid_click = False
   
        return valid_click

main()
