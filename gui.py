import joblib
import subprocess
import numpy as np
from tkinter import *
# import simpleaudio as sa
from tkinter import filedialog
from playsound import playsound

# Load the trained XGBoost model for gender recognition
gender_classes = ['Male', 'Female']
gender_model = joblib.load('xgboost_model.pkl')

# Initialize GUI
root = Tk()
root.geometry('800x600')
root.title("Gender Recognition from Voice")
root.configure(background='#CDCDCD')

# Define Labels to be displayed
result_label = Label(root, background="#CDCDCD", font=('arial', 15, 'bold'))

def play_audio(audio_file_path):
    """
    Play the audio.

    Args:
    - audio_file_path (str): The path to the audio file.

    Returns:
    None
    """
    playsound(audio_file_path)

def recognize_gender(audio_file_path):
    """
    Perform gender recognition on the given audio file path.

    Args:
    - audio_file_path (str): The path to the input audio file.

    Returns:
    None
    """

    # Call the R script to extract audio features
    r_script_result = subprocess.run(['Rscript', 'voice_analysis.R', audio_file_path], capture_output=True, text=True)
    if r_script_result.returncode != 0:
        print("Error:", r_script_result.stderr)
        return

    # Predict gender using the XGBoost model
    audio_features = [float(value) for value in r_script_result.stdout.split() if '.' in value]
    audio_features = np.array(audio_features, dtype=float).reshape(1, -1)
    pred_gender = gender_classes[gender_model.predict(audio_features)[0]]

    # Display the recognized gender
    print("Detected gender:", pred_gender)
    result_label.configure(foreground="#011638", text="Gender: {}".format(pred_gender))

def show_recognize_btn(audio_file_path):
    """
    Show the 'Recognize Gender' button after an audio file is uploaded.

    Args:
    - audio_file_path (str): The path to the input audio file.

    Returns:
    None
    """
    recognize_btn = Button(root, 
        text="Recognize Gender", 
        command=lambda: recognize_gender(audio_file_path),
        padx=10, pady=5
    )

    recognize_btn.configure(
        background="#364156",
        foreground="white",
        font=('arial', 10, 'bold')
    )

    recognize_btn.place(relx=0.42, rely=0.46)

    # Show 'Play Audio' button
    play_btn = Button(root,
        text="Play Audio",
        command=lambda: play_audio(audio_file_path),
        padx=10, pady=5
    )

    play_btn.configure(
        background="#364156",
        foreground="white",
        font=('arial', 10, 'bold')
    )

    play_btn.place(relx=0.44, rely=0.60)

def upload_audio():
    """
    Open a file dialog to upload an audio file and display it.

    Args:
    None

    Returns:
    None
    """
    try:
        audio_filepath = filedialog.askopenfilename()
        
        # Display the audio file path to the user
        audio_filepath_label.configure(text="Audio File: {}".format(audio_filepath))
        
        # Show the 'Recognize Gender' button
        show_recognize_btn(audio_filepath)

    except Exception as e:
        print("Error:", e)

# Uploading Audio for Gender Recognition
upload_button = Button(root, text="Upload Audio", command=upload_audio, padx=10, pady=5)
upload_button.configure(background="#364156", foreground="white", font=('arial', 10, 'bold'))
upload_button.pack(side="bottom", expand=True)

# Label to display the audio file path
audio_filepath_label = Label(root, text="", background="#CDCDCD", font=('arial', 10))
audio_filepath_label.pack(side="bottom", expand=True)

# Label to display the recognition result
result_label.pack(side="bottom", expand=True) 

# Set Heading / Title
heading_label = Label(root, text="Gender Recognition from Voice", pady=20, font=('arial', 20, 'bold'))
heading_label.configure(background="#CDCDCD", foreground="#364156")
heading_label.pack()

# Start program
root.mainloop()

# DEBUG
print("Done")
