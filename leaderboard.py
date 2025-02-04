import pygame

class Leaderboard:
    def __init__(self, filename="score.txt"):
        self.filename = filename

    def save_score(self, player_name, score):
        """Sauvegarde un score dans le fichier."""
        with open(self.filename, "a") as file:
            file.write(f"{player_name}:{score}\n")

    def load_scores(self):
        """Charge et trie les scores en ordre décroissant."""
        try:
            with open(self.filename, "r") as file:
                scores = [line.strip().split(":") for line in file.readlines()]
                scores = [(name, int(score)) for name, score in scores]
                scores.sort(key=lambda x: x[1], reverse=True)  # Trier par score décroissant
                return scores
        except FileNotFoundError:
            return []

    def display(self, screen):
        """Affiche le leaderboard."""
        screen.fill((139, 69, 19))  # Fond boisé
        font = pygame.font.Font(None, 36)
        scores = self.load_scores()
        
        title = font.render("🏆 Leaderboard 🏆", True, (255, 255, 255))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 20))

        y_offset = 80
        for i, (name, score) in enumerate(scores[:10]):  # Afficher les 10 meilleurs scores
            text = font.render(f"{i + 1}. {name} - {score} pts", True, (255, 255, 255))
            screen.blit(text, (50, y_offset))
            y_offset += 40

        pygame.display.flip()
        self.wait_for_exit()

    def wait_for_exit(self):
        """Attend un clic ou une touche pour fermer le leaderboard."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    running = False
