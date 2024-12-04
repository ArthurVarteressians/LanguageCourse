import pandas as pd
from gtts import gTTS
from pydub import AudioSegment
import os

# Load the Excel file
file_path = 'word_list.xlsx'  # Replace with your Excel file name
data = pd.read_excel(file_path, usecols="A,B", header=None, names=['German', 'English'])

# Get the first 500 rows
rows = data.head(500)

# Create output directory
combined_dir = 'Version1-2'
os.makedirs(combined_dir, exist_ok=True)

# Silence durations in milliseconds
pause_after_german = 1600  # Pause after German word for repeating
pause_after_english = 1500  # Pause after English word for listening
pause_between_words = 2000  # Pause between rows

# Pitch adjustment factor for German voice (negative to lower pitch)
pitch_factor = -2  # Slight pitch adjustment for a natural male voice

# Group rows in chunks of 10
chunk_size = 10
num_chunks = len(rows) // chunk_size + (1 if len(rows) % chunk_size != 0 else 0)

print("Generating MP3 files with repeated English words and improved male German voices for chunks of 10 rows...")

for i in range(num_chunks):
    # Get the start and end index for the current chunk
    start_idx = i * chunk_size
    end_idx = min((i + 1) * chunk_size, len(rows))

    # Combine the German and English text for the chunk
    combined_audio = AudioSegment.empty()  # Start with an empty audio segment

    for idx in range(start_idx, end_idx):
        german_word = rows.iloc[idx]['German']
        english_word = rows.iloc[idx]['English']

        # Generate audio for the German word
        tts_german = gTTS(text=german_word, lang='de')
        tts_german.save("temp_german.mp3")
        german_audio = AudioSegment.from_file("temp_german.mp3")

        # Adjust the pitch of the German voice
        german_audio = german_audio._spawn(german_audio.raw_data, overrides={
            "frame_rate": int(german_audio.frame_rate * (2.0 ** (pitch_factor / 12.0)))
        }).set_frame_rate(german_audio.frame_rate)

        # Generate audio for the English word
        tts_english = gTTS(text=english_word, lang='en')
        tts_english.save("temp_english.mp3")
        english_audio = AudioSegment.from_file("temp_english.mp3")

        # Combine German and English with pauses
        combined_audio += german_audio
        combined_audio += AudioSegment.silent(duration=pause_after_german)  # Pause after German word
        combined_audio += english_audio
        combined_audio += AudioSegment.silent(duration=pause_after_english)  # Pause after first English word
        combined_audio += english_audio  # Repeat English word
        combined_audio += AudioSegment.silent(duration=pause_between_words)  # Pause between rows

    # Generate the MP3 for the chunk
    output_file = f"{combined_dir}/chunk_{i+1:03d}.mp3"
    combined_audio.export(output_file, format="mp3")
    print(f"Generated: {output_file}")

# Cleanup temporary files
if os.path.exists("temp_german.mp3"):
    os.remove("temp_german.mp3")
if os.path.exists("temp_english.mp3"):
    os.remove("temp_english.mp3")

print("\nAll chunked MP3 files with repeated English words and improved male German voices generated successfully!")
