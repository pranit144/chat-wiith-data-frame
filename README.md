# Student Data Visualization Web App

This project is a Flask-based web application that allows users to upload CSV files containing student data and visualize insights through various plots and statistical summaries.

## Features
- Upload CSV files containing student data.
- Generate statistical summaries (numerical and categorical).
- Identify missing values in the dataset.
- Generate various visualizations:
  - Line plots (Overall Trend, Trend by Branch)
  - Bar plots (Students by Branch, Students by Category)
  - Stacked bar plot (Students by Year and Gender)
  - Pie chart (Proportion by Branch)
  - Boxplot (Students by Branch)
  - Heatmap (Correlation between numerical variables)
  - Violin plot (Students by Gender)
  - Area chart (Cumulative Students by Year)
  - Treemap (Students by Branch)
- Display insights derived from the visualizations.

## Installation

### Prerequisites
Ensure you have Python installed (preferably Python 3.7+).

### Clone the Repository
```bash
https://github.com/your-username/student-data-visualization.git
cd student-data-visualization
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Run the Flask App
```bash
python app.py
```

### Access the Web App
Once the server is running, open a browser and go to:
```
http://127.0.0.1:5000/
```

### Uploading Data
1. Click on the "Upload File" button and select a CSV file containing student data.
2. The application will process the file and display various insights and visualizations.

## Data Format
The uploaded CSV should contain the following columns:
- `Year` (integer): Represents the academic year.
- `Number_of_Students` (integer): Count of students.
- `Branch` (string): Branch of study.
- `Category` (string): Student category.
- `Gender` (string): Male/Female.

Example:
```csv
Year,Number_of_Students,Branch,Category,Gender
2020,50,Computer Science,General,Male
2020,40,Mechanical,OBC,Female
...
```

## Dependencies
- Flask
- Pandas
- Matplotlib
- Seaborn
- Squarify (for treemap visualization)

Install dependencies using:
```bash
pip install flask pandas matplotlib seaborn squarify
```

## License
This project is licensed under the MIT License.

## Author
- Your Name
- Your Contact (GitHub, Email, etc.)

