######################################
#                                    #
##        EatS: Sleep Tracker       ##
#                                    #
######################################
import streamlit as st
import datetime
import json
import os
import pandas as pd
from dataclasses import dataclass
from typing import List, Dict, Literal, Optional
from enum import Enum

class SleepType(Enum):
    NAP = "Nap"
    SLEEP = "Sleep"

class SleepStatus(Enum):
    UNDERSLEPT = "Underslept"
    OVERSLEPT = "Overslept"
    ADEQUATE = "Adequate"

@dataclass
class SleepRecord:
    """Represents a single sleep record"""
    date: str
    sleep_type: SleepType
    target_hours: int
    target_minutes: int
    actual_hours: int
    actual_minutes: int
    status: SleepStatus
    
    @property
    def total_actual_hours(self) -> float:
        """Calculate total actual sleep time in decimal hours"""
        return self.actual_hours + self.actual_minutes / 60
    
    @property
    def total_target_hours(self) -> float:
        """Calculate total target sleep time in decimal hours"""
        return self.target_hours + self.target_minutes / 60
    
    def to_dict(self) -> Dict:
        """Convert record to dictionary for JSON serialization"""
        return {
            "date": self.date,
            "sleep_type": self.sleep_type.value,
            "target_hours": self.target_hours,
            "target_minutes": self.target_minutes,
            "actual_hours": self.actual_hours,
            "actual_minutes": self.actual_minutes,
            "total_actual": self.total_actual_hours,
            "total_target": self.total_target_hours,
            "status": self.status.value
        }

class SleepRepository:
    """Handles storage and retrieval of sleep records"""
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.ensure_directory_exists()
    
    def ensure_directory_exists(self):
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
    
    def load_records(self) -> List[Dict]:
        """Load records from JSON file"""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r") as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            st.error(f"Error loading sleep data: {e}")
        return []
    
    def save_record(self, record: SleepRecord):
        """Save a new sleep record"""
        records = self.load_records()
        records.append(record.to_dict())
        
        try:
            with open(self.file_path, "w") as f:
                json.dump(records, f, indent=4)
        except IOError as e:
            st.error(f"Error saving sleep data: {e}")

class SleepAnalyzer:
    """Handles sleep analysis and recommendations"""
    @staticmethod
    def determine_status(actual: float, target: float) -> SleepStatus:
        """Determine sleep status based on actual vs target"""
        if actual < target:
            return SleepStatus.UNDERSLEPT
        elif actual > target:
            return SleepStatus.OVERSLEPT
        return SleepStatus.ADEQUATE
    
    @staticmethod
    def get_recommendation(status: SleepStatus, sleep_type: SleepType) -> str:
        """Get personalized sleep recommendation"""
        if status == SleepStatus.UNDERSLEPT:
            if sleep_type == SleepType.NAP:
                return "Consider a short power nap (20-30 mins) to recharge."
            return "Aim for consistent bedtimes and limit screen time before bed."
        elif status == SleepStatus.OVERSLEPT:
            if sleep_type == SleepType.NAP:
                return "Long naps can cause sleep inertia. Keep naps under 30 minutes."
            return "Oversleeping can disrupt your circadian rhythm. Set an alarm."
        return "Great job maintaining healthy sleep habits!"

