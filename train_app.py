import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import subprocess
import psutil

def load_pdfs():
    file_paths = filedialog.askopenfilenames(
        filetypes=[("PDF files", "*.pdf")],
        title="Select PDF files"
    )
    for file_path in file_paths:
        if file_path:
            # Copy the selected PDFs to the data directory
            shutil.copy(file_path, 'data')
    messagebox.showinfo("Success", "PDFs have been loaded and are ready for training.")

def train_model():
    try:
        # Run the add_database.py script to train the model
        subprocess.run(["python", "add_database.py", "--reset"], check=True)
        messagebox.showinfo("Success", "Model has been trained with the new PDFs.")
        restart_streamlit_app()
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Training failed: {e}")

def restart_streamlit_app():
    try:
        # Check for any existing Streamlit processes and terminate them
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if 'streamlit' in proc.info['cmdline']:
                proc.kill()
        
        # Restart Streamlit app
        subprocess.Popen(["streamlit", "run", "app.py"])
        messagebox.showinfo("Success", "Streamlit app has been restarted.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to restart Streamlit app: {e}")

root = tk.Tk()
root.title("Model Training Application")

tk.Button(root, text="Load PDFs", command=load_pdfs).pack(pady=10)
tk.Button(root, text="Train Model", command=train_model).pack(pady=10)

root.mainloop()
