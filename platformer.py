import pygame
import random
import math
from PIL import Image
from numpy import array, dot
from numpy.random import rand
import numpy as np
import time

#gravity = 0.2
#(width, height) = (1200, 675)
#background_colour = (255, 255, 255)
duration = 60
clock = pygame.time.Clock()
level = 'level2.bmp'
checkpoints = [(208, 578), (413, 518), (624, 456), (878, 379), (647, 302),
(457,220), (653, 124), (931, 59)]

def breed(j1, j2):
    variation = 0.05
    new_mind = np.zeros((4,4))

    for i in range(np.size(new_mind, 0)):
        for j in range(np.size(new_mind, 1)):
            coin = random.randint(0,1)
            if coin == 1:
                new_mind[i, j] = j1.mind[i, j]+ random.uniform(-variation, variation)
            if coin == 0:
                new_mind[i, j] = j2.mind[i, j]+ random.uniform(-variation, variation)

    return new_mind           
class Jumper:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (random.randint(0,255), random.randint(0,255),random.randint(0,255))
        self.thickness = size
        #vertical speed is all that is going to matter
        self.speed = 0
        self.gravity = 0.06

        self.distance_up = 0
        self.distance_up_left = 0
        self.distance_up_right = 0
        self.distance_down = 0

        self.fov = math.pi/2

        self.mind = np.random.rand(4,4)

        self.score = 0
        self.current_checkpoint = 0
        self.max_height = 0 
    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)),
        self.size, self.thickness)

    def move(self):
        self.y += self.speed
        self.speed += self.gravity

    def checkpoints_score(self):
        if 675-self.y > self.max_height:
            self.max_height = 675 - self.y
        if int(self.x) in range(checkpoints[self.current_checkpoint][0]-50 , checkpoints[self.current_checkpoint][0] + 50):
            if int(self.y) in range(checkpoints[self.current_checkpoint][1]-100 , checkpoints[self.current_checkpoint][1]):
                self.current_checkpoint +=1
                self.score += 1000
        if self.current_checkpoint > 0:
            if int(self.y) > checkpoints[self.current_checkpoint - 1][1] + 75:
                self.score -= 1000
                self.current_checkpoint -=1
        
