# Import required packages and modules
#GUI
import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image
from tkinter.font import NORMAL
from tkinter.messagebox import *
from incognitobit.Steganography import Steganography
from tkinter import Tk, CHAR, WORD, INSERT, DISABLED, filedialog, messagebox, scrolledtext

# Application class has all functionalities of GUI
class Application(Steganography):

    # Application intializer for all tabs
    def __init__(self):
        try:
            #variable intilization
            self.__buffer = 'None'
            self.__cover_filepath = 'None'
            #Main Window Setup
            self.__app = tk.Tk()      
            self.__app.geometry('800x500')
            self.__app.title("Image Steganography using RSA algo and LSB technique")
            self.__app.resizable(False, False)
            self.__app.tk.call('wm', 'iconphoto', Tk._w, ImageTk.PhotoImage(Image.open('incognitobit/images/title.ico')))
            #Tab creation
            self.__tabs = ttk.Notebook(self.__app)
            self.__createEncryptionTab()
            self.__createDecryptionTab()
            self.__createAboutTab()
            self.__tabs.pack(expand=2, fill="both")
            self.__cover_filepath = None
            self.__stego_filepath = None
            self.__app.mainloop() 
        except:
            messagebox.showerror("Oops! some error has occurred")
            self.__app.destroy()

    # Create encryption tab
    def __createEncryptionTab(self):
        self.__encryption_tab = tk.Frame(self.__tabs)
        self.__tabs.add(self.__encryption_tab, text="Encryption")
        self.__generateCanvas()
        self.__uploadCoverImageButton()
        self.__saveStegoImageButton()
        self.__messageInput()
        self.__uploadTextFileButton()
        self.__resetButton(self.__encryption_tab, 160, 300)
        self.__stegoGenerateButton()
        self.__exitButton(self.__encryption_tab, 400, 300)

    # Generate frames in encryption tab
    def __generateCanvas(self):
        self.__bg_frame = tk.Frame(self.__encryption_tab, bg="black", height=180, width=598)
        self.__bg_frame.pack()
        self.__bg_frame.pack_propagate(0)
        self.__bg_frame.place(x=1, y=2)
        self.__cover_frame = tk.Frame(self.__encryption_tab, bg="white", height = 178, width=300)
        self.__cover_frame.pack()
        self.__cover_frame.pack_propagate(0)
        self.__cover_frame.place(x=2, y=3)
        self.__stego_frame = tk.Frame(self.__encryption_tab, bg="white", height = 178, width=292)
        self.__stego_frame.pack()
        self.__stego_frame.pack_propagate(0)
        self.__stego_frame.place(x=303, y=3)

    # Action on clicking upload button in encryption tab
    def __onClickuploadCoverImageButton(self):
        self.__buffer = str(filedialog.askopenfile(filetypes=[("PNG Images", "*.png")]))
        if (self.__buffer == "None" and self.__cover_filepath == "None") or self.__buffer != "None":
            self.__cover_filepath = self.__buffer
        else:
            return
        self.__cover_filepath = self.__cover_filepath[self.__cover_filepath.find("'") + 1:]
        self.__cover_filepath = self.__cover_filepath[:self.__cover_filepath.find("'")]
        self.__cover_img = Image.open(self.__cover_filepath)
        self.__cover_img = self.__cover_img.resize((298, 176))
        self.__cover_img = ImageTk.PhotoImage(self.__cover_img)
        self.__cover_panel = tk.Label(self.__encryption_tab, image=self.__cover_img, height=172, width=296)
        self.__cover_panel.place(x=2, y=3.5)

    # Create upload cover image button in encryption tab
    def __uploadCoverImageButton(self):
        self.__upload_img_btn = tk.Button(self.__encryption_tab, text="Upload Image", command=self.__onClickuploadCoverImageButton)
        self.__upload_img_btn.place(x=110, y=194)

    # Action on clicking save stego image button
    def __onClickSaveStegoImageButton(self):
        self.__stego_filepath = str(filedialog.asksaveasfile(initialfile = 'stego.png', defaultextension=".png",filetypes=[("PNG Images","*.png")]))
        if self.__stego_filepath == "None":
            return
        self.__stego_filepath = self.__stego_filepath[self.__stego_filepath.find("'") + 1:]
        self.__stego_filepath = self.__stego_filepath[:self.__stego_filepath.find("'")]
        self.__stego_object._saveStegoImage(self.__stego_filepath)
        messagebox.showinfo("IncognitoBit", "Stego Image saved successfully")
        self.__onClickResetButton()

    # Create stego image button in encryption tab
    def __saveStegoImageButton(self):
        self.__save_stego_img_btn = tk.Button(self.__encryption_tab, text="Save Stego Image", command=self.__onClickSaveStegoImageButton)
        self.__save_stego_img_btn.place(x=385, y=194)
        self.__save_stego_img_btn["state"] = DISABLED

    # Create message box for taking input from user in encryption tab
    def __messageInput(self):
        self.__message_bg = tk.Frame(self.__encryption_tab, bg="black", height=54, width=486)
        self.__message_bg.pack()
        self.__message_bg.pack_propagate(0)
        self.__padding_left = 109
        self.__padding_top = 235
        self.__message_bg.place(x=self.__padding_left, y=self.__padding_top)
        self.__message_label = tk.Label(self.__encryption_tab, text="Enter the Message")
        self.__message_label.place(x=2.5, y=self.__padding_top)
        self.__message = tk.Text(self.__encryption_tab, undo=True, height=2.5, width=60, wrap=WORD)
        self.__message.place(x=self.__padding_left+1, y=self.__padding_top+1)

    # Action on clicking text file upload button
    def __onClickUploadTextFileButton(self):
        self.__text_filepath = str(filedialog.askopenfile(filetypes=[("Text Files", "*.txt")]))
        if self.__text_filepath == "None":
            return
        self.__text_filepath = self.__text_filepath[self.__text_filepath.find("'") + 1:]
        self.__text_filepath = self.__text_filepath[:self.__text_filepath.find("'")]
        with open(self.__text_filepath, 'r') as f:
            self.__message.insert(1.0, f.read())

    # Create text file upload button in encryption tab
    def __uploadTextFileButton(self):
        self.__upload_txt_btn = tk.Button(self.__encryption_tab, text="Upload Text", command=self.__onClickUploadTextFileButton)
        self.__upload_txt_btn.place(x=16, y=260)

    # Action on clicking reset button
    def __onClickResetButton(self):
        self.__app.destroy()
        self.__init__()

    # Create reset button in encryption and decryption tab
    def __resetButton(self, parent_widget, padding_left, padding_top):
        self.__reset_btn = tk.Button(parent_widget, text="Reset", command=self.__onClickResetButton)
        self.__reset_btn.place(x=padding_left, y=padding_top)

    # Stick stego image on stego panel label for preview
    def __stickStegoImage(self):
        self.__stego_img = ImageTk.PhotoImage(self.__stego_object._stego_image.resize((298, 176)))
        self.__stego_panel = tk.Label(self.__encryption_tab, image=self.__stego_img, height=172, width=287)
        self.__stego_panel.place(x=303, y=3.5)

    # Action on clicking stego generate button
    def __onClickStegoGenerateButton(self):
        if self.__cover_filepath is None or self.__cover_filepath == "None":
            messagebox.showerror("IncognitoBit", "Must upload a cover image")
            return
        if len(self.__message.get(1.0, "end-1c")) == 0:
            messagebox.showerror("IncognitoBit", "Must enter some message or upload text file to be hidden")
            return
        self.__message.configure(state="disabled")
        self.__upload_img_btn["state"] = DISABLED
        self.__stego_generate_btn["state"] = DISABLED
        self.__upload_txt_btn["state"] = DISABLED
        self.__stego_object = Steganography(self.__cover_filepath, self.__message.get(1.0, "end-1c"))
        self.__status = self.__stego_object._generateStegoImage()
        if self.__status != "Stego Image generated successfully":
            messagebox.showerror("IncognitoBit", self.__status)
            self.__onClickResetButton()
        else:
            self.__stickStegoImage()
            messagebox.showinfo("IncognitoBit", self.__status)
            self.__save_stego_img_btn["state"] = NORMAL

    # Create stego image generate button in encryption tab
    def __stegoGenerateButton(self):
        self.__stego_generate_btn = tk.Button(self.__encryption_tab, text="Generate Stego Image", command=self.__onClickStegoGenerateButton)
        self.__stego_generate_btn.place(x=235, y=300)

    # Create exit button in encryption and decryption tab
    def __exitButton(self, parent_widget, padding_left, padding_top):
        self.__exit_btn = tk.Button(parent_widget, text="Exit", command=self.__app.destroy)
        self.__exit_btn.place(x=padding_left, y=padding_top)

    # Create decryption tab
    def __createDecryptionTab(self):
        self.__decryption_tab = tk.Frame(self.__tabs)
        self.__tabs.add(self.__decryption_tab, text="Decryption")
        self.__createDecryptionCanvas()
        self.__uploadStegoImageButton()
        self.__retrieveMessageButton()
        self.__createSaveTextButton()
        self.__createLoadingBar()
        self.__resetButton(self.__decryption_tab, 172.5, 272.5)
        self.__exitButton(self.__decryption_tab, 270, 272.5)

    # Generate frames in decryption tab
    def __createDecryptionCanvas(self):
        self.__stego_image_bg_frame = tk.Frame(self.__decryption_tab, background="black", height=262, width=598)
        self.__stego_image_bg_frame.pack()
        self.__stego_image_bg_frame.pack_propagate(0)
        self.__stego_image_bg_frame.place(x=1, y=1)
        self.__decrypted_text = scrolledtext.ScrolledText(self.__decryption_tab, width=30, height=16, wrap=CHAR)
        self.__decrypted_text.configure(state=DISABLED)
        self.__decrypted_text.place(x=334, y=2)
        self.__stego_image_fg_frame = tk.Frame(self.__decryption_tab, background="white", height=260, width=331)
        self.__stego_image_fg_frame.pack()
        self.__stego_image_fg_frame.pack_propagate(0)
        self.__stego_image_fg_frame.place(x=2, y=2)

    # Action on clicking retrieve message button
    def __onClickRetrieveMessageButton(self):
        if self.__stego_filepath is None or self.__stego_filepath == "None":
            messagebox.showerror("IncognitoBit", "Upload an image for decryption")
            return
        self.__retrieve_btn.configure(state=DISABLED)
        self.__upload_stego_img_btn.configure(state=DISABLED)
        self.__stego_object = Steganography(self.__stego_filepath)
        self.__original_msg = self.__stego_object._retrieveMessage(self.__decryption_tab, self.__loading_bar)
        self.__decrypted_text.configure(state=NORMAL)
        self.__decrypted_text.insert(INSERT, self.__original_msg)
        self.__decrypted_text.configure(state=DISABLED)
        if len(self.__decrypted_text.get(1.0, "end-1c")) == 0:
            messagebox.showinfo("IncognitoBit", "No hidden message found")
            self.__onClickResetButton()
        else:
            messagebox.showinfo("IncognitoBit", "Message retrieved successfully")
            self.__save_text_btn.configure(state=NORMAL)

    #  Retrieve message button in decryption tab
    def __retrieveMessageButton(self):
        self.__retrieve_btn = tk.Button(self.__decryption_tab, text="Retrieve Message", command=self.__onClickRetrieveMessageButton)
        self.__retrieve_btn.place(x=355, y=272.5)

    # Action on clciking stego image upload button
    def __onClickuploadStegoImageButton(self):
        self.__stego_filepath = str(filedialog.askopenfile(filetypes=[("PNG Images", "*.png")]))
        if self.__stego_filepath == "None":
            return 
        self.__stego_filepath = self.__stego_filepath[self.__stego_filepath.find("'") + 1:]
        self.__stego_filepath = self.__stego_filepath[:self.__stego_filepath.find("'")]
        self.__stego_img = Image.open(self.__stego_filepath)
        self.__stego_img = self.__stego_img.resize((327, 255))
        self.__stego_img = ImageTk.PhotoImage(self.__stego_img)
        self.__stego_panel = tk.Label(self.__decryption_tab, image=self.__stego_img, height=255, width=327)
        self.__stego_panel.place(x=2, y=3)

    # Create upload stego image button in decryption tab
    def __uploadStegoImageButton(self):
        self.__upload_stego_img_btn = tk.Button(self.__decryption_tab, text="Upload Image", command=self.__onClickuploadStegoImageButton)
        self.__upload_stego_img_btn.place(x=35, y=272.5)

    # Action on clicking save text button
    def __onClickSaveTextButton(self):
        self.__msg_filepath = str(filedialog.asksaveasfile(initialfile = 'message.txt', defaultextension=".txt",filetypes=[("Text Files","*.txt")]))
        if self.__msg_filepath == "None":
            return
        self.__msg_filepath = self.__msg_filepath[self.__msg_filepath.find("'") + 1:]
        self.__msg_filepath = self.__msg_filepath[:self.__msg_filepath.find("'")]
        with open(self.__msg_filepath, 'w+') as f:
            f.write(self.__decrypted_text.get(1.0, "end-1c"))
        f.close()
        messagebox.showinfo("IncognitoBit", "Message saved successfully")
        self.__onClickResetButton()

    # Create save text button in decryption tab
    def __createSaveTextButton(self):
        self.__save_text_btn = tk.Button(self.__decryption_tab, text="Save Message", command=self.__onClickSaveTextButton)
        self.__save_text_btn.place(x=490, y=272.5)
        self.__save_text_btn.configure(state=DISABLED)

    # Create loading bar in decryption tab
    def __createLoadingBar(self):
        self.__loading_bg_frame = tk.Frame(self.__decryption_tab, background="red", height=30, width=600)
        self.__loading_bg_frame.pack()
        self.__loading_bg_frame.pack_propagate(0)
        self.__loading_bg_frame.place(x=0, y=308)
        self.__loading_bar = ttk.Progressbar(self.__decryption_tab, orient="horizontal", length=592, value=0)
        self.__loading_bar.place(x=1.5, y=310)
        self.__loading_bar['value'] = 0

    # Create about tab
    def __createAboutTab(self):
        self.__about_tab = tk.Frame(self.__tabs)
        self.__tabs.add(self.__about_tab, text="About")
        # self.__about = scrolledtext.ScrolledText(self.__about_tab, width=72, height=16, wrap=tk.WORD)
        # self.__about.place(x=1, y=72)
        # self.__license_text = open('LICENSE.md', 'r')
        # count = 0
        # while True:
        #     count += 1
        #     line = self.__license_text.readline()
        #     if not line:
        #         break
        #     if count == 1:
        #         self.__about.insert(tk.INSERT, '                              ' + line.strip() + '\n')
        #     elif count == 2:
        #         self.__about.insert(tk.INSERT, '                        ' + line.strip() + '\n')
        #     elif count == 3:
        #         self.__about.insert(tk.INSERT, '                     ' + line.strip() + '\n')
        #     else:
        #         self.__about.insert(tk.INSERT, line.strip() + '\n')
        # self.__about.configure(state=DISABLED)
        # self.__college_img = Image.open("incognitobit/images/about-banner.png")
        # self.__college_img = ImageTk.PhotoImage(self.__college_img)
        # self.__college_logo = tk.Label(self.__about_tab, image=self.__college_img)
        # self.__college_logo.place(x=2.5, y=1)

# Application GUI Initializer
def main():
    Application()