import pygame
import math
import sys

class KochCurveGenerator:
    def __init__(self, width=800, height=800):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Koch Curve Generator")
        self.EGGSHELL = (249, 254, 255)
        self.BLOOD = (153, 0, 0)
        self.slider_width = 300
        self.slider_height = 20
        self.slider_x = (width - self.slider_width) // 2
        self.slider_y = height - 50
        self.slider_handle_x = self.slider_x
        self.iterations = 0
        self.font = pygame.font.Font(None, 36)

    def koch_curve(self, start, end, iterations):
        if iterations == 0:
            return [start, end]
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = math.sqrt(dx**2 + dy**2)
        angle = math.atan2(dy, dx)
        third_length = length / 3
        point1 = start
        point2 = (
            start[0] + third_length * math.cos(angle),
            start[1] + third_length * math.sin(angle)
        )
        peak = (
            point2[0] + third_length * math.cos(angle - math.pi/3),
            point2[1] + third_length * math.sin(angle - math.pi/3)
        )
        point3 = (
            start[0] + 2 * third_length * math.cos(angle),
            start[1] + 2 * third_length * math.sin(angle)
        )
        point4 = end
        curve_points = (
            self.koch_curve(point1, point2, iterations-1) +
            self.koch_curve(point2, peak, iterations-1) +
            self.koch_curve(peak, point3, iterations-1) +
            self.koch_curve(point3, point4, iterations-1)
        )
        return curve_points

    def draw_koch_curve(self):
        self.screen.fill(self.EGGSHELL)
        start_point = (100, 400)
        end_point = (700, 400)
        curve_points = self.koch_curve(start_point, end_point, self.iterations)
        if len(curve_points) > 1:
            pygame.draw.lines(self.screen, self.BLOOD, False, curve_points, 2)
        text = self.font.render(f"Iterations: {self.iterations}", True, self.BLOOD)
        self.screen.blit(text, (10, 10))
        pygame.draw.rect(self.screen, (200,200,200), 
                         (self.slider_x, self.slider_y, self.slider_width, self.slider_height))
        pygame.draw.circle(self.screen, self.BLOOD, 
                           (self.slider_handle_x, self.slider_y + self.slider_height//2), 10)

    def run(self):
        clock = pygame.time.Clock()
        dragging_slider = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if (abs(mouse_x - self.slider_handle_x) < 10 and 
                        abs(mouse_y - (self.slider_y + self.slider_height//2)) < 10):
                        dragging_slider = True
                if event.type == pygame.MOUSEBUTTONUP:
                    dragging_slider = False
                if event.type == pygame.MOUSEMOTION and dragging_slider:
                    mouse_x, _ = pygame.mouse.get_pos()
                    self.slider_handle_x = max(self.slider_x, 
                                               min(mouse_x, self.slider_x + self.slider_width))
                    self.iterations = int(((self.slider_handle_x - self.slider_x) / 
                                           self.slider_width) * 8)
            self.draw_koch_curve()
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    KochCurveGenerator().run()