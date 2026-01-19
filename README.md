# Sales Analytics System

**Student Name:** A Praneeth      
**Student ID:** bitsom_ba_25071345      
**Email:** praneethpark@gmail.com    
**Date:** 19/01/2026

## Project Overview
This project implements a Sales Analytics System using Python.  
It reads sales data from a file, cleans and validates transactions, performs analytical computations, integrates product data from an external API, enriches transactions, and generates a detailed sales report.

---

## 📁 Repository Structure
sales-analytics-system/
├── main.py    
├── README.md     
├── requirements.txt    
├── data/      
│ ├── sales_data.txt    
│ └── enriched_sales_data.txt    
├── output/    
│ └── sales_report.txt     
├── utils/     
│ ├── file_handler.py      
│ ├── data_processor.py    
│ └── api_handler.py    


---

## ⚙️ Setup Instructions

1. **Download the project**
   - Open the GitHub repository
   - Click **Code → Download ZIP**
   - Extract the ZIP file to your system

2. **Open the project folder**
   - Navigate into the extracted `sales-analytics-system` folder

3. **Create a virtual environment (optional but recommended)**

```
python -m venv .venv
.venv\Scripts\activate
```

4. **Install required dependencies**
```
pip install -r requirements.txt
```

## ▶️ Run Instructions
```
Execute the main script with command:
python main.py
```

## 📄 Outputs Generated
- **Enriched Sales Data:** data/enriched_sales_data.txt
- **Sales Report:** output/sales_report.txt

## 🧪 Technologies Used

- Python 3
- Requests library
- DummyJSON API
