from tkinter import *

def main():
    root = Tk()
    root.title('Chess Game')
    icon = PhotoImage(file="./icons/mainIcon.png")
    root.iconphoto(False, icon)
    root.geometry("800x800")
    root.resizable(False, False)
    root.mainloop()

if __name__ == "__main__":
    main()