import pandas as pd
from flask import Flask, jsonify
from flask_restful import Resource, Api
import json, validators, urllib.request, os.path, excel2json

app = Flask(__name__)
@app.route('/api/v1/mdt/compile', methods = ["GET", "POST"])

def mdt():
    file_path = 'microservice.xlsx'
    if os.path.exists(file_path):
        if file_path.endswith('.txt'):
            with open(file_path,  encoding='utf-8', errors='ignore') as j:        

                lines = j.readlines()
                lines = [line.replace('\t', '') for line in lines]
            
                for url in lines: 
                    if validators.url(url):
                        response = urllib.request.urlopen(url)
                        data = json.loads(response.read())
                        return data
                    else:
                        return json.dumps(lines, indent= True)
        
        else:
            excel2json.convert_from_file(file_path)
            xls = pd.ExcelFile(file_path)
            df1 = pd.read_excel(xls)
            return df1.to_json()
            
                    
    else:
        return jsonify({"message":"File not found: Please use a valid file"})

@app.route('/api/v1/algodt/compile', methods = ["GET", "POST"])

def algodt():
    file_path = 'algorithm.xlsx'
    if os.path.exists(file_path):
        if file_path.endswith('.txt'):
            with open(file_path,  encoding='utf-8', errors='ignore') as j:        

                lines = j.readlines()
                lines = [line.replace('\t', '') for line in lines]
            
                for url in lines: 
                    if validators.url(url):
                        response = urllib.request.urlopen(url)
                        data = json.loads(response.read())
                        return data
                    else:
                        return json.dumps(lines, indent= True)
        
        else:
            excel2json.convert_from_file(file_path)
            xls = pd.ExcelFile(file_path)
            df1 = pd.read_excel(xls)
            return df1.to_json()
            
                    
    else:
        return jsonify({"message":"File not found: Please use a valid file"})

@app.route('/api/v1/idt/compile', methods = ["GET", "POST"])

def idt():
    file_path = 'infrastructure.xlsx'
    if os.path.exists(file_path):
        if file_path.endswith('.txt'):
            with open(file_path,  encoding='utf-8', errors='ignore') as j:        

                lines = j.readlines()
                lines = [line.replace('\t', '') for line in lines]
            
                for url in lines: 
                    if validators.url(url):
                        response = urllib.request.urlopen(url)
                        data = json.loads(response.read())
                        return data
                    else:
                        return json.dumps(lines, indent= True)
        
        else:
            excel2json.convert_from_file(file_path)
            xls = pd.ExcelFile(file_path)
            df1 = pd.read_excel(xls)
            return df1.to_json()
            
                    
    else:
        return jsonify({"message":"File not found: Please use a valid file"})

if __name__ == '__main__':
    app.run(debug=True)







