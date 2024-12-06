import pygame
import os
import sys
import importlib
import time

pygame.init()

logs_err = []
bootmanagerloaderconfiginfo = False

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Floppa Os Machine")
run = True

def plat():
    global screen
    picture = pygame.font.SysFont("Arial", 30).render("Floppa OS Machine", False, "White")

    for i in range(3000):
        time.sleep(0.01)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill("Black")
        screen.blit(picture, (screen.get_size()[0]/2-picture.get_size()[0]/2, screen.get_size()[1]/2-picture.get_size()[1]/2))
        pygame.display.update()

def bootmanagerUI():
    global screen, bootmanagerloaderconfiginfo
    bootoverdrives = []
    for over in os.listdir("devices"):
        if os.path.exists(f"devices/{over}/bootloader.py"):
            bootoverdrives.append(over)
    
    font = pygame.font.SysFont("Arial", 25)

    fontsobjects = []
    a = 0
    for obj in bootoverdrives:
        a += 1
        fontsobjects.append(
            {
                "id": a,
                "Text": f"{obj}",
                "Select": font.render(obj, False, "Blue"),
                "Unselect": font.render(obj, False, "Black")
            }
        )
    
    run = True
    _max = int(len(fontsobjects))
    _min = 1
    _select = 1
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    _select -= 1
                if event.key == pygame.K_DOWN:
                    _select += 1
                if event.key == pygame.K_RETURN:
                    #print(_select)
                    pack = None
                    for ui in fontsobjects:
                        if ui["id"] == _select:
                            pack = ui["Text"]
                            #print(ui["Text"])
                            #print(ui["id"])
                            #print(_select)
                            #print(pack)

                    msconfig = importlib.import_module(f"devices.{pack}.bootloader")
                    run = False
                    bootmanagerloaderconfiginfo = True
                    plat()
                    try:
                        msconfig.Boot(screen, f"devices/{pack}")
                    except Exception as ex:
                        print(f"STOPED 0x00000004C: {ex}")
                
                if _select < _min:
                    _select = _max
                
                if _select > _max:
                    _select = _min
        screen.fill("Grey")
        y = 10
        for obj in fontsobjects:
            if obj["id"] == _select:
                screen.blit(obj["Select"], (10, y))
            else:
                screen.blit(obj["Unselect"], (10, y))
            y += obj["Unselect"].get_size()[1] + 10
        pygame.display.update()

for i in range(300):
    time.sleep(0.01)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F12:
                bootmanagerUI()
    screen.fill("Black")

    pygame.display.update()

if bootmanagerloaderconfiginfo == False:
    for boot in os.listdir("devices"):
        if os.path.exists(f"devices/{boot}/bootloader.py"):
            shell = importlib.import_module(f"devices.{boot}.bootloader")
            run = False
            plat()
            try:
                shell.Boot(screen, f"devices/{boot}")
            except Exception as ex:
                run = True
                logs_err = [f"devices/{boot}", "bootloader.py", f"{ex}"]

    if run == True:
        captions = {"font": pygame.font.SysFont("Arial", 25)}
        captions["1"] = captions["font"].render("The operating system was not found or generates a critical error", False, "White")
        captions["2"] = captions["font"].render("Please install or repair the system", False, "White")
        captions["3"] = pygame.font.SysFont("Arial", 15).render(f"error device: {logs_err[0]}", False, "White")
        captions["4"] = pygame.font.SysFont("Arial", 15).render(f"error script: {logs_err[1]}", False, "White")
        captions["5"] = pygame.font.SysFont("Arial", 15).render(f"error python log: {logs_err[2]}", False, "White")


    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill("Black")

        screen.blit(captions["1"], (10, 10))
        screen.blit(captions["2"], (10, 35))
        screen.blit(captions["3"], (10, 65))
        screen.blit(captions["4"], (10, 85))
        screen.blit(captions["5"], (10, 105))

        pygame.display.update()