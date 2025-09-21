# 🌍 Sustainable Development Goals Evaluation Web App
A web application for evaluating SDG indicators (I1–I34). Users can input years and scores, calculate total and weighted results, and visualize performance. Includes session-based submission control, improvement suggestions, and a random score generator for testing.
 

The app ensures **unique submissions** through session IDs, provides **visual performance representation**, and suggests **improvements for specific indicators**.  

---

## ✨ Features
- Interactive interface for scoring SDG indicators  
- Reference and evaluation year input  
- Automatic calculation of total and weighted scores  
- Prevention of duplicate submissions via session ID  
- Visualization of institutional performance through charts  
- Random score generator (optional, for testing)  

---


## 🛠 Installation & Setup

### 1. Prerequisites
- **Python >= 3.8**  
  Check with:  
  ```bash
  python --version
- pip (Python package manager)
  Check with:

      pip --version


- Flask
Install with:

      pip install flask

- MySQL Server 8.0

      Windows: MySQL Installer

- Linux:

      sudo apt update
      sudo apt install mysql-server



## 🚀 Usage Instructions

### 1. Accessing the Application
- Start the local server and open: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  
- No username is required. The app uses session IDs to identify users and prevent duplicate submissions.  

### 2. Workspace Overview
- The main page displays SDGs and criteria (I1–I34).  
- For each indicator you can see:  
  - Weight  
  - Reference year  
  - Evaluation year  
  - User score  
  - Total score  
  - Weighted score  
- At the bottom, there are buttons for **random score generation** and **evaluation submission**.  

### 3. Entering Years
- Select the reference year and/or evaluation year (depending on the indicator type).  
- You can change your selection until you submit the evaluation.  
- ⚠️ All year fields must be filled. Otherwise, a warning will appear.  

### 4. Entering Scores
- Click on the score field to select from available values.  
- For percentage change indicators, enter numerator and denominator values for both years.  
- ⚠️ All score fields must be completed before submission.  

### 5. Submitting and Viewing Results
- Click **Submit Evaluation** to save your scores.  
- The app calculates and displays:  
  - Total score per indicator  
  - Weighted score per indicator (score × weight)  
  - Final institutional score  
- Indicators needing improvement show a message with suggestions.  

### 6. Performance Visualization
- A bar chart at the bottom of the page shows weighted scores in ascending order.  
- Hover over a bar to view detailed values.  

### 7. Optional Features
- Use the **Random Values** button to auto-fill years and scores for quick testing.  

### 8. Known Issues
- No validation if the reference year is greater than the evaluation year.  
- Different evaluation years per indicator may affect visualization accuracy.  

---

⚠️ Notes & Common Issues

Duplicate submissions are prevented using session IDs.

To submit a new evaluation, open a fresh browser window via the application link.

Common Errors

ModuleNotFoundError: No module named 'flask' → Run:
pip install flask

Access denied for user 'root@localhost' → Verify MySQL credentials in database.py.


## 📂 Repository Structure

project-root

├── static/ # CSS, JS, and assets

├── templates/ # HTML templates

├── app.py # Main application file 

├── requirements.txt # Dependencies

└── README.md # Project description and usage


