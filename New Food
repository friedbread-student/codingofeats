############################################
#                                          #
##      EatS: Food and Calorie Tracker    ##
#                                          #
############################################
import streamlit as st
import datetime
import json
import os
import pandas as pd
from dataclasses import dataclass
from typing import List, Dict, Optional

class FoodEntry:
    """Represents a single food entry with its properties"""
    def __init__(self, food: str, calories: int, date: str, time: str, meal_type: str):
        self.food = food.title()
        self.calories = calories
        self.date = date
        self.time = time
        self.meal_type = meal_type
    
    def to_dict(self) -> Dict:
        """Convert entry to dictionary for JSON serialization"""
        return {
            'food': self.food,
            'calories': self.calories,
            'date': self.date,
            'time': self.time,
            'meal_type': self.meal_type
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'FoodEntry':
        """Create FoodEntry from dictionary"""
        return cls(
            food=data['food'],
            calories=data['calories'],
            date=data['date'],
            time=data['time'],
            meal_type=data['meal_type']
        )

class FoodDatabase:
    """Handles storage and retrieval of food entries"""
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.ensure_directory_exists()
        self.entries = self.load_entries()
    
    def ensure_directory_exists(self):
        """Ensure the data directory exists"""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
    
    def load_entries(self) -> List[FoodEntry]:
        """Load entries from JSON file"""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                    return [FoodEntry.from_dict(entry) for entry in data]
        except (json.JSONDecodeError, IOError) as e:
            st.error(f"Error loading data: {e}")
        return []
    
    def save_entries(self):
        """Save entries to JSON file"""
        try:
            with open(self.file_path, 'w') as f:
                json.dump([entry.to_dict() for entry in self.entries], f, indent=4)
        except IOError as e:
            st.error(f"Error saving data: {e}")
    
    def add_entry(self, entry: FoodEntry):
        """Add a new food entry"""
        self.entries.append(entry)
        self.save_entries()
    
    def clear_entries(self):
        """Clear all entries"""
        self.entries = []
        self.save_entries()
    
    def get_entries_by_date(self, date: Optional[datetime.date] = None) -> List[FoodEntry]:
        """Filter entries by date"""
        if not date:
            return self.entries.copy()
        
        date_str = date.strftime("%B %d, %Y")
        return [entry for entry in self.entries if entry.date == date_str]

class FoodTrackerApp:
    """Main application class handling the UI and business logic"""
    def __init__(self):
        self.db = FoodDatabase("Stored Data/food_data.json")
        self.setup_ui()
    
    def setup_ui(self):
        """Configure the Streamlit UI"""
        st.set_page_config(page_title="EatS Tracker", layout="wide")
        st.title("EatS' Food and Calorie Tracker")
        st.subheader("Track your nutrition with object-oriented precision!")
        
        self.setup_sidebar()
        self.setup_main_content()
    
    def setup_sidebar(self):
        """Configure the sidebar elements"""
        with st.sidebar:
            st.header("Navigation")
            st.page_link("sleep/app.py", label="Sleep Tracker", icon="⏰")
            st.page_link("bmi.py", label="BMI Calculator", icon="⚖️")
            
            st.header("Date Filter")
            self.view_option = st.radio(
                "View by:", 
                ["Today", "All Time", "Select Date"],
                key="view_option"
            )
            
            self.selected_date = None
            if self.view_option == "Select Date":
                self.selected_date = st.date_input("Select date:", key="date_select")
    
    def setup_main_content(self):
        """Configure the main content area"""
        self.display_input_section()
        self.display_food_logs()
    
    def display_input_section(self):
        """Display the food input form"""
        with st.expander("➕ Add Food Entry", expanded=True):
            cols = st.columns([2, 1, 1])
            with cols[0]:
                food_item = st.text_input("Food Item", key="food_input")
            with cols[1]:
                calories = st.number_input("Calories", min_value=0, max_value=5000, key="calorie_input")
            with cols[2]:
                meal_type = st.selectbox(
                    "Meal", 
                    ["Breakfast", "Lunch", "Dinner", "Snack"], 
                    key="meal_input"
                )
            
            if st.button("Log Food", type="primary", key="log_food"):
                self.handle_food_entry(food_item, calories, meal_type)
    
    def handle_food_entry(self, food: str, calories: int, meal_type: str):
        """Process a new food entry"""
        if not food or not calories:
            st.warning("Please enter both food item and calories.")
            return
        
        entry_date = datetime.datetime.now().strftime("%B %d, %Y")
        entry_time = datetime.datetime.now().strftime("%H:%M")
        
        new_entry = FoodEntry(
            food=food,
            calories=calories,
            date=entry_date,
            time=entry_time,
            meal_type=meal_type
        )
        
        self.db.add_entry(new_entry)
        st.success(f"✅ Logged {food} ({calories} calories) as {meal_type}")
        st.balloons()
    
    def display_food_logs(self):
        """Display the food logs and analytics"""
        if st.button("View Food Logs", key="view_logs"):
            st.write("\n### Your Food Logs")
            
            # Get filtered entries based on view option
            if self.view_option == "Today":
                entries = self.db.get_entries_by_date(datetime.date.today())
            elif self.view_option == "Select Date" and self.selected_date:
                entries = self.db.get_entries_by_date(self.selected_date)
            else:
                entries = self.db.entries
            
            if not entries:
                st.info("No food data available for the selected period.")
                return
            
            self.display_metrics(entries)
            self.display_logs_by_date(entries)
            self.display_clear_button()
    
    def display_metrics(self, entries: List[FoodEntry]):
        """Display summary metrics"""
        total_calories = sum(entry.calories for entry in entries)
        avg_calories = total_calories / len(entries) if entries else 0
        
        col1, col2 = st.columns(2)
        col1.metric("Total Entries", len(entries))
        col2.metric("Total Calories", total_calories)
        
        # Display additional metrics in expandable section
        with st.expander("Detailed Metrics"):
            col3, col4 = st.columns(2)
            col3.metric("Average Calories per Meal", f"{avg_calories:.1f}")
            
            # Meal type distribution
            meal_counts = {}
            for entry in entries:
                meal_counts[entry.meal_type] = meal_counts.get(entry.meal_type, 0) + 1
            col4.metric("Most Frequent Meal", max(meal_counts, key=meal_counts.get) if meal_counts else "N/A")
    
    def display_logs_by_date(self, entries: List[FoodEntry]):
        """Display logs organized by date"""
        # Group entries by date
        entries_by_date = {}
        for entry in entries:
            if entry.date not in entries_by_date:
                entries_by_date[entry.date] = []
            entries_by_date[entry.date].append(entry)
        
        # Display each date group
        for date, date_entries in entries_by_date.items():
            with st.expander(f"🗓️ {date}"):
                # Create DataFrame for display
                display_data = [entry.to_dict() for entry in date_entries]
                df = pd.DataFrame(display_data)
                st.table(df)
                
                # Show daily summary
                daily_total = sum(entry.calories for entry in date_entries)
                st.write(f"**Total for {date}: {daily_total} calories**")
                
                # Visualize meal distribution
                meal_summary = {}
                for entry in date_entries:
                    meal_summary[entry.meal_type] = meal_summary.get(entry.meal_type, 0) + entry.calories
                st.bar_chart(meal_summary)
    
    def display_clear_button(self):
        """Display the clear data button with confirmation"""
        if st.button("Clear All Data", type="secondary"):
            if st.checkbox("Are you sure you want to delete all food data?"):
                self.db.clear_entries()
                st.warning("All food data has been cleared!")

# Run the application
if __name__ == "__main__":
    app = FoodTrackerApp()
