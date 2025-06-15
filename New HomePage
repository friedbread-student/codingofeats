############################################
#                                          #
##      EatS: About Page (Home Page)      ##
#                                          #
############################################
import streamlit as st
import random
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class AppLink:
    """Represents a navigation link to another app page"""
    label: str
    path: str
    icon: str

class MotivationalQuoteGenerator:
    """Handles motivational quote selection and display"""
    def __init__(self):
        self.quotes = [
            "Matulog ka nang maaga, 'wag ka magpupuyat magagalit ako >:(",
            "How was your day? Kaya pa?... Kaya 'yan!",
            "Uy nakita ko food intake mo. Kumain ka nang mabuti ha",
            # ... (include all your quotes here)
            "Fuel your body, nourish your soul, embrace health, find balance.",
            "Are you hungry right now? How about we cook a very healthy meal while I hug you from the back :3",
            "Dinner at olive garden? I'll pick you up by 8pm <33"
        ]
    
    def get_random_quote(self) -> str:
        """Returns a random motivational quote"""
        return random.choice(self.quotes)

class AboutPage:
    """Main class for the About/Home page"""
    def __init__(self):
        self.quote_generator = MotivationalQuoteGenerator()
        self.app_links = [
            AppLink("Sleep Tracker", "sleep/app.py", "⏰"),
            AppLink("Food Tracker", "food/food.py", "🍽️"),
            AppLink("BMI Tracker", "bmi.py", "⚖️"),
            AppLink("Health Dashboard", "dashboard.py", "📊")
        ]
        self.setup_page()
    
    def setup_page(self) -> None:
        """Configures the page layout and content"""
        st.set_page_config(
            page_title="EatS - Health Tracker",
            page_icon="❤️",
            layout="centered"
        )
        self.display_header()
        self.display_navigation()
        self.display_quote()
    
    def display_header(self) -> None:
        """Displays the page header and description"""
        st.title("🍎 EatS: Tracking Your Health Journey")
        st.header("Welcome to Your Personal Health Companion")
        
        st.markdown("""
        <div style="background-color:#f0f2f6;padding:20px;border-radius:10px;">
            <p style="font-size:18px;">
            EatS is a health tracking application created by first year Computer Engineering Students 
            from Cavite State University. Our mission is to help you improve your health and fitness 
            through better sleep, nutrition, and body awareness.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
    
    def display_navigation(self) -> None:
        """Displays navigation cards to other pages"""
        st.subheader("Explore Our Trackers")
        
        cols = st.columns(len(self.app_links))
        for idx, link in enumerate(self.app_links):
            with cols[idx]:
                st.page_link(
                    link.path, 
                    label=link.label, 
                    icon=link.icon,
                    help=f"Go to {link.label}"
                )
        
        st.markdown("---")
    
    def display_quote(self) -> None:
        """Displays a random motivational quote"""
        quote = self.quote_generator.get_random_quote()
        
        st.markdown(f"""
        <div style="background-color:#e6f7ff;padding:20px;border-radius:10px;border-left:5px solid #1890ff">
            <p style="font-style:italic;font-size:18px;">"{quote}"</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align:center;margin-top:20px;">
            <small>Refresh the page for a new motivational message!</small>
        </div>
        """, unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    AboutPage()
