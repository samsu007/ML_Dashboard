# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 21:13:17 2020

@author: samsu
"""


# %%
from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import csv
import warnings
warnings.filterwarnings('ignore')
app = Flask(__name__)


def transform(text_file_contents):
    return text_file_contents.replace("=", ",")


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/", methods=['POST'])
def start():
    f = request.files['data_file']
    if request.form['rows'] == "":
        dat = 5
    else:
        dat = int(request.form['rows'])
    
    if not f:
        return "No file"
    data = pd.read_csv(f)
    # print(data.head())
    tableHead = []
    tableData = []
    for index, row in data.head(n=1).iterrows():
        datas = []
        for i, value in row.items():
            datas.append(i)
        tableHead.append(datas)

    for index, row in data.head(dat).iterrows():
        datas = []
        for i, value in row.items():
            datas.append(value)
        tableData.append(datas)

    descriptive_data = []
    descriptive_head = []
    for index, row in data.describe().transpose().iterrows():
        datas = []
        datas.append("")
        for i, value in row.items():
            datas.append(i)
        descriptive_head.append(datas)

    for index, row in data.describe().transpose().iterrows():
        datas = []
        datas.append(index)
        for i, value in row.items():
            datas.append(value)
        descriptive_data.append(datas)

    corr_data = []
    corr_head = []
    for index, row in data.corr().iterrows():
        datas = []
        datas.append("")
        for i, value in row.items():
            datas.append(i)
        corr_head.append(datas)

    for index, row in data.corr().iterrows():
        datas = []
        datas.append(index)
        for i, value in row.items():
            datas.append(value)
        corr_data.append(datas)

    # columns = []
    # datatypes = []
    # count = []

    # for row in data.columns:
    #     columns.append(row)
    
    # for row in data.dtypes:
    #     datatypes.append(row)

    # for row in data.count():
    #     count.append(row)

    info_head = []
    info_head.append(["Columns","dtypes","count"])
    info_data = []

    for i in data.columns: 
        info_data.append([i,data.dtypes[i],data.count()[i]])


    missing_value = []
    for i,v in data.isnull().sum().items():
        missing_value.append([i,v])

    # print(missing_value)
    return render_template("index.html",
                           tables=tableHead,
                           tableData=tableData,
                           info_head=info_head,  
                           info_data=info_data,  
                           shape=data.shape,
                           missing_value=missing_value,
                           descriptive_data=descriptive_data,
                           descriptive_head=descriptive_head[0], 
                           corr_head=corr_head[0], 
                           corr_data=corr_data)
