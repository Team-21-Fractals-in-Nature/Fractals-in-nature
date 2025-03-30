import pygame
import math
import sys

class KochSnowflakeGenerator:
    def __init__(self, width=800, height=800):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Koch Snowflake Generator")
        
        # Colors
        self.EGGSHELL = (249, 254, 255)
        self.BLOOD = (153, 0, 0)
        
        # Slider setup
        self.slider_width = 300
        self.slider_height = 20
        self.slider_x = (width - self.slider_width) // 2
        self.slider_y = height - 50
        self.slider_handle_x = self.slider_x
        self.iterations = 0
        
        # Font for iteration, area, and perimeter display
        self.font = pygame.font.Font(None, 36)

    def koch_curve_points(self, start, end, iterations):
        """Generate Koch Curve points recursively"""
        if iterations == 0:
            return [start, end]
        
        # Calculate vector length and angle
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = math.sqrt(dx**2 + dy**2)
        angle = math.atan2(dy, dx)
        
        # Divide line into thirds
        third_length = length / 3
        
        # Calculate intermediate points
        point1 = start
        point2 = (
            start[0] + third_length * math.cos(angle),
            start[1] + third_length * math.sin(angle)
        )
        
        # Calculate peak point 
        peak = (
            point2[0] + third_length * math.cos(angle - math.pi/3),
            point2[1] + third_length * math.sin(angle - math.pi/3)
        )
        
        point3 = (
            start[0] + 2 * third_length * math.cos(angle),
            start[1] + 2 * third_length * math.sin(angle)
        )
        point4 = end
        
        # Recursively generate points for each segment
        curve_points = (
            self.koch_curve_points(point1, point2, iterations-1) +
            self.koch_curve_points(point2, peak, iterations-1) +
            self.koch_curve_points(peak, point3, iterations-1) +
            self.koch_curve_points(point3, point4, iterations-1)
        )
        
        return curve_points

    def generate_koch_snowflake(self, side_length, iterations):
        """Generate Koch Snowflake points"""
        # Calculate equilateral triangle vertices
        height = side_length * math.sqrt(3) / 2
        center_x, center_y = self.width // 2, self.height // 2
        
        # Three vertices of the initial equilateral triangle
        top = (center_x, center_y - height * 2/3)
        bottom_left = (center_x - side_length/2, center_y + height/3)
        bottom_right = (center_x + side_length/2, center_y + height/3)
        
        # Generate Koch curve for each side of the triangle
        snowflake_points = []
        sides = [
            (bottom_left, top),
            (top, bottom_right),
            (bottom_right, bottom_left)
        ]
        
        for start, end in sides:
            # Generate points for each side, rotating to create snowflake sides
            side_points = self.koch_curve_points(start, end, iterations)
            snowflake_points.extend(side_points)
        
        return snowflake_points

    def calculate_koch_snowflake_area(self, iterations):
        """
        Calculate the area of the Koch snowflake using the provided formula:
        a_0 * (1 + (1/3) * sum((4/9)^k for k in range(n)))
        
        Where:
        - a_0 is the area of the initial equilateral triangle
        - n is the number of iterations
        """
        # Area of equilateral triangle with side length 1
        a0 = math.sqrt(3) / 4
        
        # Calculate the sum term
        sum_term = sum((4/9) ** k for k in range(iterations))
        
        # Apply the full formula
        area = a0 * (1 + (1/3) * sum_term)
        
        return area

    def calculate_koch_snowflake_perimeter(self, iterations):
        """
        Calculate the perimeter of the Koch snowflake.
        The perimeter increases multiplicatively with each iteration.
        """
        # Initial triangle perimeter (3 sides of length 1)
        initial_perimeter = 3
        
        # Each iteration increases the perimeter by a factor of 4/3
        perimeter = initial_perimeter * (4/3) ** iterations
        
        return perimeter

    def draw_koch_snowflake(self):
        """Draw the Koch Snowflake"""
        self.screen.fill(self.EGGSHELL)
        
        # Generate snowflake points
        side_length = 400  # Adjust based on screen size
        snowflake_points = self.generate_koch_snowflake(side_length, self.iterations)
        
        # Draw the snowflake
        if len(snowflake_points) > 1:
            pygame.draw.lines(self.screen, self.BLOOD, True, snowflake_points, 2)
        
        # Draw iteration text
        text = self.font.render(f"Iterations: {self.iterations}", True, self.BLOOD)
        self.screen.blit(text, (10, 10))
        
        # Calculate and draw area
        area = self.calculate_koch_snowflake_area(self.iterations)
        area_text = self.font.render(f"Area: {area:.4f}", True, self.BLOOD)
        self.screen.blit(area_text, (10, 50))
        
        # Calculate and draw perimeter
        perimeter = self.calculate_koch_snowflake_perimeter(self.iterations)
        perimeter_text = self.font.render(f"Perimeter: {perimeter:.4f}", True, self.BLOOD)
        self.screen.blit(perimeter_text, (10, 90))
        
        # Draw slider
        pygame.draw.rect(self.screen, (200,200,200), 
                         (self.slider_x, self.slider_y, self.slider_width, self.slider_height))
        pygame.draw.circle(self.screen, self.BLOOD, 
                           (self.slider_handle_x, self.slider_y + self.slider_height//2), 10)

    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        dragging_slider = False
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Slider interaction
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if mouse is over slider handle
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if (abs(mouse_x - self.slider_handle_x) < 10 and 
                        abs(mouse_y - (self.slider_y + self.slider_height//2)) < 10):
                        dragging_slider = True
                
                if event.type == pygame.MOUSEBUTTONUP:
                    dragging_slider = False
                
                if event.type == pygame.MOUSEMOTION and dragging_slider:
                    # Update slider position and iterations
                    mouse_x, _ = pygame.mouse.get_pos()
                    self.slider_handle_x = max(self.slider_x, 
                                               min(mouse_x, self.slider_x + self.slider_width))
                    
                    # Map slider position to iterations (0-8)
                    self.iterations = int(((self.slider_handle_x - self.slider_x) / 
                                           self.slider_width) * 8)
            
            # Clear and redraw
            self.draw_koch_snowflake()
            pygame.display.flip()
            clock.tick(30)

# Run the Koch Snowflake generator
if __name__ == "__main__":
    KochSnowflakeGenerator().run()