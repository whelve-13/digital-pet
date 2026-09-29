import tkinter as tk
from PIL import Image, ImageTk
import random

class DesktopPet:
    def __init__(self):
        self.root = tk.Tk()

        # Frameless, transparent, always on top
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", "white")
        self.root.config(bg="white")

        # Load Pet Image
        raw_img = Image.open("pet.png").convert("RGBA")
        raw_img = raw_img.resize((190,210), Image.Resampling.LANCZOS)
        self.pet_img = ImageTk.PhotoImage(raw_img)

        # Main Pet Label
        self.label = tk.Label(self.root, image=self.pet_img, bg="white", bd=0)
        self.label.pack()

        # Speech Bubble Label
        self.bubble = tk.Label(
            self.root, text="", bg="#FFF8DC", fg="#333333",
            font=("Arial", 10, "bold"), relief="solid", bd=1, padx=6, pady=3
        )

        # Initial Position (bottom right above taskbar)
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        self.x = screen_w - 200
        self.y = screen_h - 180
        self.root.geometry(f"+{self.x}+{self.y}")

        # Dragging listeners
        self.label.bind("<Button-1>", self.start_drag)
        self.label.bind("<B1-Motion>", self.do_drag)
        self.label.bind("<Double-Button-1>", lambda e: self.say("You poked me! 😊"))

        # Reminders list
        self.messages = [
            "Drink some water! 💧",
            "Stretch your back! 🧘",
            "Rest your eyes for 20s! 👀",
            "You're doing great! ✨",
            "Take a deep breath! 🌿"
        ]

        # Start loops
        self.move_pet()
        self.schedule_reminder()

    def start_drag(self, event):
        self.drag_x = event.x
        self.drag_y = event.y

    def do_drag(self, event):
        self.x += event.x - self.drag_x
        self.y += event.y - self.drag_y
        self.root.geometry(f"+{self.x}+{self.y}")

    def say(self, text):
        self.bubble.config(text=text)
        self.bubble.pack(side="top", before=self.label)
        # Hide bubble after 4 seconds
        self.root.after(4000, self.bubble.pack_forget)

    def move_pet(self):
        # Small random wander step
        step = random.choice([-5, -2, 0, 2, 5])
        screen_w = self.root.winfo_screenwidth()
        self.x = max(20, min(screen_w - 150, self.x + step))
        self.root.geometry(f"+{self.x}+{self.y}")
        # Repeat every 400ms
        self.root.after(400, self.move_pet)

    def schedule_reminder(self):
        self.say(random.choice(self.messages))
        # Popup every 5 minutes (300,000 ms)
        self.root.after(300000, self.schedule_reminder)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    pet = DesktopPet()
    pet.run()