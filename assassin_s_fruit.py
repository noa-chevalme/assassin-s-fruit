import pygame
import random
import sys
from menu import Menu
from leaderboard import Leaderboard

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

# Charger les images de fruits
image_fruit = {
    "orange": pygame.image.load("image_fruit/orange.png"),
    "banane": pygame.image.load("image_fruit/banane.png.webp"),
    "ananas": pygame.image.load("image_fruit/ananas.webp"),
    "tomate": pygame.image.load("image_fruit/tomate.png")
}
# Redimensionner les images
image_fruit = {k: pygame.transform.scale(v, (50, 50)) for k, v in image_fruit.items()}

# Police d'affichage    
font = pygame.font.Font(None, 36)

class Fruit:
    def __init__(self, name, points):
        self.name = name
        self.image = image_fruit[name]
        self.x = random.randint(100, WIDTH - 100)
        self.y = HEIGHT
        self.vx = random.randint(-3, 3)
        self.vy = random.randint(-15, -10)
        self.gravity = 0.5
        self.key = random.choice(["A", "Z", "E", "R", "T", "Y"])  # Touche aléatoire
        self.points = points

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        text = font.render(self.key, True, BLACK)
        surface.blit(text, (self.x + 15, max(10, self.y - 30)))

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def add_points(self, fruit):
        self.score += fruit.points

def demander_pseudo():
    """Affiche un champ de texte pour entrer un pseudo."""
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
    color = pygame.Color("lightskyblue3")
    pseudo = ""
    active = False
    font = pygame.font.Font(None, 48)

    while True:
        screen.fill((139, 69, 19))  # Fond boisé
        text_surface = font.render("Entrez votre pseudo:", True, (255, 255, 255))
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - 100))

        pygame.draw.rect(screen, color, input_box, 2)
        pseudo_surface = font.render(pseudo, True, (255, 255, 255))
        screen.blit(pseudo_surface, (input_box.x + 5, input_box.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return pseudo if pseudo else "Joueur"  # Retourne "Joueur" si le pseudo est vide
                    elif event.key == pygame.K_BACKSPACE:
                        pseudo = pseudo[:-1]
                    else:
                        pseudo += event.unicode

def menu_principal():
    """Affiche le menu et attend que l'utilisateur choisisse une option."""
    menu = Menu(screen)
    leaderboard = Leaderboard()

    in_menu = True
    while in_menu:
        menu.draw()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            action = menu.handle_event(event)
            if action == "play":
                pseudo = demander_pseudo()
                jeu(pseudo)  # On passe le pseudo au jeu
                in_menu = False  # Quitter le menu après avoir entré le pseudo
            elif action == "leaderboard":
                leaderboard.display(screen)  # Afficher le leaderboard

def jeu(pseudo):
    """Boucle principale du jeu."""
    player = Player(pseudo)
    leaderboard = Leaderboard()
    fruits = [Fruit(random.choice(list(image_fruit.keys())), random.randint(50, 250)) for _ in range(5)]

    spawn_delay = 1500  
    last_spawn_time = pygame.time.get_ticks()
    difficulty_increment = 1.01

    running = True
    while running:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                key_pressed = pygame.key.name(event.key).upper()
                for fruit in fruits[:]:
                    if fruit.key == key_pressed:
                        player.add_points(fruit)
                        fruits.remove(fruit)
                        fruits.append(Fruit(random.choice(list(image_fruit.keys())), random.randint(50, 250)))

        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time > spawn_delay:
            fruits.append(Fruit(random.choice(list(image_fruit.keys())), random.randint(50, 250)))
            last_spawn_time = current_time
            spawn_delay = max(200, int(spawn_delay / difficulty_increment))

        for fruit in fruits[:]:
            fruit.update()
            if fruit.y > HEIGHT:
                fruits.remove(fruit)
                fruits.append(Fruit(random.choice(list(image_fruit.keys())), random.randint(50, 250)))
            fruit.draw(screen)

        score_text = font.render(f"Score: {player.score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(60)

    # Sauvegarde du score en fin de partie avec le pseudo
    leaderboard.save_score(player.name, player.score)

    # Retour au menu après la partie
    menu_principal()

menu_principal()
