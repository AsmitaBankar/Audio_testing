import wave
import audioop
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def vad(audio_file):
    # Read the audio file
    audio = wave.open(audio_file, 'rb')
    frame_rate = audio.getframerate()
    sample_width = audio.getsampwidth()

    # Initialize variables
    buffer_size = 1024
    speech_segments = []
    start_time = None
    end_time = None

    while True:
        frames = audio.readframes(buffer_size)
        if not frames:
            break

        # Calculate energy of the frame
        energy = audioop.rms(frames, sample_width)
        if energy > 500:  
            if start_time is None:
                start_time = audio.tell() / frame_rate
        else:
            if start_time is not None:
                end_time = audio.tell() / frame_rate
                speech_segments.append((start_time, end_time))
                start_time = end_time = None

    # Close audio file
    audio.close()
    return speech_segments

# Function to handle file selection and VAD process
def process_audio():
    audio_file = filedialog.askopenfilename(title="Select an Audio File", filetypes=[("WAV Files", "*.wav")])
    if not audio_file:
        return  # If no file is selected, do nothing
    
    try:
        detected_segments = vad(audio_file)
        if detected_segments:
            result_box.delete(1.0, tk.END)  # Clear previous results
            result_box.insert(tk.END, "Detected Speech Segments:\n", "heading")
            for i, (start, end) in enumerate(detected_segments, start=1):
                result_box.insert(tk.END, f"Segment {i}: {start:.1f}s - {end:.1f}s\n", "text")
        else:
            messagebox.showinfo("No Speech Detected", "No speech detected in the selected audio file.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Setting up the GUI
root = tk.Tk()
root.title("Voice Activity Detection (VAD)")
root.geometry("500x450")
root.config(bg="#f2f2f2")  # Set background color for the main window

# Styling for the label
label = tk.Label(root, text="Voice Activity Detection", font=("Helvetica", 18, "bold"), fg="#333333", bg="#f2f2f2")
label.pack(pady=15)

# Styling for the "Select Audio File" button with a green color
select_button = tk.Button(root, text="Select Audio File", command=process_audio, font=("Arial", 14), 
                          bg="#4CAF50", fg="purple", activebackground="#45a049", 
                          relief="raised", bd=4, padx=10, pady=5)
select_button.pack(pady=10)

# Add a scrolled text box to display the results with colors for text
result_box = scrolledtext.ScrolledText(root, width=55, height=15, wrap=tk.WORD, font=("Arial", 12), bd=5, relief="groove")
result_box.tag_configure("heading", foreground="green", font=("Arial", 12, "bold"))
result_box.tag_configure("text", foreground="black", font=("Arial", 12))
result_box.pack(pady=15)

# Add a frame for aesthetics (you can customize this to hold other buttons, icons, etc.)
frame = tk.Frame(root, bg="#333333", height=40)
frame.pack(fill=tk.X, padx=10, pady=5)

# Start the main loop for the GUI
root.mainloop()