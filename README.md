# 🗳️ Streamlit Blockchain Voting App

A simple electronic voting system built with **Streamlit** that simulates a basic **blockchain** structure. Users can vote for candidates, and every two votes are recorded in a new block containing timestamps and cryptographic hashes to ensure data integrity.

---
![image](https://github.com/user-attachments/assets/1e42ada9-d50e-46a3-820b-00541f819904)


## ✅ Features

- Vote for candidates using a unique ID (1 vote per user)
- Every 2 votes are grouped into a new blockchain block
- Each block contains:
  - Voter ID
  - Candidate chosen
  - Vote timestamp
  - Hash of previous block
  - Hash of current block
- Displays the 3 most recent blocks
- Validates the blockchain integrity
- Export all data to a CSV file

---

## 🚀 How to Run the App

Follow these steps to set up and run the app on your local machine:

### ✅ Prerequisites

Make sure you have the following installed:

- Python 3.7 or higher → https://www.python.org/downloads/
- Git → https://git-scm.com/

---

### 📦 1. Clone the repository

Open your terminal or command prompt and run:

```bash
git clone https://github.com/hugsqueen1/streamlit-vote-app.git
cd streamlit-vote-app
```
🧪 2. Create a virtual environment (optional but recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```
📥 3. Install dependencies
Once the virtual environment is activated, install the required Python dependencies:
```bash
pip install -r requirements.txt
```
🚀 4. Run the app
```bash
streamlit run app.py

```
After a few seconds, Streamlit will launch the app in your browser.
If it doesn't, copy and paste the provided local URL (usually http://localhost:8501) into your browser.
.

### 📌 Note
This application is intended for educational and demonstration purposes only and is not suitable for real election use.
