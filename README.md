# BizCardX: Extracting Business Card Data with OCR

## Introduction
BizCardX is a Streamlit application designed for extracting information from business cards. Users can upload images, extract relevant details using easyOCR, and manage the data in a MySQL database. This readme file provides an overview of the project and guides users on setup and functionality.

## Technologies
- Streamlit
- easyOCR
- MySQL
- Python (PIL, cv2, pandas, os, re, matplotlib)

## Getting Started

### Installation
```bash
pip install streamlit easyocr mysql-connector-python pandas opencv-python-headless matplotlib

## Running the Application

streamlit run your_script_name.py

Features
Home Option:

Displays a welcome message and guides users on how to use the application.
Starting easyOCR and Connecting MySQL:

Initializes easyOCR for text extraction from images.
Connects to a MySQL database and creates a table (card_data) to store extracted information and images.
Upload and Extract Option:

Allows users to upload business card images.
Uses easyOCR to extract information.
Displays the processed image and extracted data in a user-friendly GUI.
Enables users to upload extracted data to the database.
Modify Option:

Provides options to alter or delete data in the database.
Allows users to select a card, modify details, and commit changes.
Allows users to delete a selected card's information from the database.
Project Structure
your_script_name.py: Main application script.
system_path.py: Placeholder for home_image path.
image_processing.py: Placeholder for image processing functions.