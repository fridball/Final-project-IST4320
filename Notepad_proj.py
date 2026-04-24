import os
import tkinter as tk
from tkinter import ttk, messagebox
import json
from ttkbootstrap import Style

#creating the main window now...
root = tk.Tk()
root.title("Kawaii Notepad (≧ヮ≦) 💕")
root.geometry("600x400")
root.configure(bg="#e7a1b6")
style = Style(theme='journal')



#making the tabs font be in bold for better visibility
style.configure(
    "TNotebook.Tab", 
    font=("georgia", 16, "bold"),
    padding=[10, 5]
)
style.map(
    "TNotebook.Tab",
    foreground=[("selected", "#e7a1b6"), ("!selected", "#ff99cc")],
)
# mstoring notes
notes = {}
note_widgets = {}

def save_note():
    with open("notes.json", "w") as file:
        json.dump(notes, file)

# making sure users can load notes
def load_note():
   global notes
   if os.path.exists("notes.json"):
       try:
           with open("notes.json", "r") as file:
               notes = json.load(file)
       except json.JSONDecodeError:
           notes = {}
           messagebox.showerror("Error", "Failed to load notes. The file may be corrupted.")
   else:
        notes = {}


#notepad widget
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=10, pady=10)


# create function to + add new note
def add_tab(title="", content=""):
    note_frame = ttk.Frame(notebook, padding=10)
    notebook.add(note_frame, text=title if title else f"New Note {len(notebook.tabs()) + 1}")
    notebook.select(note_frame)

#create widgets for title 
    title_label = ttk.Label(note_frame, text="˖ . ݁𝜗𝜚. ݁₊Title˖ . ݁𝜗𝜚. ݁₊: ")
    title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    
    title_entry = ttk.Entry(note_frame, width=50)
    title_entry.configure(foreground="#d63384")
    title_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    title_entry.insert(0, title)

# content = "my notes"
    content_label = ttk.Label(note_frame, text="˖ . ݁𝜗𝜚. ݁₊My Notes˖ . ݁𝜗𝜚. ݁₊: ")
    content_label.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

    content_entry = tk.Text(
        note_frame, 
        width=50, 
        height=15,
        wrap="word",
        bg="#fff0f5",
        fg="#d63384",
        insertbackground="#ff69b4",
        font=("Comic Sans MS", 14)
        )
    content_entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
    content_entry.insert("1.0", content)
    note_frame.columnconfigure(1, weight=1)
    note_frame.rowconfigure(1, weight=1)

    #create A save function
    def save_current_note():
        #tite + content of note
        past_title = notebook.tab(note_frame, "text")
        current_title = title_entry.get().strip()
        current_content = content_entry.get("1.0", tk.END).strip()
        if not current_title: 
            messagebox.showinfo("Warning", "Title cannot be empty. Please enter a title for your note.")
            return
        if not current_content:
            messagebox.showinfo("Warning", "Content cannot be empty. Please enter some content for your note.")
            return
        
        #remove old title from notes dictionary if title has been changed
        if past_title in notes and past_title != current_title:
            del notes[past_title]

        #update notes dictionary with new title and content
        notes[current_title] = current_content
        save_note()

        notebook.tab(note_frame, text=current_title)
        note_widgets[note_frame] = (title_entry, content_entry)
        messagebox.showinfo("Success", f"Note '{current_title}' has been saved successfully!")
       
        #save button
    save_button = ttk.Button(
            note_frame, 
            text="｡⋆♡Save Note𐙚⋆°",
            command=save_current_note,
            style="secondary.TButton"
            )
    save_button.grid(row=2, column=1, padx=10, pady=10, sticky="e")
    note_widgets[note_frame] = (title_entry, content_entry)

        #add note to the notebook
def add_note():
    add_tab()
        
        # delete note from the notebook
def delete_note():
        current_tab = notebook.select()
        if not current_tab:
            messagebox.showwarning("Warning", "No note selected. Please select a note to delete.")
            return
        note_title = notebook.tab(current_tab, "text")
        confirm = messagebox.askyesno(
            "Delete Note", 
            f"Are you sure you want to delete the note '{note_title}'?"
            )
        if confirm:
            if note_title in notes:
                del notes[note_title]
                save_note()
        notebook.forget(current_tab)

        if current_tab in note_widgets:
            del note_widgets[current_tab]
        messagebox.showinfo("Success", f"Note '{note_title}' has been deleted successfully!")
    #load saved notes!
load_note()
if notes:
    for title, content in notes.items():
        add_tab(title, content)
else:
    add_tab()


# add buttons to the main window
button_frame = tk.Frame(root, bg="#ffe4ec")
button_frame.pack(pady=10)

new_button = tk.Button(
    button_frame,
    text="｡⋆♡New Note𐙚⋆°",
    font=("georgia", 12, "bold"),
    bg="#ffc1cc",
    fg="#ffffff",
    activebackground="#d6094e",
    activeforeground="#ffffff",
    relief="flat",
    bd=0,
    padx=10,
    pady=5,
    command=add_note,
)
new_button.pack(side=tk.LEFT, padx=10, pady=10)

delete_button = tk.Button(
    button_frame,
    text="𐙚Delete Note𐙚",
    font=("georgia", 12, "bold"),
    bg="#ff99cc",
    fg="#ffffff",
    activebackground="#d6094e",
    activeforeground="#ffffff",
    relief="flat",
    bd=0,
    padx=10,
    pady=5,
    command=delete_note,
)
delete_button.pack(side=tk.LEFT, padx=10, pady=10)


root.mainloop()