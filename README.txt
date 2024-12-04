# Generate Audio for Word List

This Python project generates MP3 files from a word list in an Excel file. Each word pair (German and English) is converted into audio using Google Text-to-Speech (gTTS) and combined into MP3 chunks for convenient playback.

---

## Setup Instructions

### 1. Install Python 3.10

brew install ffmpeg

python3.10 -m venv myenv

deactivate
source myenv/bin/activate

pip install --upgrade pip

pip install pandas gtts pydub openpyxl

ffmpeg -version

python3 runscript.py