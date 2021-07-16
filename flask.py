from flask import Flask, jsonify
from flask_restful import Resource, Api
import xlrd
import csv, yaml, json, os.path
import pandas as pd

def csv_from_excel_mdt():
    wb = xlrd.open_workbook('Microservice.xlsx')
    sh = wb.sheet_by_name('Microservice')
    your_csv_file = open('microservice.csv', 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))
    your_csv_file.close()
csv_from_excel_mdt()

def csv_from_excel_algodt():
    wb = xlrd.open_workbook('algorithm.xlsx')
    sh = wb.sheet_by_name('Algorithm')
    your_csv_file = open('algorithm.csv', 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))
    your_csv_file.close()
csv_from_excel_algodt()

def csv_from_excel_idt():
    wb = xlrd.open_workbook('infrastructure.xlsx')
    sh = wb.sheet_by_name('Infrastructure')
    your_csv_file = open('infrastructure.csv', 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))
    your_csv_file.close()
csv_from_excel_idt()


app = Flask(__name__)
@app.route('/mdt', methods = ["GET", "POST"])

def mdt():
    file_path ='microservice.csv'
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, encoding='iso-8859-1')
        text = yaml.dump(
        df.reset_index().to_dict(orient='records'),
        sort_keys=False, width=72, indent=4,
        default_flow_style=None, allow_unicode=True)
        return text
 
    else:
        return jsonify({"message":"File not found: Please use a valid file"})

@app.route('/algodt', methods = ["GET", "POST"])

def algodt():
    file_path = 'algorithm.csv'
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, encoding='iso-8859-1')
        text = yaml.dump(
        df.reset_index().to_dict(orient='records'),
        sort_keys=False, width=72, indent=4,
        default_flow_style=None)
        return text
 
    else:
        return jsonify({"message":"File not found: Please use a valid file"})

@app.route('/idt', methods = ["GET", "POST"])

def idt():
    file_path = 'infrastructure.csv'
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, encoding='iso-8859-1')
        text = yaml.dump(
        df.reset_index().to_dict(orient='records'),
        sort_keys=False, width=72, indent=4,
        default_flow_style=None)
        return text
 
    else:
        return jsonify({"message":"File not found: Please use a valid file"})

if __name__ == '__main__':
    app.run(debug=True)
