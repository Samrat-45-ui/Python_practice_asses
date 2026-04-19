"""This program is a survey data collector that allows users to input their name, age, and phone status (whether they have a mobile phone or not). The data is stored in a list of Person objects, and users can navigate through the records using a simple GUI built with Tkinter. The application includes validation checks to ensure that the input data is reasonable and provides feedback to the user when necessary."""

import tkinter as tk
from tkinter import messagebox


class Person:
    """Class to represent a person with name, age, and phone status."""

    def __init__(self, name, age, phone_status):
        """Initialize the Person object with name, age, and phone status."""
        self.name = name
        self.age = age
        self.phone_status = phone_status


class SurveyApp:
    """Main application class for the survey data collector."""

    def __init__(self, root):
        """Initialize the application with the main window and setup frames."""
        self.root = root
        self.root.title("Survey Data Collector")
        self.root.geometry("420x380")
        self.root.configure(bg="#e8effa")
        self.root.resizable(False, False)

        # Shared style settings
        self.app_bg = "#f4f7ff"  # Light, neutral background for the app
        self.card_bg = "#ffffff"
        self.primary_btn_bg = "#4b8bbe"  # A slightly darker blue for primary actions
        self.secondary_btn_bg = "#7daedc"
        self.text_fg = "#2c3e50"
        self.title_font = ("Arial", 16, "bold")  # Clear, bold font for titles
        self.label_font = ("Arial", 11)
        self.button_font = ("Arial", 10, "bold")

        # Data Storage
        self.person_list = []  # List to store Person objects
        self.current_index = 0  # To keep track of which record is currently being displayed

        self.data_frame = tk.Frame(self.root, bg=self.app_bg)
        self.display_frame = tk.Frame(self.root, bg=self.app_bg)

        # Place both in the same grid spot so they overlap
        for frame in (self.data_frame, self.display_frame):  # Loop to place both frames in the same grid location
            frame.grid(row=0, column=0, sticky='nsew')

        self.setup_data_frame()
        self.setup_display_frame()
        self.show_data_collection()

    # Setup Data Collection Frame ---
    def setup_data_frame(self):
        """Configure the data collection frame with input fields and buttons."""
        self.data_frame.configure(bg=self.app_bg, padx=20, pady=15)
        tk.Label(self.data_frame, text="Data Collection Mode", font=self.title_font, bg=self.app_bg, fg=self.text_fg).pack(pady=12)

        # Name Entry
        tk.Label(self.data_frame, text="Name:", font=self.label_font, bg=self.app_bg, fg=self.text_fg).pack(anchor="w", padx=10)  # Align label to the left with padding
        self.name_entry = tk.Entry(self.data_frame, bd=2, relief="groove", font=self.label_font)  # Standard entry widget with a groove border for better visibility
        self.name_entry.pack(fill="x", pady=5, padx=10)

        # Age Entry
        tk.Label(self.data_frame, text="Age:", font=self.label_font, bg=self.app_bg, fg=self.text_fg).pack(anchor="w", padx=10)  # Align label to the left with padding
        self.age_entry = tk.Entry(self.data_frame, bd=2, relief="groove", font=self.label_font)  # Standard entry widget with a groove border for better visibility
        self.age_entry.pack(fill="x", pady=5, padx=10)

        # Phone Status (Radio Buttons)
        tk.Label(self.data_frame, text="Do you have a mobile phone?", font=self.label_font, bg=self.app_bg, fg=self.text_fg).pack(anchor="w", padx=10, pady=(10, 4))  # Align label to the left with padding and add extra space below
        self.phone_var = tk.StringVar(value="Yes")  # Default to "Yes" for better user experience, as most people have mobile phones nowadays
        phone_frame = tk.Frame(self.data_frame, bg=self.app_bg)
        phone_frame.pack(fill="x", padx=10)
        tk.Radiobutton(  # Default to "Yes" for better user experience, as most people have mobile phones nowadays
            phone_frame,
            text="Yes",
            variable=self.phone_var,
            value="Yes",
            bg=self.app_bg,
            activebackground=self.app_bg,
            font=self.label_font,
            anchor="w",
            pady=2,
        ).pack(side="left", padx=(0, 15))
        tk.Radiobutton(  # Provide a "No" option for users who do not have a mobile phone, but default to "Yes" for better user experience, as most people have mobile phones nowadays
            phone_frame,
            text="No",
            variable=self.phone_var,  # Link both radio buttons to the same variable to ensure only one can be selected at a time
            value="No",
            bg=self.app_bg,
            activebackground=self.app_bg,  # Match the background color for a cleaner look when selected
            font=self.label_font,
            anchor="w",
            pady=2,
        ).pack(side="left")

        # Buttons
        tk.Button(
            self.data_frame,
            text="Enter Data",
            command=self.enter_data,  # Call the method to collect data and store it in the list when this button is clicked
            bg=self.primary_btn_bg,  # Use the primary button color for the main action of entering data to make it stand out and guide the user towards the key functionality of the app.
            fg="white",
            activebackground="#6aa8e6",
            activeforeground="white",
            font=self.button_font,  # Use the same button font for consistency across the app, but differentiate primary and secondary actions through color.
            bd=0,
            relief="raised",  # Use a raised relief for buttons to give them a more clickable appearance, which is especially important for the "Enter Data" button as it is the primary action in the app.
            padx=10,
            pady=6,
        ).pack(pady=12, padx=10, fill="x")

        tk.Button(  # Button to show all records, which will raise the display frame and show the first record if there are any records in the list. If the list is empty, it will show a message box informing the user that there are no records to show yet.
            self.data_frame,
            text="Show All",
            command=self.show_all_records,
            bg=self.secondary_btn_bg,
            fg="white",
            activebackground="#8bb8e1",  # A lighter blue for the secondary action to differentiate it from the primary "Enter Data" button, while still maintaining a cohesive color scheme.
            activeforeground="white",
            font=self.button_font,  # Use the same button font for consistency across the app, but differentiate primary and secondary actions through color.
            bd=0,
            relief="raised",  # Use a raised relief for buttons to give them a more clickable appearance, which is especially important for the "Show All" button as it is a key navigation element in the app.
            padx=10,
            pady=6,
        ).pack(pady=5, padx=10, fill="x")

    # Setup Display Frame ---
    def setup_display_frame(self):
        """Configure the display frame to show records and navigation buttons."""
        self.display_frame.configure(bg=self.app_bg, padx=20, pady=15)
        tk.Label(self.display_frame, text="View Records", font=self.title_font, bg=self.app_bg, fg=self.text_fg).pack(pady=12)

        # Labels to display person info
        self.info_label = tk.Label(
            self.display_frame,
            text="",
            font=self.label_font,
            justify="left",  # Align text to the left for better readability, especially when displaying multiple lines of information like name, age, and phone status.
            bg=self.card_bg,
            fg=self.text_fg,
            bd=2,
            relief="groove",  # Use a groove relief for the info label to give it a card-like appearance, which helps to visually separate it from the background and make it stand out as the main area where the person's information is displayed.
            padx=12,
            pady=12,
            width=35,
            anchor="w",  # Align text to the left within the label for better readability, especially when displaying multiple lines of information like name, age, and phone status.
        )
        self.info_label.pack(pady=20)

        # Navigation Buttons
        nav_container = tk.Frame(self.display_frame, bg=self.app_bg)
        nav_container.pack(pady=10)

        self.prev_btn = tk.Button(
            nav_container,
            text="Previous",
            command=self.show_prev,  # Call the method to show the previous record in the list when this button is clicked, with boundary checks to ensure we don't go before the start of the list.
            bg=self.secondary_btn_bg,
            fg="white",
            activebackground="#8bb8e1",  # A lighter blue for the secondary action to differentiate it from the primary "Enter Data" button, while still maintaining a cohesive color scheme.
            activeforeground="white",
            font=self.button_font,  # Use the same button font for consistency across the app, but differentiate primary and secondary actions through color.
            bd=0,  # Remove the default border to create a cleaner look, especially since we're using color and relief to differentiate buttons, which helps to maintain a modern and cohesive design aesthetic.
            relief="raised",  # Use a raised relief for buttons to give them a more clickable appearance, which is especially important for navigation buttons as they are key elements for moving through the records in the app.
            padx=12,
            pady=6,
        )
        self.prev_btn.grid(row=0, column=0, padx=5)

        self.next_btn = tk.Button(
            nav_container,
            text="Next",
            command=self.show_next,  # Call the method to show the next record in the list when this button is clicked, with boundary checks to ensure we don't go past the end of the list.
            bg=self.primary_btn_bg,
            fg="white",  # Use white text for better contrast against the primary button color, which helps to ensure that the button label is easily readable and stands out as a key navigation element in the app.
            activebackground="#6aa8e6",
            activeforeground="white",
            font=self.button_font,
            bd=0,  # Remove the default border to create a cleaner look, especially since we're using color and relief to differentiate buttons, which helps to maintain a modern and cohesive design aesthetic.
            relief="raised",  # Use a raised relief for buttons to give them a more clickable appearance, which is especially important for navigation buttons as they are key elements for moving through the records in the app.
            padx=12,
            pady=6,
        )
        self.next_btn.grid(row=0, column=1, padx=5)

        # Toggle back button
        tk.Button(
            self.display_frame,
            text="Add New Person",
            command=self.show_data_collection,  # Call the method to raise the data collection frame when this button is clicked, allowing the user to enter new records after viewing existing ones.
            bg="#6fcf97",  # A green color for the "Add New Person" button to differentiate it from the primary and secondary actions related to viewing records, while still maintaining a cohesive color scheme that complements the blues used for the other buttons.
            fg="white",
            activebackground="#7dd8a8",  # A slightly lighter green for the active state of the "Add New Person" button to provide visual feedback when the user interacts with it, while still maintaining a cohesive color scheme that complements the blues used for the other buttons.
            activeforeground="white",
            font=self.button_font,  # Use the same button font for consistency across the app, but differentiate primary and secondary actions through color, with the "Add New Person" button using a distinct green color to indicate its function as a key action for adding new records.
            bd=0,
            relief="raised",  # Use a raised relief for buttons to give them a more clickable appearance, which is especially important for the "Add New Person" button as it is a key action in the app for adding new records after viewing existing ones.
            padx=12,
            pady=8,
        ).pack(pady=20)

    # Logic for Data Entry
    def enter_data(self):
        """Collect data from input fields, validate it, and store it in the list."""
        name = self.name_entry.get()
        age = self.age_entry.get()
        phone = self.phone_var.get()
        self.AVERAGE_HUMAN_MAX_AGE = 100  # More realistic upper limit for age

        # Validation check
        if name == "" or age == "":  # Basic check for empty fields
            messagebox.showwarning("Input Error", "Please fill in all fields with valid data.")  # Show a warning message box if any of the required fields are empty, prompting the user to fill in all fields with valid data before they can successfully enter their information into the survey. This helps to ensure that the collected data is complete and usable for analysis, while also providing clear feedback to the user about what is required for successful data entry.
            return

        if len(name) > 50:  # Check for excessively long names
            messagebox.showwarning("Input Error", "Name is too long. Please enter a name with 50 characters or less.")
            return

        if name.isdigit():
            messagebox.showwarning("Input Error", "Name cannot be a number. Please enter a valid name.")
            return

        if not age.isdigit():  # Check if age is a valid number
            messagebox.showwarning("Input Error", "Age must be a valid number.")
            return

        age_int = int(age)
        if age_int <= 0 or age_int > self.AVERAGE_HUMAN_MAX_AGE:  # Adjusted upper limit to 100 for more realistic data collection
            messagebox.showwarning("Input Error", f"Age must be a positive integer and less than or equal to {self.AVERAGE_HUMAN_MAX_AGE}.")
            return

        # Create object and store in list
        new_person = Person(name, int(age), phone)  # Create a new Person object with the collected data, converting the age to an integer for proper storage and later use in the display and navigation of records.
        self.person_list.append(new_person)  # Append the new Person object to the person_list, which serves as the main data storage for all collected records in the app. This allows us to keep track of all entered data and enables the functionality to view and navigate through the records in the display frame.

        # Print check
        print(f"Collected: {name}, {age}, Phone: {phone}")  # Print the collected data to the console for debugging purposes, allowing us to verify that the data is being collected correctly before it is stored in the list and displayed in the app. This can help identify any issues with data collection or validation during development and testing.

        # Clear widgets
        self.name_entry.delete(0, tk.END)  # Clear the name entry field after successful data entry to provide a clean slate for the next input
        self.age_entry.delete(0, tk.END)  # Clear the age entry field after successful data entry to provide a clean slate for the next input
        self.phone_var.set("Yes")  # Reset the phone status radio buttons to the default "Yes" after successful data entry to provide a consistent starting point for the next input.
        messagebox.showinfo("Success", f"Data for {name} added!")  # Show a success message box after successfully adding a new record to the list, providing feedback to the user that their data has been collected and stored successfully.

    # Display Logic & Navigation
    def show_all_records(self):  # Method to show all records, which will raise the display frame and show the first record if there are any records in the list.
        if not self.person_list:  # Check if the list is empty before trying to display records, and show an informational message box if there are no records to show yet, prompting the user to enter data before they can view records in the display frame.
            messagebox.showinfo("Empty", "No data to show yet!")
            return

        self.current_index = 0
        self.update_display()
        self.display_frame.tkraise()

    def show_data_collection(self):  # Method to show the data collection frame, which will raise the data collection frame to allow the user to enter new records after viewing existing ones in the display frame.
        """Raise the data collection frame to allow user to enter new records."""
        self.data_frame.tkraise()

    def update_display(self):  # Method to update the display Labels with the current person's information and update the window title to reflect the current record being viewed.
        """Update the display labels with the current person's information and update the window title."""
        # Configure labels to show info from current object
        person = self.person_list[self.current_index]
        display_text = f"Name: {person.name}\nAge: {person.age}\nMobile: {person.phone_status}"
        self.info_label.config(text=display_text)

        # Counter for user context
        self.root.title(f"Record {self.current_index + 1} of {len(self.person_list)}")

    def show_next(self):  # Method to show the next record in the list, with a boundary check.
        """Boundary check to ensure we don't go past the end of the list, then update display to show next record."""
        # Boundary check
        if self.current_index < len(self.person_list) - 1:
            self.current_index += 1
            self.update_display()
        else:
            messagebox.showinfo("End", "You have reached the end of the list.")

    def show_prev(self):  # Method to show the previous record in the list, with a boundary check.
        """Boundary check to ensure we don't go before the start of the list, then update display to show previous record."""
        # Boundary check
        if self.current_index > 0:
            self.current_index -= 1
            self.update_display()
        else:
            messagebox.showinfo("Start", "This is the first record.")


# --- Main Program Execution ---
if __name__ == "__main__":
    """Entry point for the application."""

    root = tk.Tk()  # Create the main application window using Tkinter, which will serve as the container for all the frames and widgets in the survey data collector app.
    app = SurveyApp(root)
    root.mainloop()  # Start the Tkinter event loop, which will keep the application running and responsive to user interactions until the user closes the window.
