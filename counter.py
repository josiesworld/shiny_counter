import sys
import math
import json
import os.path
from datetime import datetime
from tkinter import *
from tkinter import simpledialog, messagebox
from pynput import keyboard
from pynput.keyboard import Key


class CreateCounter():
    def __init__(self):
        self.root = Tk()
        self.load_counter()
        self.root.overrideredirect(1)
        self.allow_input = 0
        self.allow_reposition = 0
        self.quit_inputs = 0
        self.allow_alphabet = 0
        self.lock_all_inputs = 0

        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()

        self.download_fonts()
        self.L = Label(self.root, text=self.counter, foreground='white', font=(self.font_style, self.font_size))
        self.L.focus_set()
        self.L.pack()

        # Need window to appear so we can size it then we need to update again to position it correctly.
        self.L.update_idletasks()
        self.size_window()
        self.L.update_idletasks()

        self.start_time = datetime.now()
        self.root.attributes('-topmost',True)
        self.root.wm_attributes('-transparentcolor', self.root['bg'])
        self.root.mainloop()

    def on_press(self,key):
        try:
            # Allow us to stop this app from gathering inputs if we need to type.
            if hasattr(key, "char"):
                if key.char == '?':
                    self.lock_all_inputs = not self.lock_all_inputs
            if not self.lock_all_inputs:
                self.update_label(key)
        except Exception as e:
            print(e)
            return

    def update_label(self,key):
        if hasattr(key,'vk'): 
            if key.vk > 95 and key.vk < 106:
                key.char = str(key.vk - 96)
            if key.vk == 110:
                self.allow_input = not self.allow_input
        
        if hasattr(key,"name"):
            if key.name in ["up", "down", "left", "right"] and self.allow_reposition:
                if key.name == 'up':
                    self.y_init = "top"
                elif key.name == 'down':
                    self.y_init = "bottom"
                elif key.name == 'right':
                    self.x_init = "right"
                elif key.name == 'left':
                    self.x_init = "left"
                self.save_fonts()


        #if key == Key.enter:
        #    key.char = '+'

        if hasattr(key,"char"):

            if key.char == '+':
                self.counter += 1
            elif key.char == '-' and self.counter > 0:
                self.counter -= 1
            elif key.char in ('*'):
                self.counter = 0
            elif key.char in ['0','1','2','3','4','5','6','7','8','9'] and self.allow_input:
                if self.counter == 0:
                    self.counter = int(key.char)
                else:
                    self.counter = int(f"{self.counter}{key.char}")
            elif key.char == '|':
                self.allow_alphabet = not self.allow_alphabet
            
            # So that we can type stuff on other apps without affecting counter.
            if self.allow_alphabet:
                if key.char == "f":
                    temp_win = Tk()
                    temp_win.withdraw()
                    temp_win.focus_set()
                    answer = simpledialog.askinteger("Font Size","Input a font size: ", parent=temp_win, minvalue=15, maxvalue=100)
                    temp_win.destroy()
                    self.font_size = answer
                    self.L.config(font=(self.font_style,self.font_size))
                    self.save_fonts()
                
                elif key.char == 'p':
                    self.allow_reposition = not self.allow_reposition
                elif key.char == 'q':
                    if (datetime.now() - self.start_time).total_seconds() < 1:
                        self.quit_inputs += 1
                    self.start_time = datetime.now()
                    if self.quit_inputs >= 2:
                        self.save_counter()
                        self.root.destroy()
                elif key.char == 'r':
                    self.load_counter()
                elif key.char == 's':
                    self.save_counter()

        self.L['text'] = self.counter
        self.size_window()
        return

    def save_counter(self):
        with open('savedata.txt', 'w+') as f:
            f.write(str(self.counter))


    def load_counter(self):
        if os.path.isfile('savedata.txt'):
            with open('savedata.txt', 'r+') as f:
                saved_counter = f.read()
                self.counter = int(saved_counter)
        else:
            self.counter = 0
        return

    def size_window(self):
        if self.y_init.lower() == "top":
            y_pos = 0
        else:
            y_pos = self.root.winfo_screenheight() - self.root.winfo_height() - 25
        if self.x_init.lower() == "left":
            x_pos = 0
        elif self.root.winfo_width() == 0 or self.counter < 10:
            x_pos = self.root.winfo_screenwidth() - self.font_size
        elif self.counter >= 10:
            x_pos = self.root.winfo_screenwidth() - self.root.winfo_width() #- root.font_size

        self.root.geometry('+%d+%d'%(x_pos,y_pos))

        return

    def download_fonts(self):
        style = {}
        if os.path.isfile('style.json'):
            with open('style.json', 'r') as f:
                style = json.loads(f.read())
        self.font_style = style.get("font","Helvetica")
        self.font_size = style.get("size",36)
        self.x_init = style.get("x_pos","right")
        self.y_init = style.get("y_pos","bottom")
        return

    def save_fonts(self):
        style = {
            "font": self.font_style,
            "size": self.font_size,
            "x_pos": self.x_init,
            "y_pos": self.y_init
        }
        with open('style.json', 'w') as f:
            f.write(json.dumps(style, indent=4))


if __name__ == "__main__":
    CreateCounter()