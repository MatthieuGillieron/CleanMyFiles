import os
import shutil
import tkinter as tk
from tkinter import filedialog
import webbrowser
import ttkbootstrap as ttk

def open_github():
    webbrowser.open("https://github.com/MatthieuGillieron")

def organize_files(directory, language):
    if not os.path.isdir(directory):
        print("Le répertoire n'existe pas !" if language == "fr" else "The directory does not exist!")
        return

    categories = {
        "Images" if language == "en" else "Images": [".jpg", ".jpeg", ".png", ".gif"],
        "Videos" if language == "en" else "Vidéos": [".mp4", ".avi", ".mkv", ".mov"],
        "Documents" if language == "en" else "Documents": [".pdf", ".docx", ".xlsx", ".txt"],
        "Music" if language == "en" else "Musique": [".mp3", ".wav", ".flac"],
        "Archives" if language == "en" else "Archives": [".zip", ".tar", ".gz", ".rar"],
        "Others" if language == "en" else "Autres": []
    }

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isdir(filepath):
            continue

        _, extension = os.path.splitext(filename)
        extension = extension.lower()

        destination_folder = "Others" if language == "en" else "Autres"
        for category, extensions in categories.items():
            if extension in extensions:
                destination_folder = category
                break

        dest_path = os.path.join(directory, destination_folder)
        os.makedirs(dest_path, exist_ok=True)

        shutil.move(filepath, os.path.join(dest_path, filename))
        print(f"Moved: {filename}" if language == "en" else f"Déplacé : {filename}")

def create_gui():
    app = ttk.Window(themename="darkly")
    app.title("File Organizer")
    app.geometry("600x400")

    # Créer une instance de Style
    style = ttk.Style()

    # Définir un style personnalisé pour le bouton "Browse"
    style.configure("custom.TButton",
                    padding=10,  # Augmenter l'espace à l'intérieur du bouton
                    relief="flat",
                    background="#1E90FF",  # Bleu pour le bouton
                    foreground="white",
                    borderwidth=2,
                    width=13,  # Largeur du bouton
                    height=2)  # Hauteur du bouton

    # Définir un style pour le bouton "RUN"
    style.configure("custom_run.TButton",
                    padding=10,  # Augmenter l'espace à l'intérieur du bouton
                    relief="flat",
                    background="#27AE60",  # Vert foncé pour le bouton "RUN"
                    foreground="white",
                    borderwidth=2,
                    width=5,  # Largeur du bouton
                    height=1)  # Hauteur du bouton

    # Modifier le style du bouton au survol
    style.map("custom.TButton",
              background=[('active', '#1E90FF'), ('hover', '#4682B4')])  # Autre bleu sur survol
    style.map("custom_run.TButton",
              background=[('active', '#228B22'), ('hover', '#3CB371')])  # Vert plus clair sur survol


    # Titre cliquable (avec style interactif)
    title = ttk.Label(
        app, text="GitHub → MatthieuGillieron",
        font=("Helvetica", 16, "bold"),
        cursor="hand2",
        foreground="#FFFFFF"
    )
    title.pack(pady=20)
    title.bind("<Button-1>", lambda e: open_github())
    title.bind("<Enter>", lambda e: title.config(foreground="#1E90FF", underline=True))
    title.bind("<Leave>", lambda e: title.config(foreground="#FFFFFF", underline=False))

    # Choix de langue
    language_var = tk.StringVar(value="en")
    ttk.Label(
        app, text="Choose Language / Choisissez la langue:", anchor="w", font=("Helvetica", 13, "italic")).pack(fill="x", padx=20, pady=10)
    ttk.Radiobutton(app, text="English", variable=language_var, value="en").pack(anchor="w", padx=40)
    ttk.Radiobutton(app, text="Français", variable=language_var, value="fr").pack(anchor="w", padx=40)

    # Texte explicatif pour le bouton "Browse"
    ttk.Label(
        app, text="Select the folder you want to organize / Sélectionnez le dossier à organiser:",
        anchor="w", font=("Helvetica", 13, "italic")
    ).pack(fill="x", padx=20, pady=(25, 5))

    # Bouton "Browse" avec style personnalisé
    directory_var = tk.StringVar()
    browse_button = ttk.Button(
        app, text="Browse / Parcourir",
        command=lambda: directory_var.set(filedialog.askdirectory()),
        style="custom.TButton"
    )
    browse_button.pack(anchor="w", padx=40, pady=15)

    # Bouton "RUN" avec style personnalisé
    ttk.Button(
        app, text="RUN",
        command=lambda: organize_files(directory_var.get(), language_var.get()),
        style="custom_run.TButton"
    ).pack(pady=20, side="bottom")

    app.mainloop()

if __name__ == "__main__":
    create_gui()
