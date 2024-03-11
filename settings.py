import pygame

screen_size_display = (width_screen, height_screen) = (600, 250)
FPS = 60
gravity = 0.6

black_color = (0, 0, 0)
white_color = (255, 255, 255)
bg_color = (235, 235, 235)
gp = 4

# ! rgb

highest_scores = 0

screen_layout_display = pygame.display.set_mode(screen_size_display)
time_clock = pygame.time.Clock()
pygame.display.set_caption("Dino Run ")

pygame.init()

jump_sound = pygame.mixer.Sound('resources/jump.wav')
die_sound = pygame.mixer.Sound('resources/die.wav')
checkPoint_sound = pygame.mixer.Sound('resources/checkPoint.wav')


# ! music counds