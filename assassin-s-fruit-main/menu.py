import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.bg_color = (139, 69, 19)  # Marron boisé
        self.button_color = (205, 133, 63)  # Beige clair
        self.text_color = (255, 255, 255)

        # Charger la police
        self.font = pygame.font.Font(None, 40)

        # Définir les boutons
        self.play_button = pygame.Rect(self.width // 2 - 100, self.height // 2 - 50, 200, 50)
        self.leaderboard_button = pygame.Rect(self.width // 2 - 100, self.height // 2 + 20, 200, 50)

    def draw(self):
        self.screen.fill(self.bg_color)
        
        # Dessiner les boutons
        pygame.draw.rect(self.screen, self.button_color, self.play_button, border_radius=10)
        pygame.draw.rect(self.screen, self.button_color, self.leaderboard_button, border_radius=10)

        # Ajouter du texte sur les boutons
        self.draw_text("Jouer", self.play_button)
        self.draw_text("Leaderboard", self.leaderboard_button)

        pygame.display.flip()

    def draw_text(self, text, rect):
        text_surface = self.font.render(text, True, self.text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.collidepoint(event.pos):
                return "play"
            elif self.leaderboard_button.collidepoint(event.pos):
                return "leaderboard"
        return None
