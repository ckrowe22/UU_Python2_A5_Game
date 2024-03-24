import pygame, sys, math, random

# My theme is... The Birds!
# There are lots of enemy birds flying around and there are two big birds that can eat the enemy birds.

# Test if two sprite masks overlap
def pixel_collision(mask1, rect1, mask2, rect2):
    offset_x = rect2[0] - rect1[0]
    offset_y = rect2[1] - rect1[1]
    # See if the two masks at the offset are overlapping.
    overlap = mask1.overlap(mask2, (offset_x, offset_y))
    return overlap

# A basic Sprite class that can draw itself, move, and test collisions
class Sprite:
    def __init__(self, image):
        self.image = image
        self.rectangle = image.get_rect()
        self.mask = pygame.mask.from_surface(image)

    def set_position(self, new_position):
        self.rectangle.center = new_position

    def draw(self, screen):
        screen.blit(self.image, self.rectangle)

    def is_colliding(self, other_sprite):
        return pixel_collision(self.mask, self.rectangle, other_sprite.mask, other_sprite.rectangle)


class Enemy:
    def __init__(self, image, width, height):
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rectangle = image.get_rect()
        self.rectangle.center = (random.randint(0, width), random.randint(0, height))
        vx = random.randint(0, 5)
        vy = random.randint(0, 5)
        self.speed = (vx, vy)
        # Add code to
        # 1. Set the rectangle center to a random x and y based
        #    on the screen width and height
        # 2. Set a speed instance variable that holds a tuple (vx, vy)
        #    which specifies how much the rectangle moves each time.
        #    vx means "velocity in x".

    def move(self):
        # print("need to implement move!")
        self.rectangle.move_ip(self.speed)

        # Add code to move the rectangle instance variable in x by
        # the speed vx and in y by speed vy. The vx and vy are the
        # components of the speed instance variable tuple.
        # A useful method of rectangle is pygame's move_ip method.
        # Research how to use it for this task.

    def bounce(self, width, height):
        # print("need to implement bounce!")
        if self.rectangle.top < 0 or self.rectangle.bottom > height:
            self.speed = (self.speed[0], -self.speed[1])
        if self.rectangle.left < 0 or self.rectangle.right > width:
            self.speed = (-self.speed[0], self.speed[1])

        # This method makes the enemy bounce off of the top/left/right/bottom
        # of the screen. For example, if you want to check if the object is
        # hitting the left side, you can test
        # if self.rectangle.left < 0:
        # The rectangle.left tests the left side of the rectangle. You will
        # want to use .right .top .bottom for the other sides.
        # The height and width parameters gives the screen boundaries.
        # If a hit of the edge of the screen is detected on the top or bottom
        # you want to negate (multiply by -1) the vy component of the speed instance
        # variable. If a hit is detected on the left or right of the screen, you
        # want to negate the vx component of the speed.
        # Make sure the speed instance variable is updated as needed.

    def draw(self, screen):
        # Same draw as Sprite
        screen.blit(self.image, self.rectangle)

class DropEnemy(Enemy):
    def __init__(self, image, width, height):
        super().__init__(image, width, height)
        self.position = self.rectangle.center

    def move(self):
        self.speed = (self.speed[0], self.speed[1] + .1)
        self.position = (self.rectangle.center[0] + self.speed[0], self.rectangle.center[1] + self.speed[1])
        self.rectangle.center = self.position


# I really wanted to utilize inheritance, so I made a new class that is inherited from the Enemy class.
# It is a larger bird that can eat the smaller enemy birds but doesn't impact the player sprite.
# It uses the inherited move and bounce methods, and has its own method called 'eat.'
class BigBird(Enemy):
    def __init__(self, image, width, height):
        super().__init__(image, width, height)

    def eat(self, enemylist):
        for enemy in enemylist:
                if self.rectangle.collidepoint(enemy.rectangle.center[0], enemy.rectangle.center[1]):
                    enemylist.remove(enemy)

class PowerUp:
    def __init__(self, image, width, height):
        # Set the PowerUp position randomly like is done for the Enemy class.
        # There is no speed for this object as it does not move.
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rectangle = image.get_rect()
        self.rectangle.center = (random.randint(0, width), random.randint(0, height))

    def draw(self, screen):
        # Same as Sprite
        screen.blit(self.image, self.rectangle)

