import pygame
from copy import deepcopy


def export(points, screen_mid):
    points = deepcopy(points)
    p_line = "(StartPoint=(Pitch={pitch},Yaw={yaw},Roll=0),EndPoint=(Pitch=0,Yaw=0,Roll=0)," \
             "bUseStartPointOnly=True," \
             "CustomWaveMotion=(bUseCustomWaveMotion=False,WaveFreq=(X=0.000000,Y=0.000000,Z=0.000000)," \
             "WaveAmp=(X=0.000000,Y=0.000000,Z=0.000000),WavePhase=(X=0.000000,Y=0.000000,Z=0.000000))),"
    with open("exportedFiringPattern.txt", "w+") as f:
        f.write("set FiringModeDefinition FiringPatternLines (")
        for point in points:
            point.x -= screen_mid.x
            point.y = screen_mid.y - point.y
            f.write(p_line.format(pitch=int(point.y * 20), yaw=int(point.x * 20)))
        f.seek(f.tell() - 1)
        f.write(")")


str_help = "LMB: New Point  RMB: Remove last Point  G: Toggle trough Grids  X/Y: Clone on X/Y axis  Enter: Save to " \
           "'exportedFiringPattern.txt'"
pygame.init()
pygame.display.set_caption("BL Firing Pattern Editor")
black = (0, 0, 0)
white = (255, 255, 255)
grey = (190, 190, 190)
light_blue = (100, 100, 155)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
X, Y = 1280, 720
grids = ((1, 1), (16, 9), (32, 18), (64, 36))
curr_grid = 0
display_surface = pygame.display.set_mode((X, Y))
image = pygame.transform.scale(pygame.image.load("BL2FiringPatternBG.png"), display_surface.get_rect()[2:])
my_font = pygame.font.SysFont("Arial.ttf", 24)
help_text = my_font.render(str_help, True, green)
help_text_bg = my_font.render(str_help, True, black)

middle = pygame.Vector2(display_surface.get_rect()[2] / 2, display_surface.get_rect()[3] / 2)
clock = pygame.time.Clock()
pattern_points = []  # store our Vector2 of pattern points
b_clone_y = False
b_clone_x = False
b_snap = False
while True:
    display_surface.blit(image, (0, 0))

    # show grid
    for x in range(0, X, X // grids[curr_grid][0]):
        pygame.draw.line(display_surface, light_blue, (x, 0), (x, Y))
    for y in range(0, Y, Y // grids[curr_grid][1]):
        pygame.draw.line(display_surface, light_blue, (0, y), (X, y))

    # show x/y help lines if needed
    if b_clone_x:
        pygame.draw.line(display_surface, green, (0, Y // 2), (X, Y // 2))
    if b_clone_y:
        pygame.draw.line(display_surface, blue, (X // 2, 0), (X // 2, Y))

    # Display our help text
    display_surface.blit(help_text_bg, (1, 0))
    display_surface.blit(help_text_bg, (-1, 0))
    display_surface.blit(help_text_bg, (0, 1))
    display_surface.blit(help_text_bg, (0, -1))
    display_surface.blit(help_text, (0, 0))

    # mid crosshair
    pygame.draw.line(display_surface, red, middle, (middle.x, middle.y + 20), 1)
    pygame.draw.line(display_surface, red, middle, (middle.x, middle.y - 20), 1)
    pygame.draw.line(display_surface, red, middle, (middle.x + 20, middle.y), 1)
    pygame.draw.line(display_surface, red, middle, (middle.x - 20, middle.y), 1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:  # Right click remove last point
            if pattern_points:
                pattern_points.pop()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Left click add new point
            pos = pygame.Vector2(*pygame.mouse.get_pos())
            # calc optional snap location
            if b_snap and curr_grid > 0:
                # Ill keep this as an optional ToDo :)
                pass

            pattern_points.append(pos)
            if b_clone_y and b_clone_x:
                new_pos = pygame.Vector2()
                if pos.x > middle.x:
                    new_pos.x = (middle.x - (pos.x - middle.x))
                elif pos.x < middle.x:
                    new_pos.x = (middle.x + (middle.x - pos.x))

                if pos.y > middle.y:
                    new_pos.y = (middle.y - (pos.y - middle.y))
                elif pos.y < middle.y:
                    new_pos.y = (middle.y + (middle.y - pos.y))

                pattern_points.append(new_pos)
            elif b_clone_y:
                if pos.x > middle.x:
                    pattern_points.append(pygame.Vector2(middle.x - (pos.x - middle.x), pos.y))
                elif pos.x < middle.x:
                    pattern_points.append(pygame.Vector2(middle.x + (middle.x - pos.x), pos.y))

            elif b_clone_x:
                if pos.y > middle.y:
                    pattern_points.append(pygame.Vector2(pos.x, (middle.y - (pos.y - middle.y))))
                elif pos.y < middle.y:
                    pattern_points.append(pygame.Vector2(pos.x, (middle.y + (middle.y - pos.y))))

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:  # Export all the current points to txt
                export(pattern_points, middle)
            elif event.key == pygame.K_g:
                curr_grid = (curr_grid + 1) % len(grids)
            elif event.key == pygame.K_y or event.key == pygame.K_z:
                b_clone_y = not b_clone_y
            elif event.key == pygame.K_x:
                b_clone_x = not b_clone_x
            elif event.key == pygame.K_s:
                b_snap = not b_snap


    # Draw our pattern points
    for point in pattern_points:
        pygame.draw.line(display_surface, white, point, (point.x, point.y + 5), 1)
        pygame.draw.line(display_surface, white, point, (point.x, point.y - 5), 1)
        pygame.draw.line(display_surface, white, point, (point.x + 5, point.y), 1)
        pygame.draw.line(display_surface, white, point, (point.x - 5, point.y), 1)

    # update our screen
    clock.tick(30)
    pygame.display.flip()
