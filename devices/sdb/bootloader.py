import pygame
import pygame_gui
import sys
import importlib
import os

class Boot():
    def __init__(self, screen, mount):
        self.screen = screen
        self.mount = mount
        self.sva = False

        """for boot in os.listdir("devices"):
            if os.path.exists(f"devices/{boot}/bootloader.py"):
                if "devices/"+boot != mount:
                    #print(boot)
                    shell = importlib.import_module(f"devices.{boot}.bootloader")
                    self.sva = True
                    try:
                        if shell.grun == True:
                            shell.Boot(screen, f"devices/{boot}")
                    except:
                        pass"""

        self.bg = pygame.Surface(self.screen.get_size())
        self.manager = pygame_gui.UIManager((800, 600))

        self.setup_programm = importlib.import_module(f"{mount.replace("/", ".")}.0.bin.setup")
        self.setup_programm.UIWindow(self.manager, self.mount)

        if self.sva == False:
            self.loop()

    def loop(self):
        self.run = True
        self.clock = pygame.time.Clock()

        while self.run:
            self.time_delta = self.clock.tick(60)/1000.0
            self.bg.fill("White")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                self.manager.process_events(event)
            
            self.manager.update(self.time_delta)

            self.screen.blit(self.bg, (0, 0))

            self.manager.draw_ui(self.screen)

            pygame.display.update()
