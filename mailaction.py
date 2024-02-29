import os
import tkinter as tk
from tkinter import filedialog, messagebox, Text
import webbrowser

def wrapper(root):
    """
    Wrapper function to initialize and configure the main application window.
    
    Parameters:
        root (tk.Tk): The Tkinter root window.
    """
    def get_files(folder_path):
        """
        Function to retrieve specific files from a folder and update the UI fields accordingly.
        
        Parameters:
            folder_path (str): The path to the folder containing the required files.
        """
        files = []
        subject_file_found = False
        pdf_files = []  # List to store paths of PDF files
        for root, _, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                if filename.endswith(".pdf"):
                    pdf_files.append(file_path)
                if filename == "subject.txt":
                    with open(file_path, "r") as f:
                        entry_subject.delete(0, tk.END)
                        entry_subject.insert(tk.END, f.read().strip())
                        subject_file_found = True
                elif filename.startswith("body"):
                    with open(file_path, "r") as f:
                        text_body.delete("1.0", tk.END)
                        text_body.insert(tk.END, f.read())
                elif filename.startswith("bcc"):
                    with open(file_path, "r") as f:
                        entry_bcc.delete(0, tk.END)
                        entry_bcc.insert(tk.END, f.read())
                elif filename.startswith("cc"):
                    with open(file_path, "r") as f:
                        entry_cc.delete(0, tk.END)
                        entry_cc.insert(tk.END, f.read())
                elif filename.startswith("name"):
                    with open(file_path, "r") as f:
                        entry_name.delete(0, tk.END)
                        entry_name.insert(tk.END, f.read())
                elif filename.startswith("to"):
                    with open(file_path, "r") as f:
                        entry_to.delete(0, tk.END)
                        entry_to.insert(tk.END, f.read())
                # Collect all files, mainly for checking the count later
                files.append(file_path)
        
        # Update the attachment field with PDF files, separated by a semicolon if more than one
        entry_attachment.delete(0, tk.END)
        entry_attachment.insert(tk.END, "; ".join(pdf_files))

        if len(files) != 7:
            messagebox.showerror("Error", "Folder contains more than or less than 7 suitable files.")
            return
        if not subject_file_found:
            messagebox.showerror("Error", "No subject.txt file found in the folder.")
            return
        if not files:
            messagebox.showerror("Error", "No suitable files found in the folder.")
            return

    def ask_folder():
        """
        Function to prompt the user to select a folder using file dialog.
        """
        folder_path = filedialog.askdirectory()
        if folder_path:
            text_body.delete("1.0", tk.END)  # Clear the body text when selecting a new folder
            text_body.insert(tk.END, "Files loaded from folder: " + folder_path)
            get_files(folder_path)

    def compose_email():
        """
        Function to compose and send an email based on user input.
        """
        subject = entry_subject.get()
        body = "Hello " + entry_name.get() + "\n" + text_body.get("1.0", tk.END).strip()   
        to = entry_to.get()
        cc = entry_cc.get()
        bcc = entry_bcc.get()
        attachments = entry_attachment.get()
        if not to:
            messagebox.showerror("Error", "Recipient email address is required.")
            return
        mailto_url = f'mailto:{to}'
        params = []
        if cc:
            params.append(f'cc={cc}')
        if bcc:
            params.append(f'bcc={bcc}')
        if subject:
            params.append(f'subject={subject}')
        if body:
            params.append(f'body={body}')
        # Note: Attachments cannot be automated through mailto due to security restrictions
        mailto_url += '?' + '&'.join(params)
        webbrowser.open_new(mailto_url)
        # Reminder to manually attach PDFs if needed
        if attachments:
            #messagebox.showinfo("Reminder", "Remember to attach your files manually: " + attachments)
            print()

    # Create the main window
    root.title("Compose Email")

    # Option to import
    label_radio = tk.Label(root, text="Import from folder")
    select_folder_button = tk.Button(root, text="Select Folder", command=ask_folder)
    label_radio.grid(row=0, columnspan=2, pady=20)
    select_folder_button.grid(row=1, columnspan=2, pady=10)

    # Target Name
    label_name = tk.Label(root, text="Target's Name:")
    label_name.grid(row=3, column=0, sticky="w")
    entry_name = tk.Entry(root)
    entry_name.grid(row=3, column=1, padx=5, pady=5, sticky="we")

    # Subject
    label_subject = tk.Label(root, text="Subject:")
    label_subject.grid(row=2, column=0, sticky="w")
    entry_subject = tk.Entry(root)
    entry_subject.grid(row=2, column=1, padx=5, pady=5, sticky="we")

    # Body
    label_body = tk.Label(root, text="Body:")
    label_body.grid(row=4, column=0, sticky="nw")
    text_body = tk.Text(root, height=5, width=30)
    text_body.grid(row=4, column=1, padx=5, pady=5, sticky="we")

    # To
    label_to = tk.Label(root, text="To:")
    label_to.grid(row=5, column=0, sticky="w")
    entry_to = tk.Entry(root)
    entry_to.grid(row=5, column=1, padx=5, pady=5, sticky="we")

    # Cc
    label_cc = tk.Label(root, text="Cc:")
    label_cc.grid(row=6, column=0, sticky="w")
    entry_cc = tk.Entry(root)
    entry_cc.grid(row=6, column=1, padx=5, pady=5, sticky="we")

    # Bcc
    label_bcc = tk.Label(root, text="Bcc:")
    label_bcc.grid(row=7, column=0, sticky="w")
    entry_bcc = tk.Entry(root)
    entry_bcc.grid(row=7, column=1, padx=5, pady=5, sticky="we")

    # Attachment
    label_attachment = tk.Label(root, text="Attachment:")
    label_attachment.grid(row=8, column=0, sticky="w")
    entry_attachment = tk.Entry(root)
    entry_attachment.grid(row=8, column=1, padx=5, pady=5, sticky="we")

    # Compose button
    button_compose = tk.Button(root, text="Compose", command=compose_email)
    button_compose.grid(row=9, columnspan=2, pady=10)

    # Check folder automatically on app start
    current_directory = os.getcwd()
    folder_name = "inputFolder"
    folder_path = os.path.join(current_directory, folder_name)

    if os.path.exists(os.path.join(current_directory, folder_name)) and os.path.isdir(os.path.join(current_directory, folder_name)):
        get_files(folder_path)

    # Run the application
    root.mainloop()

# Run the application
def main(root):
    """
    Main function to run the application.
    
    Parameters:
        root (tk.Tk): The Tkinter root window.
    """
    wrapper(root)
