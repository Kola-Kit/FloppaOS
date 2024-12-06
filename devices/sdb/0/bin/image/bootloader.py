import pygame
import importlib
import sys

class Boot():
    def __init__(self, screen, mount):
        self.screen = screen
        self.mount = mount
        self.imp = importlib.import_module(f"{self.mount.replace("/", ".")}.null.bin.imp")

        self.font = pygame.font.SysFont("Arial", 25)
        self.a = self.font.render("OS is started!", False, "White")

        self.loop()

    def loop(self):
      self.run = True

      while self.run:
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        self.screen.fill("Black")
        self.screen.blit(self.a, (self.screen.get_size()[0]/2-self.a.get_size()[0], self.screen.get_size()[1]/2-self.a.get_size()[1]))
        pygame.display.update()
