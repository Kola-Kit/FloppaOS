import pygame
import pygame_gui
import os
import json
import time
import threading
import shutil

import pygame_gui.elements.ui_progress_bar

class Mount(pygame_gui.elements.UIWindow):
    def __init__(self, manager, main):
        self.main = main
        self.base_manager = manager
        self.root_sel = "/"
        super().__init__(
            manager=manager,
            window_display_title="Create Mount",
            rect=pygame.Rect(10, 10, 350, 250),
            resizable=False
        )
        
        self.CurrentPartion = pygame_gui.elements.UITextBox(
            f"Selected Partion: {self.main.abc3[0]}",
            manager=self.base_manager,
            container=self,
            relative_rect=pygame.Rect(10, 10, 330, 40)
        )

        self.TypeMount = pygame_gui.elements.UIDropDownMenu(
            manager=self.base_manager,
            container=self,
            options_list=["/", "/boot", "/home", "/lib", "GPT", "fat32"],
            starting_option="/",
            relative_rect=pygame.Rect(10, 100, 330, 40)
        )

        self.Mounted = pygame_gui.elements.UIButton(
            manager=self.base_manager,
            container=self,
            relative_rect=pygame.Rect(270, 170, 70, 40),
            text="Mount"
        )
    
    def process_event(self, event):
        super().process_event(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.Mounted:
                self.hide()
                self.kill()
                self.main.real(f"devices/{self.main.abc3[1]}/{self.main.abc3[0].split(":")[2]}", self.root_sel)
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            self.root_sel = event.text
    
    def update(self, time_delta):
        super().update(time_delta)

class UIWindow(pygame_gui.elements.UIWindow):
    def __init__(self, manager, mount):
        super().__init__(
            manager=manager,
            window_display_title="setup",
            rect=pygame.Rect(45, 45, 700, 500),
            resizable=False
        )

        self.setup = 0
        self.old_setup = None
        self.base_manager = manager
        self.elements_setup = []
        self.mount = mount
        self.value_s = 0

        self.abc2 = []
        self.abc3 = []
        
        self.SystemSetupRoot = {
            "/": None,
            "/boot": None,
            "/home": None,
            "/lib": None,
            "GPT": None
        }

        for disk in os.listdir("devices"):
            if f"devices/{disk}" != self.mount:
                abc2rc1 = json.loads(open(f"devices/{disk}/current.json").read())
                self.abc2.append("Disk:" + disk + f"-Name:{abc2rc1["Name"]}-Mem:{abc2rc1["Memory"]}")
                for partion in os.listdir(f"devices/{disk}"):
                    if os.path.isdir(f"devices/{disk}/{partion}"):
                        if partion != "__pycache__":
                            self.abc2.append(f".Disk:{disk}-->Partion:{partion}")

    def update(self, time_delta):
        self.chek_var()
        super().update(time_delta)
    
    def chek_var(self):
        if self.setup != self.old_setup:
            for serv in self.elements_setup:
                serv.hide()
                serv.kill()
            self.elements_setup = []
            self.old_setup = self.setup
            self.chek()
    
    def process_event(self, event):
        super().process_event(event)

        if self.setup == 0:
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.elements_setup[1]:
                    self.setup += 1
        elif self.setup == 1:
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.elements_setup[0]:
                    self.setup += 1
            if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                if event.ui_element == self.elements_setup[2]:
                    self.abc3 = [event.text, event.text.split(":")[1].split("-")[0]]
                    if event.text[0] == ".":
                        self.elements_setup[4].enable()
                        self.elements_setup[3].disable()
                        self.elements_setup[5].disable()
                    else:
                        self.elements_setup[4].disable()
                        self.elements_setup[3].enable()
                        self.elements_setup[5].enable()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.elements_setup[3]:
                    if self.elements_setup[3].is_enabled == True:
                        self.NewPartionTable()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.elements_setup[4]:
                    if self.elements_setup[4].is_enabled == True:
                        self.MountPartion()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.elements_setup[5]:
                    if self.elements_setup[5].is_enabled == True:
                        self.FormatDisk()

    def process_event_mount(self, event):
        self.child.process_event(event)
    
    def update_mount(self, time_delta):
        self.child.update(time_delta)
    
    def FormatDisk(self):
        for sh in os.listdir(f"devices/{self.abc3[1]}"):
            if sh != "current.json":
                if os.path.isdir(f"devices/{self.abc3[1]}/{sh}"):
                    shutil.rmtree(f"devices/{self.abc3[1]}/{sh}")
                else:
                    os.remove(f"devices/{self.abc3[1]}/{sh}")
        
        self.elements_setup[2].hide()
        self.elements_setup[2].kill()

        self.abc2 = []
        for disk in os.listdir("devices"):
            if f"devices/{disk}" != self.mount:
                abc2rc1 = json.loads(open(f"devices/{disk}/current.json").read())
                self.abc2.append("Disk:" + disk + f"-Name:{abc2rc1["Name"]}-Mem:{abc2rc1["Memory"]}")
                for partion in os.listdir(f"devices/{disk}"):
                    if os.path.isdir(f"devices/{disk}/{partion}"):
                        if partion != "__pycache__":
                            self.abc2.append(f".Disk:{disk}-->Partion:{partion}")

        self.elements_setup[2] = pygame_gui.elements.UISelectionList(
            manager=self.base_manager,
            container=self,
            relative_rect=pygame.Rect((10, 60, 680, 200)),
            item_list=self.abc2
        )

    
    def real(self, root_dir, root_type):
        if root_type != "GPT":
            self.SystemSetupRoot[root_type] = root_dir
        else:
            rc = f"{root_dir}".split("/")
            final = ""

            okolo = -1
            m = int(len(rc))
            for add in range(m-1):
                okolo += 1
                if add != m:
                    if m-2 == add:
                        final += f"{rc[okolo]}"
                    else:
                        final += f"{rc[okolo]}/"

            self.SystemSetupRoot[root_type] = final

        self.elements_setup[5].hide()
        self.elements_setup[5].kill()
        self.elements_setup[5] = pygame_gui.elements.UISelectionList(
            manager=self.base_manager,
            container=self,
            relative_rect=pygame.Rect(10, 320, 250, 100),
            item_list=[f"/ = {self.SystemSetupRoot["/"]}",
                       f"/boot = {self.SystemSetupRoot["/boot"]}",
                       f"/home = {self.SystemSetupRoot["/home"]}",
                       f"/lib = {self.SystemSetupRoot["/lib"]}",
                       f"GPT = {self.SystemSetupRoot["GPT"]}"]
        )

        if self.SystemSetupRoot["/"] != None:
            self.elements_setup[0].enable()

    def MountPartion(self):
        Mount(self.base_manager, self)
    
    def NewPartionTable(self):
        res = -1
        te = False
        for partion in os.listdir(f"devices/{self.abc3[1]}"):
            res += 1
            te = True
        if te == False:
            res = 0
        res = f"{res}"
        fin = ""
        table = {
            "0": "null",
            "1": "one",
            "2": "two",
            "3": "tree",
            "4": "four",
            "5": "five",
            "6": "six",
            "7": "seven",
            "8": "eight",
            "9": "nine",
        }
        for ch in list(res):
            fin += table[ch]
        
        os.mkdir(f"devices/{self.abc3[1]}/{fin}")

        self.elements_setup[2].hide()
        self.elements_setup[2].kill()

        self.abc2 = []
        for disk in os.listdir("devices"):
            if f"devices/{disk}" != self.mount:
                abc2rc1 = json.loads(open(f"devices/{disk}/current.json").read())
                self.abc2.append("Disk:" + disk + f"-Name:{abc2rc1["Name"]}-Mem:{abc2rc1["Memory"]}")
                for partion in os.listdir(f"devices/{disk}"):
                    if os.path.isdir(f"devices/{disk}/{partion}"):
                        if partion != "__pycache__":
                            self.abc2.append(f".Disk:{disk}-->Partion:{partion}")

        self.elements_setup[2] = pygame_gui.elements.UISelectionList(
            manager=self.base_manager,
            container=self,
            relative_rect=pygame.Rect((10, 60, 680, 200)),
            item_list=self.abc2
        )

        #self.elements_setup[3].show()

    def chek(self):
        if self.setup == 0:
            self.abc1 = pygame.Rect(0, 0, 150, 40)
            self.abc1.bottomright = (-30, -20)
            self.elements_setup.append(pygame_gui.elements.UITextBox(
                "Welcome To Floppa OS Setup",
                container=self,
                manager=self.base_manager,
                relative_rect=pygame.Rect(10, 10, 220, 40)
            ))
            self.elements_setup.append(pygame_gui.elements.UIButton(
                manager=self.base_manager,
                container=self,
                relative_rect=self.abc1,
                text="Next",
                anchors={'right': 'right','bottom': 'bottom'}
            ))

            self.last = 0
            self.samp = []
        elif self.setup == 1:
            self.abc1 = pygame.Rect(0, 0, 150, 40)
            self.abc1.bottomright = (-30, -20)
            self.elements_setup.append(pygame_gui.elements.UIButton(
                manager=self.base_manager,
                container=self,
                relative_rect=self.abc1,
                text="Next",
                anchors={'right': 'right','bottom': 'bottom'}
            ))
            self.elements_setup[0].disable()
            self.elements_setup.append(pygame_gui.elements.UITextBox(
                "Select the drive to install",
                container=self,
                manager=self.base_manager,
                relative_rect=pygame.Rect(10, 10, 220, 40)
            ))
            self.elements_setup.append(pygame_gui.elements.UISelectionList(
                manager=self.base_manager,
                container=self,
                relative_rect=pygame.Rect((10, 60, 680, 200)),
                item_list=self.abc2
            ))
            self.elements_setup.append(pygame_gui.elements.UIButton(
                manager=self.base_manager,
                container=self,
                relative_rect=pygame.Rect(10, 260, 200, 40),
                text="New Partition Table"
            ))
            self.elements_setup[3].disable()
            self.elements_setup.append(pygame_gui.elements.UIButton(
                manager=self.base_manager,
                container=self,
                relative_rect=pygame.Rect(230, 260, 200, 40),
                text="Change"
            ))
            self.elements_setup[4].disable()
            self.elements_setup.append(pygame_gui.elements.UIButton(
                manager=self.base_manager,
                container=self,
                relative_rect=pygame.Rect(450, 260, 200, 40),
                text="Format"
            ))
            self.elements_setup[5].disable()
            self.elements_setup.append(pygame_gui.elements.UISelectionList(
                manager=self.base_manager,
                container=self,
                relative_rect=pygame.Rect(10, 320, 250, 100),
                item_list=[f"/ = {self.SystemSetupRoot["/"]}",
                           f"/boot = {self.SystemSetupRoot["/boot"]}",
                           f"/home = {self.SystemSetupRoot["/home"]}",
                           f"/lib = {self.SystemSetupRoot["/lib"]}",
                           f"GPT = {self.SystemSetupRoot["GPT"]}"]
            ))

            self.last = 0
            self.samp = []
        elif self.setup == 2:
            
            self.elements_setup.append(pygame_gui.elements.UIImage(
                relative_rect=pygame.Rect(0, 0, 700, 300),
                image_surface=pygame.transform.scale(pygame.image.load(f"{self.mount}/0/bin/setup.png"), (700, 300)),
                manager=self.base_manager,
                container=self
            ))

            self.elements_setup.append(pygame_gui.elements.UITextBox(
                "Copying Files...",
                manager=self.base_manager,
                container=self,
                relative_rect=pygame.Rect(10, 310, 190, 40)
            ))

            self.elements_setup.append(pygame_gui.elements.UIStatusBar(
                manager=self.base_manager,
                container=self,
                relative_rect=pygame.Rect(10, 360, 680, 50),
                percent_method=self.setup_get_var
            ))

            self.last = 0
            self.samp = []

            threading.Thread(target=self.cop).start()
        
    def setup_get_var(self):
        return float(self.value_s)

    def cop(self):
        """
        shutil.copytree(f"{self.mount}/0/bin/image/root", f"{self.SystemSetupRoot["/"]}", dirs_exist_ok=True)
        self.value_s += 25
        time.sleep(1)
        shutil.copytree(f"{self.mount}/0/bin/image/boot", f"{self.SystemSetupRoot["/boot"]}", dirs_exist_ok=True)
        self.value_s += 25
        time.sleep(1)
        shutil.copytree(f"{self.mount}/0/bin/image/home", f"{self.SystemSetupRoot["/home"]}", dirs_exist_ok=True)
        self.value_s += 25
        time.sleep(1)
        shutil.copytree(f"{self.mount}/0/bin/image/libs", f"{self.SystemSetupRoot["/lib"]}", dirs_exist_ok=True)
        self.value_s += 20
        time.sleep(1)
        """
        shutil.copyfile(f"{self.mount}/0/bin/image/bootloader.py", f"{self.SystemSetupRoot["GPT"]}/bootloader.py")
        #self.value_s += 5
        self.value_s = 100
        time.sleep(1)
