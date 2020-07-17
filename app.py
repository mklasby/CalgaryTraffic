# app.py - view

import tkinter as tk


class App(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        root = tk.Tk()
        BG_COLOUR = "GREY"
        FG_COLOUR = "WHITE"


def main():
    app = App()


if __name__ == "__main__":
    print("Running app.main()...\n")
    main()
