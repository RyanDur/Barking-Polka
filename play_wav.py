try:
    from playsound import playsound
    audio_file = "output.wav"  # Replace with the actual path
    playsound(audio_file)
except ImportError:
    print("playsound library is not installed. Please install it using: pip install playsound")
except Exception as e:
    print(f"An error occurred: {e}")