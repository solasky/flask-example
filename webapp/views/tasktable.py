# Copyright (C) 2019 MyRepublic Group Ltd qianqian.zhang@myrepublic.net
# DO NOT REDISTRIBUTE
import os
import flask
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from webapp import app
from webapp.models.models import ContentClassificationTask
from webapp.database import DataTablesServer

# JSON (data type application/json)
@app.route('/tasks/', methods=('GET', 'POST'))
def get_tasks():
    # get table columns
    columns = ContentClassificationTask.__table__.columns.keys()
    
    # defind index column
    index_column = "index"
    
    # init DataTableServer and get result
    results = DataTablesServer(request, columns, index_column, ContentClassificationTask).output_result()

    # return the results as a string for the datatable
    return flask.jsonify(results)
