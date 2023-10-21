import os
import shutil
from tkinter import Tk, Canvas, PhotoImage, Button, Scrollbar, VERTICAL

# Function to get possible units for a question based on the paper
def get_possible_units(filename):
    paper_info = filename.split("_")
    paper_number = int(paper_info[3][0])
    print(paper_info)
    print(paper_number)
    
    units = []
    if paper_number == 1:
        units = list(range(1, 9))
    elif paper_number == 2:
        units = list(range(9, 13))
    elif paper_number == 3:
        units = list(range(13, 21))
    elif paper_number == 4:
        units = list(range(19, 21))
        
    return units

# Function to move file to the sorted directory and show next image
def move_and_show_next(filename, unit, image_files):
    dest_folder = f"./sorted/{unit}/"
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    shutil.move(filename, os.path.join(dest_folder, os.path.basename(filename)))
    print(f"Moved {filename} to {dest_folder}")
    show_next_image(image_files)

# Function to display the next image
def show_next_image(image_files):
    if image_files:
        next_image_path = image_files.pop(0)
        next_img = PhotoImage(file=next_image_path)
        canvas.create_image(0, 0, anchor="nw", image=next_img)
        canvas.image = next_img  # Keep a reference to avoid garbage collection
        canvas.config(scrollregion=canvas.bbox("all"))  # Enable scrolling
        
        units = get_possible_units(os.path.basename(next_image_path))
        for i, unit in enumerate(units):
            Button(frame, text=f"Unit {unit}", command=lambda u=unit: move_and_show_next(next_image_path, u, image_files)).grid(row=0, column=i)
    else:
        print("No more images to display.")

# Function to handle mouse wheel scrolling
def on_mousewheel(event):
    canvas.yview_scroll(-1*(event.delta//120), "units")
    
# Get a list of all image files
image_files = []
for dirpath, _, filenames in os.walk('./images'):
    for filename in filenames:
        if filename.endswith('.png') and 'q_' in filename:
            image_files.append(os.path.join(dirpath, filename))

# Initialize tkinter window
root = Tk()
root.title("Question Sorter")
root.geometry("1800x1000")

# Initialize scrollbar
scrollbar = Scrollbar(root, orient=VERTICAL)
scrollbar.pack(side="right", fill="y")

# Initialize canvas
canvas = Canvas(root, yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)

# Bind the mouse wheel scrolling event
canvas.bind_all("<MouseWheel>", on_mousewheel)

# Connect scrollbar to canvas
scrollbar.config(command=canvas.yview)

# Add a frame in the canvas
frame = Canvas(canvas)
canvas_frame = canvas.create_window((0, 0), window=frame, anchor="nw")

# Show the first image
show_next_image(image_files)

# Run the GUI
root.mainloop()