class SleepTrackerApp:
    """Main application class for the Sleep Tracker"""
    def __init__(self):
        self.repository = SleepRepository("Stored Data/sleep_data.json")
        self.analyzer = SleepAnalyzer()
        self.setup_ui()
    
    def setup_ui(self):
        """Configure the Streamlit interface"""
        st.set_page_config(page_title="EatS Sleep Tracker", layout="wide")
        st.title("Sleep Tracker")
        st.subheader("Optimize your sleep patterns for better health")
        
        self.display_input_section()
        self.display_history_section()
        self.display_navigation()
    
    def display_input_section(self):
        """Display the sleep input form"""
        with st.form("sleep_form"):
            # Sleep type selection
            sleep_type = st.radio(
                "Sleep Type:",
                [SleepType.NAP.value, SleepType.SLEEP.value],
                horizontal=True
            )
            sleep_type_enum = SleepType(sleep_type)
            
            # Target sleep inputs
            st.subheader("Target Sleep")
            target_col1, target_col2 = st.columns(2)
            with target_col1:
                target_hours = st.number_input(
                    f"Target {sleep_type.lower()} hours:",
                    min_value=0,
                    max_value=24 if sleep_type_enum == SleepType.SLEEP else 5,
                    step=1,
                    key=f"target_hours_{sleep_type.lower()}"
                )
            with target_col2:
                target_minutes = st.number_input(
                    f"Target {sleep_type.lower()} minutes:",
                    min_value=0,
                    max_value=59,
                    step=1,
                    key=f"target_minutes_{sleep_type.lower()}"
                )
            
            # Actual sleep inputs
            st.subheader("Actual Sleep")
            today = datetime.date.today().strftime("%B %d, %Y")
            actual_col1, actual_col2 = st.columns(2)
            with actual_col1:
                actual_hours = st.number_input(
                    f"Actual {sleep_type.lower()} hours:",
                    min_value=0,
                    step=1,
                    key=f"actual_hours_{sleep_type.lower()}"
                )
            with actual_col2:
                actual_minutes = st.number_input(
                    f"Actual {sleep_type.lower()} minutes:",
                    min_value=0,
                    max_value=59,
                    step=1,
                    key=f"actual_minutes_{sleep_type.lower()}"
                )
            
            submitted = st.form_submit_button("Log Sleep")
            
            if submitted:
                self.process_sleep_entry(
                    sleep_type_enum,
                    target_hours,
                    target_minutes,
                    actual_hours,
                    actual_minutes,
                    today
                )
    
    def process_sleep_entry(self, sleep_type: SleepType, target_h: int, target_m: int, 
                          actual_h: int, actual_m: int, date: str):
        """Process and store a new sleep entry"""
        try:
            if not (target_h or target_m):
                st.warning("Please enter target sleep time.")
                return
            
            if not (actual_h or actual_m):
                st.warning("Please enter actual sleep time.")
                return
            
            total_actual = actual_h + actual_m / 60
            total_target = target_h + target_m / 60
            
            status = self.analyzer.determine_status(total_actual, total_target)
            recommendation = self.analyzer.get_recommendation(status, sleep_type)
            
            record = SleepRecord(
                date=date,
                sleep_type=sleep_type,
                target_hours=target_h,
                target_minutes=target_m,
                actual_hours=actual_h,
                actual_minutes=actual_m,
                status=status
            )
            
            self.repository.save_record(record)
            
            # Display results
            st.success(f"Sleep logged for {date}")
            st.metric(
                label="Sleep Status",
                value=status.value,
                delta=f"{total_actual:.1f}h (actual) vs {total_target:.1f}h (target)"
            )
            st.info(f"Recommendation: {recommendation}")
            
        except Exception as e:
            st.error(f"Error processing sleep data: {str(e)}")
    
    def display_history_section(self):
        """Display sleep history and trends"""
        st.subheader("Sleep History")
        records = self.repository.load_records()
        
        if not records:
            st.info("No sleep records available yet.")
            return
        
        df = pd.DataFrame(records)
        
        # Show latest record summary
        latest = df.iloc[-1]
        cols = st.columns(3)
        cols[0].metric("Last Sleep", latest["sleep_type"])
        cols[1].metric("Actual", f"{latest['total_actual']:.1f} hours")
        cols[2].metric("Status", latest["status"])
        
        # Show full history
        with st.expander("View All Records"):
            st.dataframe(df.sort_values("date", ascending=False))
            
            # Visualization
            if len(df) > 1:
                chart_df = df[["date", "total_actual", "total_target"]].copy()
                chart_df["date"] = pd.to_datetime(chart_df["date"])
                chart_df.set_index("date", inplace=True)
                st.line_chart(chart_df)
    
    def display_navigation(self):
        """Display navigation links"""
        st.markdown("---")
        st.write("Navigate to other trackers:")
        col1, col2 = st.columns(2)
        col1.page_link("food/food.py", label="Food Tracker", icon="🍽️")
        col2.page_link("bmi.py", label="BMI Tracker", icon="⚖️")

# Run the application
if __name__ == "__main__":
    app = SleepTrackerApp()
