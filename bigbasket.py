from tkinter import *
from PIL import Image, ImageTk
import cv2

# Global variables for theme color and offer text
theme_color = "white"
offer_text = ""

# Function to apply the selected theme and display the options
def apply_theme():
    global theme_color, offer_text
    theme_color = color_entry.get()
    offer_text = offer_entry.get()
    
    clear_frame()  # Clear the input frame
    show_options_page()  # Show options for generating image or video

# Show options for generating image or video
def show_options_page():
    root.configure(bg=theme_color)
    clear_frame()
    Label(root, text="Select an option:", bg=theme_color, font=("Arial", 14)).pack(pady=20)

    Button(root, text="Generate Image", command=show_image_page, bg=theme_color).pack(pady=10)
    Button(root, text="Generate Video", command=show_video_page, bg=theme_color).pack(pady=10)

# Show the image page
def show_image_page():
    clear_frame()
    try:
        img = Image.open('image.png')
        # Resize to fit the window, leaving space for the back button
        img = img.resize((root.winfo_width(), root.winfo_height() - 100))
        imgtk = ImageTk.PhotoImage(img)

        image_label = Label(root, image=imgtk)
        image_label.image = imgtk  # Keep a reference to avoid garbage collection
        image_label.pack(fill=BOTH, expand=True)

        # Display the offer text
        Label(root, text=f"Offer: {offer_text}", bg=theme_color, font=("Arial", 14)).pack(pady=20)

        # Back button to return to options
        Button(root, text="Back", command=show_options_page, bg=theme_color).pack(pady=10)
    except FileNotFoundError:
        messagebox.showerror("Error", "Image file not found!")

# Show the video page
def show_video_page():
    clear_frame()
    global video_source
    video_source = cv2.VideoCapture('video.mp4')
    
    if not video_source.isOpened():
        messagebox.showerror("Error", "Video file not found!")
        return

    # Create a label to display the video
    video_label = Label(root)
    video_label.pack(fill=BOTH, expand=True)

    play_video(video_label)  # Start video playback

def play_video(video_label):
    global video_source
    ret, frame = video_source.read()
    
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)

        # Resize to fit the window, leaving space for the back button
        img = img.resize((root.winfo_width(), root.winfo_height() - 100))  
        imgtk = ImageTk.PhotoImage(image=img)

        video_label.imgtk = imgtk  # Keep a reference to avoid garbage collection
        video_label.configure(image=imgtk)

        # Increase speed by adjusting the delay
        video_label.after(5, lambda: play_video(video_label))  # Call again after 5 ms
    else:
        video_source.release()
        messagebox.showinfo("End", "Video playback finished.")

    # Back button to return to options, ensure only one is added
    if not hasattr(video_label, 'back_button'):
        video_label.back_button = Button(root, text="Back", command=show_options_page, bg=theme_color)
        video_label.back_button.pack(pady=10)

def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

# Creating the main window
root = Tk()
root.title("Theme and Media Selector")
root.geometry("800x600")  # Set initial size of the window

# Input frame for theme selection
input_frame = Frame(root)
input_frame.pack(pady=20)

Label(input_frame, text="Background Color:").grid(row=0, column=0)
color_entry = Entry(input_frame)
color_entry.grid(row=0, column=1)

Label(input_frame, text="Offer:").grid(row=1, column=0)
offer_entry = Entry(input_frame)
offer_entry.grid(row=1, column=1)

Button(input_frame, text="Apply", command=apply_theme).grid(row=2, columnspan=2, pady=10)

# Start the GUI loop
root.mainloop()
