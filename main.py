import tkinter as tk
from tkinter import messagebox

class Person:
    def __init__(self, name, age, phone_status):
        self.name = name
        self.age = age
        self.phone_status = phone_status

class SurveyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Survey Data Collector")
        self.root.geometry("400x350")

        # Data Storage
        self.person_list = []
        self.current_index = 0

        self.data_frame = tk.Frame(self.root)
        self.display_frame = tk.Frame(self.root)

        # Place both in the same grid spot so they overlap
        for frame in (self.data_frame, self.display_frame):
            frame.grid(row=0, column=0, sticky='nsew')

        self.setup_data_frame()
        self.setup_display_frame()
        self.show_data_collection()

    # Setup Data Collection Frame ---
    def setup_data_frame(self):
        tk.Label(self.data_frame, text="Data Collection Mode", font=("Arial", 14, "bold")).pack(pady=10)

        # Name Entry
        tk.Label(self.data_frame, text="Name:").pack()
        self.name_entry = tk.Entry(self.data_frame)
        self.name_entry.pack(pady=5)

        # Age Entry
        tk.Label(self.data_frame, text="Age:").pack()
        self.age_entry = tk.Entry(self.data_frame)
        self.age_entry.pack(pady=5)

        # Phone Status (Radio Buttons)
        tk.Label(self.data_frame, text="Do you have a mobile phone?").pack()
        self.phone_var = tk.StringVar(value="Yes")
        tk.Radiobutton(self.data_frame, text="Yes", variable=self.phone_var, value="Yes").pack()
        tk.Radiobutton(self.data_frame, text="No", variable=self.phone_var, value="No").pack()

        # Buttons
        tk.Button(self.data_frame, text="Enter Data", command=self.enter_data, bg="lightblue").pack(pady=10)
        tk.Button(self.data_frame, text="Show All", command=self.show_all_records).pack(pady=5)

    # Setup Display Frame ---
    def setup_display_frame(self):
        tk.Label(self.display_frame, text="View Records", font=("Arial", 14, "bold")).pack(pady=10)

        # Labels to display person info
        self.info_label = tk.Label(self.display_frame, text="", font=("Arial", 11), justify="left")
        self.info_label.pack(pady=20)

        # Navigation Buttons
        nav_container = tk.Frame(self.display_frame)
        nav_container.pack(pady=10)

        self.prev_btn = tk.Button(nav_container, text="Previous", command=self.show_prev)
        self.prev_btn.grid(row=0, column=0, padx=5)

        self.next_btn = tk.Button(nav_container, text="Next", command=self.show_next)
        self.next_btn.grid(row=0, column=1, padx=5)

        # Toggle back button
        tk.Button(self.display_frame, text="Add New Person", command=self.show_data_collection, bg="lightgreen").pack(pady=20)

    #Logic for Data Entry ---
    def enter_data(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        phone = self.phone_var.get()

        # Validation check
        if name == "" or age == "":
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        # Create object and store in list
        new_person = Person(name, age, phone)
        self.person_list.append(new_person)

        # Print check
        print(f"Collected: {name}, {age}, Phone: {phone}")

        # Clear widgets
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.phone_var.set("Yes")
        messagebox.showinfo("Success", f"Data for {name} added!")

    # Display Logic & Navigation for Records
    def show_all_records(self):
        if not self.person_list:
            messagebox.showinfo("Empty", "No data to show yet!")
            return
        
        self.current_index = 0
        self.update_display()
        self.display_frame.tkraise()

    def show_data_collection(self):
        self.data_frame.tkraise()


if __name__ == "__main__":
    root = tk.Tk()
    app = SurveyApp(root)
    root.mainloop()