import random
from flask import Flask, render_template, url_for, escape, request, redirect, session
import os
import pandas as pd
import numpy as np
import csv
import math
from sklearn import neighbors, datasets
from numpy.random import permutation
from sklearn.metrics import precision_recall_fscore_support
import UnderGraduateServer

app = Flask(__name__, static_folder='../static/dist/', template_folder='../static')
app.secret_key = os.urandom(24)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/graduate')
def graduate():
    return render_template('graduate.html')


@app.route("/main")
def return_main():
    return render_template('index.html')


@app.route('/undergraduate')
def undergraduate():
    return render_template('undergraduate.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return index()
    else:
        return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'susmita' or request.form['password'] != '1234':
            error = 'Invalid Username/Password.'
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            return return_main()
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    # Removing data from session by setting logged_flag to False.
    session['logged_in'] = False
    session['username'] = ''
    # redirecting to home page
    return index()


def euclidean_dist(test, train, length):
    distance = 0
    for x in range(length):
        distance += np.square(test[x] - train[x])
    return np.sqrt(distance)


def knn(trainSet, test_instance, k):
    distances = {}
    sort = {}
    length = test_instance.shape[1]

    for x in range(len(trainSet)):
        distance = euclidean_dist(test_instance, trainSet.iloc[x], length)
        distances[x] = distance[0]

    sorted_distances = sorted(distances.items(), key=lambda x: x[1])
    print(sorted_distances[:5])

    neighbors_list = []

    for x in range(k):
        neighbors_list.append(sorted_distances[x][0])

    duplicateNeighbors = {}

    for x in range(len(neighbors_list)):
        responses = trainSet.iloc[neighbors_list[x]][-1]

        if responses in duplicateNeighbors:
            duplicateNeighbors[responses] += 1
        else:
            duplicateNeighbors[responses] = 1
    print(responses)

    sortedNeighbors = sorted(duplicateNeighbors.items(), key=lambda x: x[1], reverse=True)
    return (sortedNeighbors, neighbors_list)


@app.route('/undergraduatealgo')
def undergraduatealgo():
    result = UnderGraduateServer.main()
    format_result = {}
    list1 = []
    list2 = []
    for i in result:
        list1.append(i[0])
    for i in result:
        list2.append(i[1])

    format_result[list1[0]] = list2[0]
    format_result[list1[1]] = list2[1]
    format_result[list1[2]] = list2[2]
    format_result[list1[3]] = list2[3]
    format_result[list1[4]] = list2[4]

    print('format data = ', format_result)
    return render_template("undergrade_search_result.html", result=format_result)


@app.route('/graduatealgo')
def graduatealgo():
    data = pd.read_csv('../WebScraped_data/csv/Processed_data.csv')
    data.drop(data.columns[data.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
    greV = float(request.args.get("greV"))
    greQ = float(request.args.get("greQ"))
    greA = float(request.args.get("greA"))
    cgpa = float(request.args.get("cgpa"))
    testSet = [[greV, greQ, greA, cgpa]]
    test = pd.DataFrame(testSet)
    k = 7
    result, neigh = knn(data, test, k)
    list1 = []
    list2 = []
    for i in result:
        list1.append(i[0])
    for i in result:
        list2.append(i[1])
    format_result = {}
    j = 0
    for i in list1:
        j = j+1
        format_result[j] = i
    return render_template("graduate_search_result.html", result=format_result)


if __name__ == '__main__':
    app.run()
