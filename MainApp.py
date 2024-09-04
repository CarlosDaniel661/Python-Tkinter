import tkinter as tk
from interfaces.main_app import MainApp
from service.item_service import ItemService

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
    