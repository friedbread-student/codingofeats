#########################################
#                                       #
##          EatS: BMI Tracker          ##
#                                       #
#########################################
import math
import streamlit as st
import pandas as pd
import os
from dataclasses import dataclass
from typing import Tuple, Optional
from datetime import datetime

@dataclass
class BMIRecord:
    """Represents a single BMI measurement record"""
    date: str
    weight: float  # in kg
    height: float  # in cm
    bmi: float
    classification: str
    suggestion: str

class BMICalculator:
    """Handles BMI calculations and classifications"""
    @staticmethod
    def calculate(weight: float, height: float) -> float:
        """Calculate BMI from weight (kg) and height (cm)"""
        if height <= 0:
            raise ValueError("Height must be greater than zero")
        height_m = height / 100
        return round(weight / (height_m ** 2), 2)
    
    @staticmethod
    def classify(bmi: float) -> Tuple[str, str]:
        """Classify BMI and provide health suggestion"""
        if bmi < 18.5:
            return ("Underweight", 
                   "Consider increasing calorie intake and consult a nutritionist.")
        elif 18.5 <= bmi < 24.9:
            return ("Normal weight", 
                   "Maintain balanced diet and regular exercise.")
        elif 25 <= bmi < 29.9:
            return ("Overweight", 
                   "Focus on healthy diet, exercise, and consult a professional.")
        else:
            return ("Obese", 
                   "Consult a doctor to develop a weight loss plan.")

class BMIRepository:
    """Handles storage and retrieval of BMI records"""
    def __init__(self, file_path: str = "bmi_data.csv"):
        self.file_path = file_path
        self.ensure_file_exists()
    
    def ensure_file_exists(self):
        """Create data file with headers if it doesn't exist"""
        if not os.path.exists(self.file_path):
            df = pd.DataFrame(columns=[
                "Date", "Weight (kg)", "Height (cm)", 
                "BMI", "Classification", "Suggestion"
            ])
            df.to_csv(self.file_path, index=False)
    
    def add_record(self, record: BMIRecord):
        """Add a new BMI record to storage"""
        df = pd.read_csv(self.file_path)
        new_data = {
            "Date": record.date,
            "Weight (kg)": record.weight,
            "Height (cm)": record.height,
            "BMI": record.bmi,
            "Classification": record.classification,
            "Suggestion": record.suggestion
        }
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv(self.file_path, index=False)
    
    def get_all_records(self) -> pd.DataFrame:
        """Retrieve all BMI records"""
        if os.path.exists(self.file_path):
            return pd.read_csv(self.file_path)
        return pd.DataFrame()

class BMITrackerApp:
    """Main application class for the BMI Tracker"""
    def __init__(self):
        self.calculator = BMICalculator()
        self.repository = BMIRepository()
        self.setup_ui()
    
    def setup_ui(self):
        """Configure the Streamlit interface"""
        st.set_page_config(page_title="EatS BMI Tracker", layout="wide")
        st.title("BMI Tracker")
        st.subheader("Track your Body Mass Index over time")
        
        self.display_input_section()
        self.display_history_section()
    
    def display_input_section(self):
        """Display the BMI input and calculation form"""
        with st.form("bmi_form"):
            col1, col2 = st.columns(2)
            with col1:
                weight = st.number_input(
                    "Weight (kg):", 
                    min_value=0.0, 
                    step=0.1,
                    help="Enter your weight in kilograms"
                )
            with col2:
                height = st.number_input(
                    "Height (cm):", 
                    min_value=0.0, 
                    step=0.1,
                    help="Enter your height in centimeters"
                )
            
            submitted = st.form_submit_button("Calculate BMI")
            
            if submitted:
                self.process_bmi_calculation(weight, height)
    
    def process_bmi_calculation(self, weight: float, height: float):
        """Handle BMI calculation and record storage"""
        try:
            if weight <= 0 or height <= 0:
                st.warning("Please enter valid weight and height values.")
                return
            
            bmi = self.calculator.calculate(weight, height)
            classification, suggestion = self.calculator.classify(bmi)
            
            # Display results
            st.metric("Your BMI", f"{bmi:.1f}")
            st.write(f"**Classification:** {classification}")
            st.write(f"**Recommendation:** {suggestion}")
            
            # Store record
            record = BMIRecord(
                date=datetime.now().strftime("%Y-%m-%d"),
                weight=weight,
                height=height,
                bmi=bmi,
                classification=classification,
                suggestion=suggestion
            )
            self.repository.add_record(record)
            st.success("BMI measurement saved!")
            
        except ValueError as e:
            st.error(str(e))
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    
    def display_history_section(self):
        """Display the BMI measurement history"""
        st.subheader("Your BMI History")
        df = self.repository.get_all_records()
        
        if df.empty:
            st.info("No BMI measurements recorded yet.")
            return
        
        # Show latest measurement
        latest = df.iloc[-1]
        cols = st.columns(3)
        cols[0].metric("Latest BMI", f"{latest['BMI']:.1f}")
        cols[1].metric("Weight", f"{latest['Weight (kg)']} kg")
        cols[2].metric("Height", f"{latest['Height (cm)']} cm")
        
        # Show full history
        with st.expander("View All Measurements"):
            st.dataframe(df.sort_values("Date", ascending=False))
            
            # Simple trend visualization
            if len(df) > 1:
                st.line_chart(df.set_index("Date")["BMI"])

# Run the application
if __name__ == "__main__":
    app = BMITrackerApp()
