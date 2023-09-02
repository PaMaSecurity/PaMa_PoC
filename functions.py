# imports:
from imports import tk, messagebox, convert_bin_txt
import add_account
import delete_account
import edit_account


class App(tk.Frame):
    def __init__(self, master, seed=None):
        super().__init__(master)
        # window:
        self.master = master
        self.root = master
        self.root.geometry('500x600')
        self.root.minsize(500, 600)  # 400x500
        self.root.resizable(height=True, width=True)
        self.root.config(bg='black')
        self.root.title("Command invite")
        self.create_widget()
        self.listbox.pack(side='top', fill='y')
        self.frame.pack(side='bottom')
        self.label.pack(side='left', fill='y')
        self.entry.pack(side='right')
        self.entry.focus_set()
        # events:
        self.root.bind('<Return>', self.add_listbox)
        self.root.bind('<Configure>', self.resize)
        # dictionaries:
        self.create_dico()
        self.read_txt()
        # variables:
        self.seed = seed
        # at the start:
        self.print_screen("Version 1.0")

    def create_dico(self):
        self.software_to_id = {}
        self.software_to_password = {}
        self.default_name_list = {"help": None, "namelist": None, "quit": None, "cls": None, "add": None,
                                  "delete": None, "edit": None, "credits": None}
        self.name_list = {"help": None, "namelist": None, "quit": None, "cls": None, "add": None,
                          "delete": None, "edit": None, "credits": None}
        self.dico_help = {
            "add": "Add an account",
            "cls": "Clear the screen",
            "credits": "",
            "delete": "delete an account",
            "edit": "Edit account information",
            "help": "Displays order information",
            "namelist": "Allows you to consult the database in which the accounts are stored",
            "quit": "Close the software"
        }

    def create_widget(self):
        self.frame = tk.Frame(self.root)
        self.label = tk.Label(self.frame,
                              text='>>>',
                              fg='white',
                              bg='black',
                              font=("arial", 9))
        self.entry = tk.Entry(self.frame,
                              width=int(self.root.winfo_width() / 6),
                              bg='#5E615E',
                              fg='black',
                              font=("arial", 9))
        self.listbox = tk.Listbox(self.root, width=int(self.root.winfo_width() / 6),
                                  height=int(self.root.winfo_width() / 13.8),
                                  bg='black',
                                  fg='#22E427',
                                  highlightthickness=0, font=("arial", 9))

    def resize(self, event=None):
        x = round(self.root.winfo_width() / 6)
        y = round(self.root.winfo_height() / 16.667)
        z = round(self.root.winfo_height() / 66.6667)
        self.entry.config(width=x)
        self.listbox.config(width=x,
                            height=round(y / (z / 9)),
                            font=("arial", z))
        self.entry.config(font=("arial", z))
        self.label.config(font=("arial", z))

    def add_listbox(self, event=None):
        self.print_screen('>>> ' + self.entry.get())
        cmd = self.entry.get()
        self.entry.delete(0, tk.END)
        cmd = cmd.lower()
        cmd = cmd.replace(" ", "")
        try:
            x = self.name_list[cmd]
            del x
            self.order_fulfilment(cmd)
        except:
            self.update_name_list()
            try:
                x = self.name_list[cmd]
                del x
                self.order_fulfilment(cmd)
            except:
                self.print_screen("Sorry, the account name is not registered in our database...")
                self.print_screen("Write 'help' to consult the list of commands.")

    def print_screen(self, text):
        self.listbox.insert('end', text)

    def order_fulfilment(self, software):
        if software == "main_password":
            self.print_screen("Sorry, the account name is not registered in our database...")
            self.print_screen("Write 'help' to consult the list of commands.")
        elif software == "help":
            for i in self.dico_help:
                self.print_screen([i, self.dico_help[i]])
        elif software == "quit":
            self.root.\
                destroy()
        elif software == "cls":
            self.listbox.delete(0, tk.END)
            self.listbox.insert('end', '>>> ' + "cls")
        elif software == "namelist":
            for i in self.name_list:
                if i == "main_password":
                    pass
                else:
                    self.print_screen(i)
            pass
        elif software == "add":
            root = tk.Tk()
            root = add_account.Add_account(root, name_list=self.name_list,
                                           software_to_password=self.software_to_password,
                                           software_to_id=self.software_to_id)
            root.mainloop()
        elif software == "delete":
            root = tk.Tk()
            root = delete_account.Delete_account(root, name_list=self.name_list,
                                                 software_to_password=self.software_to_password,
                                                 software_to_id=self.software_to_id,
                                                 default_name_list=self.default_name_list)
            root.mainloop()
        elif software == "edit":
            root = tk.Tk()
            root = edit_account.Edit_account(root, name_list=self.name_list,
                                             software_to_password=self.software_to_password,
                                             software_to_id=self.software_to_id,
                                             default_name_list=self.default_name_list)
            root.mainloop()
        elif software == "credits":
            self.print_screen(
                "Creator/Developer: Elie Ruggiero. Many thanks to ZukaBri3k (https://github.com/ZukaBri3k/CommandInvite/blob/main/main.py) for his precious help!")
        else:
            if self.software_to_id[software] == "":
                self.print_screen("There is no identification for this account.")
            else:
                self.print_screen("The ID is " + self.software_to_id[software])
            self.copy_in_clipboard(self.software_to_password[software])
            # self.print_screen(software_to_password[software])
            self.print_screen("The password has been saved in the clipboard.")

    def copy_in_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()

    def read_txt(self):
        with open("password.txt", "r+") as file:
            f = file.readlines()
            for i in range(len(f)):
                f[i] = convert_bin_txt(text=f[i])
            file.close()
        try:
            files = ""
            for i in range(len(f)):
                files = files + f[i]

            files = files.replace('\n', "")
            f = files.split(';;')
            for i in range(len(f)):
                element = f[i]
                if element == "":
                    pass
                else:
                    element = element.split('::')
                    website = element[0]
                    element = element[1].split("//")
                    id_ = element[0]
                    password = element[1]
                    self.name_list[website] = None
                    self.software_to_id[website] = id_
                    self.software_to_password[website] = password
        except:
            self.print_screen(
                "An error has occurred:( Please restart the software. If the error persists, please contact us.")
            messagebox.showerror("Error", "An error has occurred, quit the software")

    def update_name_list(self):
        self.name_list = {"help": None, "namelist": None, "quit": None, "cls": None, "add": None,
                          "delete": None, "edit": None, "credits": None}
        self.read_txt()