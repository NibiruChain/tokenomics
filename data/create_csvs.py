from typing import List
import xlsx
import csv
import os

def csv_from_excel():
    excel_file_paths: List[str] = [f for f in os.listdir() if ("xlsx" in f)]
    workbook = xlsx.Workbook(excel_file_paths[0])
    sheet: xlsx.Sheet = [sheet for sheet in workbook 
                         if ("token_distribution" in sheet.name)][0]
        
    with open('token_distribution.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        for row_num, cells in sheet.rows().items():
            writer.writerow([c.value for c in cells])

# runs the csv_from_excel function:

if __name__ == "__main__":
    csv_from_excel()