import tkinter as tk
from tkinter import font as tkfont
from tkinter.filedialog import askopenfilenames, askdirectory
from tkinter import StringVar
from tkinter import messagebox
from PIL import Image, ImageTk

class WallpaperGenerator(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.title("Compass Desktop")
        self.resizable(False, False)
        # # Designate Height and Width of app
        app_width = 300
        app_height = 250

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)

        self.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        self.frames = {}
        for F in (StartPage, ImagePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        """
        create on screen widgets for GUI
        """
        self.logo = Image.open("compass_desktop.png")
        self.logo = self.logo.resize((200, 115), Image.ANTIALIAS)
        self.logo_image = ImageTk.PhotoImage(self.logo)
        self.logo_label = tk.Label(self, image=self.logo_image)
        self.logo_label.config(anchor="center")
        self.logo_label.pack(pady=10)
        self.label = tk.Label(self, text="Welcome to the Compass Wallpaper Gen!")
        self.label.pack(pady=5)
        self.choose_img = tk.Button(self, text="Get Started", command=lambda: self.controller.show_frame("ImagePage"))
        self.choose_img.pack()


class ImagePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="Step 1: Choose your images")
        self.label.pack(pady=10)
        self.choose_img = tk.Button(self, text="Choose Images", command=self.choose_img_button)
        self.choose_img.pack()

        self.has_files = False
        self.files_text = StringVar()
        self.files_text.set(" ")
        self.directory_label = tk.Label(self, textvariable=self.files_text)
        self.directory_label.pack(pady=10)

    def choose_img_button(self):
        filenames = " "
        filenames = askopenfilenames(filetypes=[("JPEG Images", "*.jpg"), ("JPEG Images 2", "*.jpeg"), ("PNG Images", "*.png")])
        lst = list(filenames)
        if len(lst) < 1:
            print("Must select images")
        else:
            if len(lst) <= 1:
                self.files_text.set(f"{len(lst)} image selected")
                print(self.files_text.get())
                
            else:
                self.files_text.set(f"{len(lst)} images selected")

            if self.has_files == False:
                self.second_label = tk.Label(self, text="-------------------------------------", font='bold')
                self.second_label.pack(pady=2)
                self.second_label = tk.Label(self, text="Step 2: Choose a folder to save the images")
                self.second_label.pack(pady=10)
                self.create_image_btn = tk.Button(self, text="Choose a folder", command=lambda : self.create_image(filenames))
                self.create_image_btn.pack()
                self.has_files = True

    def create_image(self, selected_images):
        """
        create new image by overlaying tech help card on top of selected image
        """
        size = (1366, 768)
        output_img_list = []
        card = Image.open("tech_card.png")
        card = card.resize(size, Image.ANTIALIAS)

        for image in selected_images:
            # print(image)
            image = Image.open(image)
            back_img = image.copy()
            back_img = back_img.resize(size, Image.ANTIALIAS)
            back_img.paste(card, (0, 0), card)
            # back_img.show()
            output_img_list.append(back_img)
        output_directory = askdirectory()
        for image in output_img_list:
            image.save(f"{output_directory}/{output_img_list.index(image)}.png", "png")
        tk.messagebox.showinfo(title="Done!", message=f"Images have been successfully created!\nThey were saved to:\n {output_directory}!")
        self.destroy()

app = WallpaperGenerator()
app.mainloop()