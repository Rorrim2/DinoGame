import os

import pygame
from Dino import Dino
from Background import Background
from Tree import Tree
import random
from Agent import Agent
import matplotlib.pyplot as plt
from datetime import date
import time
import json

from pygame.locals import (K_UP, KEYDOWN, K_ESCAPE)

confirmed = False
player_play = False

NUMBER_OF_ITERATIONS = 0

FILENAME = ""
# asking for a player
while not confirmed:
    print("Who is playing? If player: type 'p', if ai type 'a'")
    player_vs_ai = input()
    if player_vs_ai == "p":
        player_play = True
        confirmed = True
        NUMBER_OF_ITERATIONS = 1
    elif player_vs_ai == 'a':
        confirmed = True
        NUMBER_OF_ITERATIONS = 50
        print("Input filename")
        FILENAME = input()
    else:
        print("Wrong input, try again")

# learning init
NO_ACTION = 0
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

agent = Agent(alpha=0.1, epsilon=0.1, discount=0.99,
                  get_legal_actions=[K_UP, NO_ACTION])

if FILENAME != "":
    agent.load_qValues_from_json(FILENAME)

rewards = []
for i in range(NUMBER_OF_ITERATIONS):
    print("Game nr " + str(i))
    running = True
    total_reward = 0

    pygame.init()
    pygame.display.set_caption("Dino Run")

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    background = Background("Assets/background.png", [0, 0])

    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 500)

    player = Dino()

    obstacles = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    obstacles_list = []

    clock = pygame.time.Clock()

    state = SCREEN_WIDTH - player.x
    next_state = state
    action = 0

    step_finished = True
    while running:
        screen.fill((255, 255, 255))
        screen.blit(background.image, background.rect)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == pygame.QUIT:
                running = False
            elif event.type == ADDENEMY:
                rand = random.randint(0, 100)
                can_plant = True
                if rand < 80:
                    for obstacle in obstacles:
                        if obstacle.x > 600:
                            can_plant = False
                    if can_plant:
                        tree = Tree()
                        obstacles.add(tree)
                        obstacles_list.append(tree)
                        all_sprites.add(tree)

        if player_play:
            pressed_keys = pygame.key.get_pressed()

            # counting points
            for obstacle in obstacles_list:
                if obstacle.x < player.x:
                    player.counter += 1
                    print(player.counter)
                    obstacles_list.pop(0)
            # obstacles_list = [x for x in obstacles_list if not x.x < player.x]

            player.update_sprite(pressed_keys)
            obstacles.update()

            for entity in all_sprites:
                screen.blit(entity.surf, entity.rect)
            if pygame.sprite.spritecollideany(player, obstacles):
                player.kill()
                running = False

            pygame.display.flip()
            clock.tick(30)
        else:
            reward = 0
            if step_finished:
                action = agent.get_action(state)
                step_finished = False
            #step
            if action == K_UP:
                player.update_sprite_ai(K_UP)
                if not player.jumping:
                    step_finished = True
                    reward = -2
            else:
                player.update_sprite_ai(NO_ACTION)
                step_finished = True
            #reward

            for obstacle in obstacles_list:
                if obstacle.x < player.x and not player.jumping:
                    player.counter += 1
                    reward = 2
                    obstacles_list.pop(0)
                    step_finished = True
            obstacles.update()
            #done
            for entity in all_sprites:
                screen.blit(entity.surf, entity.rect)
            if pygame.sprite.spritecollideany(player, obstacles) or player.counter >= 50:
                total_reward = player.counter
                step_finished = True
                player.kill()
                running = False
                if player.counter < 50:
                    reward = -40
            # update agent
            if step_finished:
                if len(obstacles_list) == 0:
                    next_state = SCREEN_WIDTH - player.x
                else:
                    next_state = obstacles_list[0].x - player.x
                agent.update(state, action, reward, next_state, running)
                state = next_state

            pygame.display.flip()
            clock.tick(30)
    if not player_play:
        rewards.append(total_reward)
    pygame.quit()

if not player_play:
    plt.plot(rewards)
    plt.ylabel('Points')
    plt.show()
    today = date.today()
    current_date = today.strftime("%b_%d_%Y")
    if not os.path.exists("Data"):
        os.mkdir("Data")
    t = time.localtime()
    current_time = time.strftime("%H_%M_%S", t)
    serializable = dict((str(k), v) for (k, v) in agent.get_qvalues().items())
    with open("Data" + "/" + current_date + "_" + current_time + '.json', 'w') as fp:
        json.dump(serializable, fp, indent = 4)