"""
    def bounce(self):
        if self.x > width - self.size:
            self.x = 2 * (width - self.size) - self.x
        elif self.x < self.size:
            self.x = 2 * self.size - self.x
        if self.y > height - self.size:
            self.y = 2 * (height - self.size) - self.y
            self.speed = 0
        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.speed = 0
"""
class  Enviroment:

    def __init__(self, size, image, colliding):
        self.width = size[0]
        self.height = size[1]
        self.colour = (255, 255, 255)
        self.track = array(Image.open(image))[:,:,1]/255
        self.track = self.track.astype(int)
        self.colliding = colliding
        self.jumpers = []

    def addJumper(self):
        x = 600
        y = 650
        size = 5
        jumper = Jumper(x, y, size)

        self.jumpers.append(jumper)

    def bounce(self, jumper):
        if jumper.x > self.width - jumper.size:
            jumper.x = 2 * (self.width - jumper.size) - jumper.x
        elif jumper.x < jumper.size:
            jumper.x = 2 * jumper.size - jumper.x
        if jumper.y > self.height - jumper.size:
            jumper.y = 2 * (self.height - jumper.size) - jumper.y
            jumper.speed = 0
        elif jumper.y < jumper.size:
            jumper.y = 2 * jumper.size - jumper.y
            jumper.speed = 0 

    def level_bounce(self, jumper):

        if self.track[int(jumper.y), int(jumper.x + jumper.size)] == 0:
            jumper.x -= jumper.size
            jumper.score -= 25
        
        if self.track[int(jumper.y), int(jumper.x - jumper.size)] == 0:
            jumper.x += jumper.size
            jumper.score -= 25

        if self.track[int(jumper.y + jumper.size), int(jumper.x)] == 0:
            jumper.speed = 0
            jumper.y -= jumper.size/20
            
            
        if self.track[int(jumper.y - jumper.size), int(jumper.x)] == 0:
            if jumper.speed < 0:
                jumper.speed = 0.001
            jumper.y += jumper.size/20
            #decrease score when colliding with the top of a platform
            jumper.score -= 25
            

    def update(self):
        for i, jumper in enumerate(self.jumpers):
            jumper.move()
            jumper.display()
            jumper.checkpoints_score()
            self.bounce(jumper)
            self.level_bounce(jumper)
          #  keys = pygame.key.get_pressed()
            self.distances(jumper)
            self.brain(jumper)
    
    """
            if keys[pygame.K_UP] and jumper.speed == 0:
                jumper.speed -= 3.5
            if keys[pygame.K_RIGHT]:
                jumper.x += 3.5
            if keys[pygame.K_LEFT]:
                jumper.x -= 3.5
            if keys[pygame.K_DOWN] and jumper.speed != 0:
                jumper.speed += 2 * jumper.gravity
    """

    def distances(self, jumper):
        angle = jumper.fov/2
        up = math.pi

        def wheres_the_wall(self, jumper, angle):

            in_wall = False
            vector_x = jumper.x
            vector_y = jumper.y 

            while in_wall == False:

                vector_x += 2 * math.sin(angle)
                vector_y += 2 * math.cos(angle)
                if self.track[int(vector_y), int(vector_x)] == 0:
                    in_wall = True
                
            return vector_x, vector_y
        
        test_x, test_y = wheres_the_wall(self, jumper, 0)
        jumper.distance_down = math.hypot(test_x - jumper.x, test_y - jumper.y)

        test_x, test_y = wheres_the_wall(self, jumper, up)
        jumper.distance_up = math.hypot(test_x - jumper.x, test_y - jumper.y)

        test_x, test_y = wheres_the_wall(self, jumper, up - angle)
        jumper.distance_up_right = math.hypot(test_x - jumper.x, test_y - jumper.y)

        test_x, test_y = wheres_the_wall(self, jumper, up + angle)
        jumper.distance_up_left = math.hypot(test_x - jumper.x, test_y - jumper.y)

    def brain(self, jumper):
        inputs = np.array([jumper.distance_up, jumper.distance_up_right,
        jumper.distance_up_left, jumper.distance_down])
        
        outputs = jumper.mind @ inputs
        if outputs[0] > 200 and jumper.speed == 0:
            jumper.speed -= 3.75
        if outputs[1] > 200 and outputs[1]> outputs[2]:
            jumper.x += 3.5
        if outputs[2] > 200 and outputs[2] > outputs[1]:
            jumper.x -= 3.5
        if outputs[3] > 200:
            jumper.speed += 2 * jumper.gravity
    
    def env_reset(self):
        for i , jumper in enumerate(self.jumpers):
            jumper.x = 600
            jumper.y = 650
            jumper.speed = 0
            jumper.score = 0
            jumper.current_checkpoint = 0
            jumper.max_height = 0






#pygame.init()
env = Enviroment((1200, 675), image = level, colliding = False )       
screen = pygame.display.set_mode((env.width, env.height))
for i in range(300):
    env.addJumper()

pygame.display.set_caption('My Second Game')
#screen.fill(background_colour)

#my_second_particle = Jumper(150, 50, 15)
#my_second_particle.display()

running = True
level_image = pygame.image.load(level)
level_rect = level_image.get_rect()
level_rect.left, level_rect.left = [0,0]
n = 0
while n < 40:
    start_time = time.time()
    current_time = time.time()

    while current_time - start_time < 60 and running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                n = 40
        screen.fill(env.colour)
        screen.blit(level_image, level_rect)
        env.update()
        pygame.display.flip()
        current_time = time.time()
    for i, jumper in enumerate(env.jumpers):
        jumper.score += jumper.max_height

    env.jumpers.sort(key = lambda x: x.score, reverse = True)

    print('The top Scores for this generation are \n')
    for i, jumper in enumerate(env.jumpers):
        if i > 9:
            jumper.mind = breed(env.jumpers[random.randint(0,9)], env.jumpers[random.randint(0,9)])
        if i < 9:
            print(jumper.score)
    env.env_reset()
    running = True

    print('Current Generation =', n)
    n +=1
    