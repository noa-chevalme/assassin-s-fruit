import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()
clock = pygame.time.Clock()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Assassin's Fruit")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Charger les images
image_fruit = pygame.image.load("image_fruit/orange.png")
image_bombe = pygame.image.load("image_fruit/bombe.png")

# Redimensionner les images
image_fruit = pygame.transform.scale(image_fruit, (50, 50))
image_bombe = pygame.transform.scale(image_bombe, (50, 50))

# Police d'affichage    
font = pygame.font.Font(None, 36)

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.lives = 3

    def add_points(self, points):
        self.score += points
    
    def lose_life(self):
        self.lives -= 1

class Fruit:
    def __init__(self):
        self.image = image_fruit
        self.x = random.randint(100, WIDTH - 100)
        self.y = HEIGHT
        self.vx = random.randint(-3, 3)
        self.vy = random.randint(-12, -8)
        self.gravity = 0.4
        self.key = random.choice(["Z", "Q", "S", "D"])  # Seules les touches ZQSD
        self.points = random.randint(50, 250)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        text = font.render(self.key, True, BLACK)
        surface.blit(text, (self.x + 15, max(10, self.y - 30)))

class Bombe:
    def __init__(self):
        self.image = image_bombe
        self.x = random.randint(100, WIDTH - 100)
        self.y = HEIGHT
        self.vx = random.randint(-3, 3)
        self.vy = random.randint(-12, -8)
        self.gravity = 0.4
        self.key = random.choice(["Z", "Q", "S", "D"])  # Seules les touches ZQSD

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        text = font.render(self.key, True, RED)
        surface.blit(text, (self.x + 15, max(10, self.y - 30)))

def demander_pseudo():
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
    color = pygame.Color("lightskyblue3")
    pseudo = ""
    active = False
    font = pygame.font.Font(None, 48)

    while True:
        screen.fill((139, 69, 19))  # Fond boisé
        text_surface = font.render("Entrez votre pseudo:", True, WHITE)
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - 100))
        
        pygame.draw.rect(screen, color, input_box, 2)
        pseudo_surface = font.render(pseudo, True, WHITE)
        screen.blit(pseudo_surface, (input_box.x + 5, input_box.y + 10))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                active = input_box.collidepoint(event.pos)
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return pseudo if pseudo else "Joueur"
                    elif event.key == pygame.K_BACKSPACE:
                        pseudo = pseudo[:-1]
                    else:
                        pseudo += event.unicode

def jeu():
    pseudo = demander_pseudo()
    player = Player(pseudo)
    fruits = []
    bombes = []

    spawn_delay = 1000  # Augmenté pour plus de rapidité
    last_spawn_time = pygame.time.get_ticks()

    running = True
    while running:
        screen.fill((139, 69, 19))  # Fond boisé
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                key_pressed = pygame.key.name(event.key).upper()
                for fruit in fruits[:]:
                    if fruit.key == key_pressed:
                        player.add_points(fruit.points)
                        fruits.remove(fruit)
                for bombe in bombes[:]:
                    if bombe.key == key_pressed:
                        player.lose_life()
                        bombes.remove(bombe)

        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time > spawn_delay:
            if random.random() < 0.7:
                fruits.append(Fruit())
            else:
                bombes.append(Bombe())
            last_spawn_time = current_time
            spawn_delay = max(300, spawn_delay - 20)  # Accélère avec le temps

        for obj_list in [fruits, bombes]:
            for obj in obj_list[:]:
                obj.update()
                if obj.y > HEIGHT:
                    obj_list.remove(obj)
                obj.draw(screen)

        score_text = font.render(f"Score: {player.score}", True, WHITE)
        lives_text = font.render(f"Vies: {player.lives}", True, RED)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))

        if player.lives <= 0:
            running = False

        pygame.display.update()
        clock.tick(60)

def menu_principal():
    jeu()

menu_principal()
