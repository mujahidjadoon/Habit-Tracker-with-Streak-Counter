# 🎯 Habit Tracker with Streaks (Streamlit)

A beautiful, motivating, and interactive web application to **track daily habits** and **build powerful completion streaks**. Built with Python and Streamlit, this app helps users maintain consistency and track progress toward long-term goals.

---

## ✨ Features

* **Custom Habit Creation:** Easily add new habits with custom names, target days (goals), and categories (Health, Learning, Fitness, etc.).
* **Dynamic Streak Counter:** The application dynamically calculates and displays the current **streak** (consecutive days completed) with motivational indicators (e.g., 🔥).
* **7-Day Visual Calendar:** Each habit card includes a clear visual calendar showing completion status for the last seven days, making consistency easy to spot.
* **Progress Tracking:** Displays a progress bar indicating how close the user is to their long-term **target day goals**.
* **Statistics Dashboard:** A header dashboard summarizes total ongoing streaks, habits completed today, and the number of active habits.
* **Persistence:** All habit data (including streaks and completed dates) is managed using **Streamlit Session State** for the duration of the session.

---

## 💻 Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend/App Framework** | **Streamlit** (Python) | Creates the interactive, data-driven web interface. |
| **State Management** | **Streamlit Session State** | Persists habit data, streaks, and the calendar state across interactions. |
| **Date & Time** | `datetime` (Python Standard Library) | Crucial for calculating streaks and managing the 7-day calendar view. |

---

## 🚀 How to Run Locally

### Prerequisites
Ensure you have **Python 3.8+** installed.

### Installation Steps
1.  **Clone the repository:**
    ```bash
    git clone [YOUR_REPOSITORY_URL]
    cd [Your-Repository-Name]
    ```
2.  **Install dependencies** using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Streamlit application:**
    ```bash
    streamlit run main.py
    ```

---

## 📤 Next Step: Uploading to GitHub

If you haven't pushed your files yet, use the following commands in your project's terminal:

1.  **Stage all files (`main.py`, `requirements.txt`, `README.md`):**
    ```bash
    git add .
    ```
2.  **Commit your changes:**
    ```bash
    git commit -m "Feat: Habit Tracker with streak calculation and dashboard."
    ```
3.  **Push to your GitHub repository:**
    ```bash
    git push
    ```

Would you like to move on to the next project idea, or do you have any other questions about the Habit Tracker?
