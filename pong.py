import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

ball = pygame.draw.rect(screen, pygame.Color(255,255,255), pygame.Rect(10, 10, 10, 10))
cur_x = 5
cur_y = 5
coordinates = screen.get_size()

player = pygame.draw.rect(screen, pygame.Color(255,255,255), pygame.Rect(10, 10, 10, coordinates[1] / 5))
com = pygame.draw.rect(screen, pygame.Color(255,255,255), pygame.Rect(coordinates[0] - 20, 10, 10, coordinates[1] / 5))

def ball_bounce(cur_x, cur_y):
    if ball.x >= coordinates[0] - 10:
        cur_x = -5
        ball_move = ball.move(cur_x,cur_y)
    elif ball.x <= 0:
        cur_x = 5
        ball_move = ball.move(cur_x,cur_y)
    else:
        ball_move = ball.move(cur_x,cur_y)
        
    return cur_x, ball_move
    

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    # Check for specific keys and perform actions
    if keys[pygame.K_UP]:
        if player.y > 0:
            player = player.move(0,-10)
    if keys[pygame.K_DOWN]:
        if player.y < coordinates[1] - player.height:
            player = player.move(0,10)
    
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE
    
    # Ball render
    if ball.y <= 0:
        cur_y = 5
        cur_x, ball_move = ball_bounce(cur_x, cur_y)
    elif ball.y >= coordinates[1] - 10:
        cur_y = -5
        cur_x, ball_move = ball_bounce(cur_x, cur_y)
    else:
        cur_x, ball_move = ball_bounce(cur_x, cur_y)
        
    ball = pygame.draw.rect(screen, pygame.Color(255,255,255),ball_move)
    # print(ball.x, ball.y)
    
    # Left Paddle render
    player = pygame.draw.rect(screen, pygame.Color(255,255,255), player)
    
    pygame.event.get()
    
    
    # Right Paddle render
    com = pygame.draw.rect(screen, pygame.Color(255,255,255), pygame.Rect(coordinates[0] - 20, 10, 10, coordinates[1] / 5))
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()