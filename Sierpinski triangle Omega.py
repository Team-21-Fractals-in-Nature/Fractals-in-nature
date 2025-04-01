import pygame
import sys

class SierpinskiTriangle:
    def __init__(self, width=800, height=800):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sierpinski Triangle Generator")
        self.EGGSHELL = (249, 254, 255)
        self.BLOOD = (153, 0, 0)
        self.initial_triangle = [
            (width // 2, 100),     
            (100, height - 100),   
            (width - 100, height - 100)  
        ]
        self.iterations = 0
        self.font = pygame.font.Font(None, 36)

    def generate_triangles(self, iterations):
        triangles = [self.initial_triangle]
        for _ in range(iterations):
            new_triangles = []
            for triangle in triangles:
                a, b, c = triangle
                mid_ab = (
                    (a[0] + b[0]) // 2,
                    (a[1] + b[1]) // 2
                )
                mid_bc = (
                    (b[0] + c[0]) // 2,
                    (b[1] + c[1]) // 2
                )
                mid_ca = (
                    (c[0] + a[0]) // 2,
                    (c[1] + a[1]) // 2
                )
                new_triangles.extend([
                    (a, mid_ab, mid_ca),
                    (mid_ab, b, mid_bc),
                    (mid_ca, mid_bc, c)
                ])
            triangles = new_triangles
        return triangles

    def draw_triangles(self, triangles):
        self.screen.fill(self.EGGSHELL)
        for triangle in triangles:
            pygame.draw.polygon(self.screen, self.BLOOD, triangle, 1)
        text = self.font.render(f"Iterations: {self.iterations}", True, self.BLOOD)
        self.screen.blit(text, (10, 10))

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.iterations < 10:
                        self.iterations += 1
                    elif event.key == pygame.K_DOWN and self.iterations > 0:
                        self.iterations -= 1
            triangles = self.generate_triangles(self.iterations)
            self.draw_triangles(triangles)
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    SierpinskiTriangle().run()