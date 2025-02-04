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
RED = (255, 0, 0)

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

# Nombre max de fruits simultanés à l'écran
MAX_FRUITS = 3
PENALTY_POINTS = 50  # Pénalité en cas d'erreur

class Fruit:
    def __init__(self, name, points):
        self.name = name
        self.image = image_fruit[name]
        self.x = random.randint(100, WIDTH - 100)
        self.y = HEIGHT
        self.vx = random.randint(-3, 3)
        self.vy = random.randint(-15, -10)
        self.gravity = 0.5
        self.key = random.choice(["A", "Z", "E", "R", "T", "Y"])
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

    def add_points(self, points):
        self.score = max(0, self.score + points)  # Empêche le score d'être négatif

def jeu(pseudo):
    """Boucle principale du jeu."""
    player = Player(pseudo)
    leaderboard = Leaderboard()
    fruits = [Fruit(random.choice(list(image_fruit.keys())), random.randint(50, 250)) for _ in range(2)]

    spawn_delay = 1500  
    last_spawn_time = pygame.time.get_ticks()
    difficulty_increment = 1.01
    wrong_key_pressed = False  # Pour l'effet d'erreur

    running = True
    while running:
        screen.fill(RED if wrong_key_pressed else WHITE)  # Clignote en rouge si erreur
        wrong_key_pressed = False  # Réinitialise après affichage

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                key_pressed = pygame.key.name(event.key).upper()
                fruit_found = False
                
                for fruit in fruits[:]:
                    if fruit.key == key_pressed:
                        player.add_points(fruit.points)
                        fruits.remove(fruit)
                        fruit_found = True
                        break  # On arrête la boucle dès qu'on trouve le bon fruit
                
                if not fruit_found:  
                    player.add_points(-PENALTY_POINTS)  # Pénalité si mauvaise touche
                    wrong_key_pressed = True  # Active le clignotement rouge

        current_time = pygame.time.get_ticks()
        
        # Vérifier si on peut ajouter un fruit
        if len(fruits) < MAX_FRUITS and current_time - last_spawn_time > spawn_delay:
            fruits.append(Fruit(random.choice(list(image_fruit.keys())), random.randint(50, 250)))
            last_spawn_time = current_time
            spawn_delay = max(500, int(spawn_delay / difficulty_increment))  # Augmente la difficulté

        for fruit in fruits[:]:
            fruit.update()
            if fruit.y > HEIGHT:
                fruits.remove(fruit)
            fruit.draw(screen)

        # Afficher le score
        score_text = font.render(f"Score: {player.score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(60)

    # Sauvegarde du score en fin de partie
    leaderboard.save_score(player.name, player.score)
    fin_jeu(player)

def fin_jeu(player):
    """Affiche l'écran de fin et attend l'entrée de l'utilisateur."""
    screen.fill(WHITE)
    message = font.render(f"Fin du jeu ! Score: {player.score}", True, BLACK)
    screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - 50))
    message2 = font.render("Appuyez sur Entrée pour retourner au menu", True, BLACK)
    screen.blit(message2, (WIDTH // 2 - message2.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()

    attente = True
    while attente:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    attente = False

    menu_principal()

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
                pseudo = "Joueur"
                jeu(pseudo)
                in_menu = False
            elif action == "leaderboard":
                leaderboard.display(screen)

menu_principal()