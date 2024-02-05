# BizCardX: Extracting Business Card Data with OCR

## Overview
BizCardX is a Streamlit application designed to simplify the extraction and management of business card data. It uses easyOCR for information extraction and MySQL as the database system. The application provides three main functionalities: Home, Upload & Extract, and Modify.

## Technologies
- Streamlit
- easyOCR
- MySQL
- PIL (Pillow)
- OpenCV
- Matplotlib
- Pandas
- Regular Expressions

## Setup
1. Install the required packages:
    ```bash
    pip install streamlit easyocr mysql-connector-python pandas opencv-python-headless matplotlib
    ```

2. Clone the repository:
    ```bash
    git clone https://github.com/sugin22/BizCardX--Extracting-Business-Card-Data-with-OCR.git
    cd BizCardX
    ```

3. Run the application:
    ```bash
    streamlit run app.py
    ```

## Features

### Home Option
- Provides a welcome message and guidance on using the application.

### Upload & Extract Option
- Allows users to upload a business card image.
- Utilizes easyOCR to extract relevant information (company name, cardholder name, etc.).
- Displays the extracted data in a clean interface.
- Saves the extracted information and the uploaded image to a MySQL database.
- Supports viewing the updated data from the database.

### Modify Option
- Provides options to alter or delete existing data in the database.
- Users can select a card, modify its details, and commit changes to the database.
- Offers the option to delete a business card entry from the database.

## Project Structure
- `app.py`: Main Streamlit application file.
- `system_path.py`: File containing the path to the home image.
- `streamlit_option_menu.py`: Custom module for creating option menus in Streamlit.
- `uploaded_cards/`: Directory to store uploaded business card images.

## Database Structure
- Table Name: `card_data`
  - Columns: `id`, `company_name`, `card_holder`, `designation`, `mobile_number`, `email`, `website`, `area`, `city`, `state`, `pin_code`, `image` (LONGBLOB)

## Contributors
- Sugin Elankavi Rajendran
