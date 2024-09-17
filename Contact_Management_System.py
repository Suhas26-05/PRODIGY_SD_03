import tkinter as tk
from tkinter import messagebox, simpledialog
import os

# File to store contacts persistently
CONTACTS_FILE = 'contacts.txt'

# Function to load contacts from the file
def load_contacts():
    contacts = {}
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'r') as file:
            for line in file:
                name, phone, email = line.strip().split(',')
                contacts[name] = {'phone': phone, 'email': email}
    return contacts

# Function to save contacts to the file
def save_contacts():
    with open(CONTACTS_FILE, 'w') as file:
        for name, info in contacts.items():
            file.write(f"{name},{info['phone']},{info['email']}\n")

# Function to add a new contact
def add_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()

    # Validate input fields
    if name == '' or phone == '' or email == '':
        messagebox.showerror("Input Error", "All fields must be filled.")
        return

    # Check if phone number contains exactly 10 digits and is numeric
    if not phone.isdigit() or len(phone) != 10:
        messagebox.showerror("Invalid Phone Number", "Phone number must be exactly 10 digits.")
        return

    if name in contacts:
        messagebox.showerror("Duplicate Contact", "Contact already exists.")
    else:
        contacts[name] = {'phone': phone, 'email': email}
        save_contacts()
        update_contact_list()
        messagebox.showinfo("Success", f"Contact '{name}' added successfully.")
        clear_entries()

# Function to update the contact list display
def update_contact_list():
    contact_listbox.delete(0, tk.END)
    for name in contacts:
        contact_listbox.insert(tk.END, name)

# Function to view selected contact details
def view_contact():
    try:
        selected_name = contact_listbox.get(contact_listbox.curselection())
        contact = contacts[selected_name]
        messagebox.showinfo("Contact Info", f"Name: {selected_name}\nPhone: {contact['phone']}\nEmail: {contact['email']}")
    except tk.TclError:
        messagebox.showerror("Selection Error", "Please select a contact to view.")

# Function to edit a selected contact
def edit_contact():
    try:
        selected_name = contact_listbox.get(contact_listbox.curselection())
        contact = contacts[selected_name]

        # Load the contact details into the entry fields for editing
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)

        name_entry.insert(0, selected_name)
        phone_entry.insert(0, contact['phone'])
        email_entry.insert(0, contact['email'])

        # Update the "Add Contact" button to "Save Changes"
        add_button.config(text="Save Changes", command=lambda: save_changes(selected_name))
    except tk.TclError:
        messagebox.showerror("Selection Error", "Please select a contact to edit.")

# Function to save changes to an existing contact
def save_changes(old_name):
    new_name = name_entry.get().strip()
    new_phone = phone_entry.get().strip()
    new_email = email_entry.get().strip()

    # Validate the input fields
    if new_name == '' or new_phone == '' or new_email == '':
        messagebox.showerror("Input Error", "All fields must be filled.")
        return

    if not new_phone.isdigit() or len(new_phone) != 10:
        messagebox.showerror("Invalid Phone Number", "Phone number must be exactly 10 digits.")
        return

    # Remove the old contact and add the updated one
    del contacts[old_name]
    contacts[new_name] = {'phone': new_phone, 'email': new_email}
    save_contacts()
    update_contact_list()
    messagebox.showinfo("Success", "Contact updated successfully.")

    # Reset the "Add Contact" button
    add_button.config(text="Add Contact", command=add_contact)
    clear_entries()

# Function to delete a selected contact
def delete_contact():
    try:
        selected_name = contact_listbox.get(contact_listbox.curselection())
        response = messagebox.askyesno("Delete Contact", f"Are you sure you want to delete '{selected_name}'?")
        if response:
            del contacts[selected_name]
            save_contacts()
            update_contact_list()
            messagebox.showinfo("Success", "Contact deleted successfully.")
    except tk.TclError:
        messagebox.showerror("Selection Error", "Please select a contact to delete.")

# Function to clear the input fields
def clear_entries():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

# Initial setup
contacts = load_contacts()

# Create the main window
window = tk.Tk()
window.title("Contact Management System")
window.geometry("500x550")
window.config(bg='#f0f4f5')

# Title label
title_label = tk.Label(window, text="Contact Management System", font=("Helvetica", 18), bg='#f0f4f5')
title_label.pack(pady=10)

# Name entry
name_label = tk.Label(window, text="Name:", font=("Helvetica", 12), bg='#f0f4f5')
name_label.pack()
name_entry = tk.Entry(window, font=("Helvetica", 12), width=30)
name_entry.pack(pady=5)

# Phone entry
phone_label = tk.Label(window, text="Phone:", font=("Helvetica", 12), bg='#f0f4f5')
phone_label.pack()
phone_entry = tk.Entry(window, font=("Helvetica", 12), width=30)
phone_entry.pack(pady=5)

# Email entry
email_label = tk.Label(window, text="Email:", font=("Helvetica", 12), bg='#f0f4f5')
email_label.pack()
email_entry = tk.Entry(window, font=("Helvetica", 12), width=30)
email_entry.pack(pady=5)

# Add/Save button
add_button = tk.Button(window, text="Add Contact", font=("Helvetica", 12), command=add_contact, bg='#00CED1', fg='white')
add_button.pack(pady=10)

# Contact listbox
contact_listbox = tk.Listbox(window, font=("Helvetica", 12), width=40, height=10)
contact_listbox.pack(pady=10)

# View, Edit, and Delete buttons
button_frame = tk.Frame(window, bg='#f0f4f5')
button_frame.pack(pady=10)

view_button = tk.Button(button_frame, text="View", font=("Helvetica", 12), command=view_contact, bg='#4CC552', fg='white', width=10)
view_button.grid(row=0, column=0, padx=5)

edit_button = tk.Button(button_frame, text="Edit", font=("Helvetica", 12), command=edit_contact, bg='#ff9800', fg='white', width=10)
edit_button.grid(row=0, column=1, padx=5)

delete_button = tk.Button(button_frame, text="Delete", font=("Helvetica", 12), command=delete_contact, bg='#f44336', fg='white', width=10)
delete_button.grid(row=0, column=2, padx=5)

# Load the contact list when starting the application
update_contact_list()

# Start the Tkinter event loop
window.mainloop()
