import streamlit as st
from datetime import date, timedelta
import random

# --- 1. Configuration & Initial Data ---

# Define categories and their corresponding colors for visual consistency
CATEGORIES = {
    'Health': 'red',
    'Learning': 'blue',
    'Productivity': 'purple',
    'Fitness': 'green',
    'Mindfulness': 'orange'
}


# Mock data initialization using today's date context
# NOTE: The streak logic in this simplified version relies on accurate date handling.
def get_mock_habits():
    today = date.today().isoformat()
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    day_before = (date.today() - timedelta(days=2)).isoformat()

    return [
        {
            'id': 1,
            'name': 'Morning Exercise',
            'category': 'Health',
            'color': CATEGORIES['Health'],
            'streak': 2,
            'completedDates': [yesterday, today],  # Completed 2 days in a row
            'targetDays': 30
        },
        {
            'id': 2,
            'name': 'Read 30 Minutes',
            'category': 'Learning',
            'color': CATEGORIES['Learning'],
            'streak': 1,
            'completedDates': [today],  # Completed only today
            'targetDays': 100
        },
        {
            'id': 3,
            'name': 'Drink 8 Glasses Water',
            'category': 'Health',
            'color': CATEGORIES['Health'],
            'streak': 0,
            'completedDates': [day_before],  # Not completed yesterday or today (Streak broken)
            'targetDays': 60
        }
    ]


# --- 2. State Initialization ---
if 'habits' not in st.session_state:
    st.session_state.habits = get_mock_habits()
if 'show_form' not in st.session_state:
    st.session_state.show_form = False
if 'today_str' not in st.session_state:
    st.session_state.today_str = date.today().isoformat()


# --- 3. Core Logic Functions ---

def calculate_streak(completed_dates_list):
    """Calculates the current streak based on a list of ISO-formatted dates."""
    dates = sorted([date.fromisoformat(d) for d in completed_dates_list], reverse=True)

    if not dates or dates[0] < date.today():
        # If the last recorded date is not today, the streak is 0.
        # However, for demonstration, we'll keep the simple "last completed days in a row" logic.
        pass

    current_streak = 0
    reference_date = date.today()

    # Check if today is completed to start the streak from the right day
    if reference_date.isoformat() in completed_dates_list:
        current_streak = 1
        reference_date -= timedelta(days=1)

    # Check continuous days backward
    while True:
        target_date = reference_date.isoformat()
        if target_date in completed_dates_list:
            current_streak += 1
            reference_date -= timedelta(days=1)
        else:
            break

    return current_streak


def toggle_habit_today(habit_id):
    """Marks a habit complete/incomplete for the current day and updates the streak."""
    today_str = st.session_state.today_str

    new_habits = []
    for habit in st.session_state.habits:
        if habit['id'] == habit_id:
            is_completed_today = today_str in habit['completedDates']

            if is_completed_today:
                # Remove today's date
                new_completed = [d for d in habit['completedDates'] if d != today_str]
            else:
                # Add today's date
                new_completed = habit['completedDates'] + [today_str]

            # Recalculate streak based on the new completed dates
            new_streak = calculate_streak(new_completed)

            new_habits.append({
                **habit,
                'completedDates': new_completed,
                'streak': new_streak
            })
        else:
            new_habits.append(habit)

    st.session_state.habits = new_habits


def add_new_habit():
    """Adds a new habit to the list."""
    if st.session_state.new_habit_name.strip():
        new_habit = {
            'id': random.randint(1000, 9999),
            'name': st.session_state.new_habit_name.strip(),
            'category': st.session_state.new_habit_category,
            'color': CATEGORIES[st.session_state.new_habit_category],
            'streak': 0,
            'completedDates': [],
            'targetDays': st.session_state.new_habit_target
        }
        st.session_state.habits.append(new_habit)
        st.session_state.show_form = False

        # Clear form inputs after submission (optional but clean)
        st.session_state.new_habit_name = ''
        st.session_state.new_habit_target = 30


def delete_habit(habit_id):
    """Deletes a habit by ID."""
    st.session_state.habits = [h for h in st.session_state.habits if h['id'] != habit_id]


def get_last_7_days():
    """Returns a list of the last 7 days (including today) for the calendar."""
    days = []
    for i in range(6, -1, -1):
        date_obj = date.today() - timedelta(days=i)
        days.append({
            'date_str': date_obj.isoformat(),
            'label': date_obj.strftime('%a'),
            'is_today': i == 0
        })
    return days


# --- 4. UI Rendering ---

st.set_page_config(layout="wide", page_title="Habit Tracker")

