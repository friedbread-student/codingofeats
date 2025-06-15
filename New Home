#########################################
#                                       #
##           EatS: HOMEPAGE            ##
#                                       #
#########################################
import streamlit as st
from pathlib import Path

# Set page config with improved metadata
st.set_page_config(
    page_title="EatS Health Tracker",
    page_icon="🏋️",
    layout="centered",
    menu_items={
        'About': "EatS - A comprehensive health tracking system by CvSU Computer Engineering students"
    }
)

# Get the base directory path
BASE_DIR = Path(__file__).parent

# Define page configurations with absolute paths
pages = {
    "Information": [
        {
            "title": "About Us", 
            "icon": "👥",
            "path": BASE_DIR / "aboutus.py",
            "default": True
        }
    ],
    "Services": [
        {
            "title": "Food Tracker",
            "icon": "🍽️",
            "path": BASE_DIR / "food" / "food.py"
        },
        {
            "title": "Sleep Tracker",
            "icon": "😴", 
            "path": BASE_DIR / "sleep" / "app.py"
        },
        {
            "title": "BMI Tracker",
            "icon": "⚖️",
            "path": BASE_DIR / "bmi.py"
        }
    ]
}

def main():
    """Main application entry point"""
    st.title("EatS Health Tracker")
    st.subheader("Your comprehensive health and wellness companion")
    
    # Display welcome message
    st.markdown("""
    <div style="background-color:#f0f2f6;padding:20px;border-radius:10px;margin-bottom:20px;">
        <p style="font-size:18px;">
        Welcome to EatS! Track your nutrition, sleep patterns, and body metrics all in one place.
        Select a service below to get started on your health journey.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create navigation sections
    for section, page_configs in pages.items():
        st.markdown(f"### {section}")
        
        cols = st.columns(len(page_configs))
        for idx, config in enumerate(page_configs):
            with cols[idx]:
                # Verify page exists before creating link
                if config["path"].exists():
                    st.page_link(
                        str(config["path"]),
                        label=config["title"],
                        icon=config["icon"],
                        help=f"Go to {config['title']}"
                    )
                else:
                    st.error(f"Page not found: {config['path']}")
        
        st.markdown("---")
    
    # Display footer
    st.markdown("""
    <div style="text-align:center;margin-top:30px;">
        <small>Developed by CvSU Computer Engineering Students</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