class PowerUpRotate(PowerUp):
    def __init__(self, image, width, height):
        super().__init__(image, width, height)
        self.angle = 0
        self.original_image = image

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.original_image, self.angle)
        self.image = rotated_image
        new_rect = self.rectangle.center
        self.rectangle = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rectangle.center = new_rect
        self.angle += 0.2
        super().draw(screen)


def main():
    # Setup pygame
    pygame.init()

    # Get a font for printing the lives left on the screen.
    myfont = pygame.font.SysFont('monospace', 24)

    # Define the screen
    width, height = 600, 400
    size = width, height
    screen = pygame.display.set_mode((width, height))

    # Load image assets
    # Choose your own image
    enemy = pygame.image.load("bird.png").convert_alpha()
    # Here is an example of scaling it to fit a 50x50 pixel size.
    enemy_image = pygame.transform.smoothscale(enemy, (50, 50))
    seagull_image = pygame.image.load("seagull.png").convert_alpha()


    # Make some number of enemies that will bounce around the screen.
    # Make a new Enemy instance each loop and add it to enemy_sprites. 
    enemy_sprites = []
    for i in range(12):
        enemy_sprites.append(Enemy(enemy_image, 600, 400))
        enemy_sprites.append(DropEnemy(seagull_image, 600, 400))

    #making a couple of the big birds that can eat the smaller ones
    hawk_image = pygame.image.load("hawk.png").convert_alpha()
    bigbird_list = []
    for i in range(2):
        bigbird_list.append(BigBird(hawk_image, width, height))


    # This is the character you control. Choose your image.
    player_image = pygame.image.load("Screaming.png").convert_alpha()
    player_sprite = Sprite(player_image)
    life = 3

    # This is the powerup image. Choose your image.
    powerup_image = pygame.image.load("bandaid.png").convert_alpha()
    powerup_rotate_image = pygame.image.load("pink_bandaid.png").convert_alpha()
    # Start with an empty list of powerups and add them as the game runs.
    powerups = []

    # Main part of the game
    is_playing = True
    # while loop
    while is_playing and life > 0: # while is_playing is True, repeat

        # Check for events
        for event in pygame.event.get():
            # Stop loop if click on window close button
            if event.type == pygame.QUIT:
                is_playing = False

        # Make the player follow the mouse
        pos = pygame.mouse.get_pos()
        player_sprite.set_position(pos)

        for enemy in enemy_sprites:
            # if enemy.rectangle.collidepoint(pos):
            if player_sprite.is_colliding(enemy):
                life -= .1

        # Loop over the enemy sprites. If the player sprite is
        # colliding with an enemy, deduct from the life variable.
        # A player is likely to overlap an enemy for a few iterations
        # of the game loop - experiment to find a small value to deduct that
        # makes the game challenging but not frustrating.

        for powerup in powerups:
            if player_sprite.is_colliding(powerup):
                life += 1
        # Loop over the powerups. If the player sprite is colliding, add
        # 1 to the life.

        # Make a list comprehension that removes powerups that are colliding with
        # the player sprite.
        powerups = [p for p in powerups if not player_sprite.is_colliding(p)]

        # Loop over the enemy_sprites. Each enemy should call move and bounce.
        for enemy in enemy_sprites:
            enemy.move()
            enemy.bounce(600, 400)

        # Looping over the 2 bigger birds and also calling the eat method
        for bird in bigbird_list:
            bird.move()
            bird.bounce(600, 400)
            bird.eat(enemy_sprites)

        # Choose a random number. Use the random number to decide to add a new
        # powerup to the powerups list. Experiment to make them appear not too
        # often, so the game is challenging.

        if random.random() > .94 and random.random() < 1:
            powerups.append(PowerUp(powerup_image, 600, 400))
        elif random.random() > .8 and random.random() > .86:
            powerups.append(PowerUpRotate(powerup_rotate_image, 600, 400))

        # Erase the screen with a background color
        screen.fill((0,100,50)) # fill the window with a color

        # Draw the characters
        for enemy_sprite in enemy_sprites:
            enemy_sprite.draw(screen)
        for powerup_sprite in powerups:
            powerup_sprite.draw(screen)
        for bird in bigbird_list:
            bird.draw(screen)

        player_sprite.draw(screen)

        # Write the life to the screen.
        text = "Life: " + str('%.1f'%life)
        label = myfont.render(text, True, (255, 255, 0))
        screen.blit(label, (20, 20))

        # Bring all the changes to the screen into view
        pygame.display.update()
        # Pause for a few milliseconds
        pygame.time.wait(20)

    # Once the game loop is done, pause, close the window and quit.
    # Pause for a few seconds
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