# Custom CSS for styling (Mimicking Tailwind gradients and dark mode)
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #4c2c77, #721d7b, #c4307f); 
    background-attachment: fixed;
    color: white;
}
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown p {
    color: white !important;
}
div[data-testid="stMetricValue"] {
    font-size: 3rem !important;
    font-weight: bold;
}
/* Style the habit tracker cards */
.habit-card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(5px);
    border-radius: 1rem;
    padding: 1.5rem;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    transition: background 0.3s;
}
.habit-card:hover {
    background: rgba(255, 255, 255, 0.15);
}
.category-badge-red { background: linear-gradient(90deg, #EF4444, #F97316); padding: 2px 8px; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }
.category-badge-blue { background: linear-gradient(90deg, #3B82F6, #4F46E5); padding: 2px 8px; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }
.category-badge-purple { background: linear-gradient(90deg, #A855F7, #EC4899); padding: 2px 8px; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }
.category-badge-green { background: linear-gradient(90deg, #10B981, #059669); padding: 2px 8px; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }
.category-badge-orange { background: linear-gradient(90deg, #F59E0B, #EA580C); padding: 2px 8px; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }

</style>
""", unsafe_allow_html=True)


def habit_tracker_app():
    # --- Statistics ---
    habits = st.session_state.habits
    today_str = st.session_state.today_str

    total_streaks = sum(h['streak'] for h in habits)
    completed_today = len([h for h in habits if today_str in h['completedDates']])

    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h1><span style='font-size: 2.5rem;'>🎯</span> Habit Tracker</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #ccc;'>Build better habits, one day at a time</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Stats Dashboard (3 Columns)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="habit-card" style="background: linear-gradient(135deg, #EF4444, #F97316);">
            <div style="color: white; opacity: 0.9;">Total Streaks <span style="float: right;">🔥</span></div>
            <div style="font-size: 2.5rem; font-weight: bold;">{total_streaks}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="habit-card" style="background: linear-gradient(135deg, #10B981, #059669);">
            <div style="color: white; opacity: 0.9;">Completed Today <span style="float: right;">🏆</span></div>
            <div style="font-size: 2.5rem; font-weight: bold;">{completed_today}/{len(habits)}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="habit-card" style="background: linear-gradient(135deg, #3B82F6, #4F46E5);">
            <div style="color: white; opacity: 0.9;">Active Habits <span style="float: right;">📈</span></div>
            <div style="font-size: 2.5rem; font-weight: bold;">{len(habits)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --- Add Habit Button & Form ---

    btn_col, _ = st.columns([1, 4])
    with btn_col:
        st.button(
            "➕ Add Habit",
            on_click=lambda: st.session_state.update(show_form=True),
            use_container_width=True
        )

    if st.session_state.show_form:
        st.markdown('<div class="habit-card">', unsafe_allow_html=True)
        st.subheader("Create New Habit")

        # Form Inputs
        col_name, col_cat = st.columns(2)
        with col_name:
            st.text_input("Habit Name", key='new_habit_name', placeholder="e.g., Meditate 10 minutes")
        with col_cat:
            st.selectbox("Category", options=list(CATEGORIES.keys()), key='new_habit_category')

        st.number_input("Target Days", min_value=1, value=30, key='new_habit_target')

        col_create, col_cancel = st.columns(2)
        with col_create:
            st.button("Create Habit", on_click=add_new_habit, use_container_width=True, type="primary")
        with col_cancel:
            st.button("Cancel", on_click=lambda: st.session_state.update(show_form=False), use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # --- Habit List ---

    st.markdown("## Your Habits")
    last_7_days = get_last_7_days()

    for habit in habits:
        progress = (len(habit['completedDates']) / habit['targetDays']) * 100
        is_completed_today = today_str in habit['completedDates']

        st.markdown('<div class="habit-card">', unsafe_allow_html=True)

        # Habit Header and Delete Button
        header_cols = st.columns([6, 1])
        with header_cols[0]:
            st.markdown(f"### {habit['name']} <span class='category-badge-{habit['color']}'>{habit['category']}</span>",
                        unsafe_allow_html=True)
        with header_cols[1]:
            st.button("❌", key=f"del_{habit['id']}", on_click=delete_habit, args=(habit['id'],))

        # Streak and Goal
        st.markdown(f"""
            <p style='color: #ccc; margin-top: -10px;'>
                🔥 **{habit['streak']}** day streak | Target: **{habit['targetDays']}** days
            </p>
        """, unsafe_allow_html=True)

        # Progress Bar
        st.progress(min(progress / 100, 1.0), text=f"Progress: {progress:.0f}%")

        st.markdown("---")

        # Day Calendar and Checkboxes (8 columns: Label + 7 Days)
        calendar_cols = st.columns(8)

        calendar_cols[0].markdown("**Calendar**", unsafe_allow_html=True)

        for i, day in enumerate(last_7_days):
            is_completed = day['date_str'] in habit['completedDates']

            with calendar_cols[i + 1]:
                st.markdown(
                    f"<div style='text-align: center; color: {'white' if day['is_today'] else '#ccc'}; font-weight: {'bold' if day['is_today'] else 'normal'};'>{day['label']}</div>",
                    unsafe_allow_html=True)

                # Checkbox only enabled for today
                if day['is_today']:
                    st.checkbox(
                        label="✓",
                        value=is_completed,
                        key=f"check_{habit['id']}",
                        on_change=toggle_habit_today,
                        args=(habit['id'],),
                        label_visibility="collapsed"
                    )
                else:
                    # Display past days visually
                    status_color = 'green' if is_completed else '#666'
                    status_text = '✓' if is_completed else '—'

                    st.markdown(f"""
                        <div style='text-align: center; font-size: 1.5rem; color: {status_color};'>
                            {status_text}
                        </div>
                    """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    if not habits:
        st.markdown(
            """
            <div style="text-align: center; padding: 40px; background: rgba(255, 255, 255, 0.1); border-radius: 1rem;">
                <span style="font-size: 2rem;">🌟</span>
                <p style="font-size: 1.25rem; color: white;">No habits yet. Click '➕ Add Habit' to begin your journey!</p>
            </div>
            """, unsafe_allow_html=True
        )


if __name__ == '__main__':
    habit_tracker_app()