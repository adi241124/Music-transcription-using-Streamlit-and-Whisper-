import streamlit as st
import os
import whisper

def save_uploaded_file(uploaded_file, save_path):
    with open(os.path.join(save_path, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())

def load_whisper_model():
    model = whisper.load_model("base")
    return model

model = load_whisper_model()

def transcribe_audio(mp3_filepath):
    # Transcribe using whisper
    result = model.transcribe(mp3_filepath)
    transcription = result['text']
    return transcription

def main():
    st.title("Song Transcriber")

    # File uploader widget allowing multiple file uploads
    uploaded_files = st.file_uploader("Upload audio files (up to 5)", type="mp3", accept_multiple_files=True)

    if uploaded_files is not None and len(uploaded_files) <= 5:
        save_path = "audio_files"  # Folder to save the uploaded files
        os.makedirs(save_path, exist_ok=True)

        # Process each uploaded file
        transcriptions = []
        for uploaded_file in uploaded_files:
            # Display the uploaded file
            st.audio(uploaded_file, format='audio/mp3')

            # Save the uploaded file
            save_uploaded_file(uploaded_file, save_path)
            st.success(f"Audio file '{uploaded_file.name}' uploaded successfully.")

            # Transcribe the audio
            transcribed_text = transcribe_audio(os.path.join(save_path, uploaded_file.name))
            transcriptions.append((uploaded_file.name, transcribed_text))

        # Display transcriptions
        st.subheader("Transcribed Texts:")
        for filename, transcription in transcriptions:
            st.text_area(f"Transcribed Text for {filename}", value=transcription, height=200)

    elif uploaded_files is not None:
        st.warning("Please upload up to 5 audio files.")

if __name__ == "__main__":
    main()