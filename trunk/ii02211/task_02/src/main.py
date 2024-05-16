import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json

class ContactsApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Адресная книжка")
        self.master.geometry("500x400")

        self.contacts = []

        self.create_widgets()

    def create_widgets(self):
        self.name_label = ttk.Label(self.master, text="Имя:")
        self.name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.name_entry = ttk.Entry(self.master)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.surname_label = ttk.Label(self.master, text="Фамилия:")
        self.surname_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.surname_entry = ttk.Entry(self.master)
        self.surname_entry.grid(row=1, column=1, padx=10, pady=5)

        self.address_label = ttk.Label(self.master, text="Адрес:")
        self.address_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.address_entry = ttk.Entry(self.master)
        self.address_entry.grid(row=2, column=1, padx=10, pady=5)

        self.add_button = ttk.Button(self.master, text="Добавить", command=self.add_contact)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.delete_button = ttk.Button(self.master, text="Удалить", command=self.delete_contact)
        self.delete_button.grid(row=3, column=1, columnspan=2, pady=10)

        self.contacts_listbox = tk.Listbox(self.master, width=50)
        self.contacts_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        self.load_button = ttk.Button(self.master, text="Загрузить", command=self.load_contacts)
        self.load_button.grid(row=5, column=0, pady=10)

        self.save_button = ttk.Button(self.master, text="Сохранить", command=self.save_contacts)
        self.save_button.grid(row=5, column=1, pady=10)

    def add_contact(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        address = self.address_entry.get()
        if name and surname and address:
            contact = {"Имя": name, "Фамилия": surname, "Адрес": address}
            self.contacts.append(contact)
            self.contacts_listbox.insert(tk.END, f"{name} {surname} - {address}")
            self.clear_fields()

    def delete_contact(self):
        selected_index = self.contacts_listbox.curselection()
        if selected_index:
            self.contacts.pop(selected_index[0])
            self.contacts_listbox.delete(selected_index[0])

    def save_contacts(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            try:
                with open(filename, "w") as file:
                    json.dump(self.contacts, file, indent=4)
                print("Адреса сохранены,успешно!")
            except Exception as e:
                print(f"Ошибка при сохранении: {e}")

    def load_contacts(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            try:
                with open(filename, "r") as file:
                    self.contacts = json.load(file)
                    self.contacts_listbox.delete(0, tk.END)
                    for contact in self.contacts:
                        self.contacts_listbox.insert(tk.END, f"{contact['name']} {contact['surname']} - {contact['address']}")
                print("Адреса загружены!")
            except FileNotFoundError:
                print("Файл контакта не найден.")
            except Exception as e:
                print(f"Ошибка при загрузке: {e}")

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.surname_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)


def main():
    root = tk.Tk()
    app = ContactsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
