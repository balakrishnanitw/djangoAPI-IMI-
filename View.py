

# Create your views here.
# -*- coding: utf-8 -*-


# Use this template if you want to create a REST API and support a GET or
# a POST request
# Example for GET: http://hostname:port/endpoint_name?param1=val1&param2=val2
# POST operation can also be made on any of the "exposed" endpoints.

from __future__ import print_function

#import cherrypy
import simplejson as json
import re
from nltk.corpus import stopwords
import numpy as np
import sys
import os
#from django.http import request
from django.http import HttpResponse
import mkl
import platform
from sklearn.externals import joblib
from collections import OrderedDict
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from API.q_scripts.a_class_func_dir import DirStructure, Job, Data

# User Inputs -----------------------------------------------------------------
path_base = os.path.dirname(os.path.dirname(os.path.realpath('__file__'))) 
if platform.system() == 'Linux':
    mkl.set_num_threads(15)
else:
    mkl.set_num_threads(10)

#Load the model data
def unpickle_data():
    cv_n_fold_dl = 0
    # Set Base Path----------------------------------------------------------------
    os.chdir(path_base)
    sys.path.append(path_base)

    
    # Read Config File: -----------------------------------------------------------
    configData = DirStructure('API/config.ini')
    #data = Data(pd_or_np = 'pd', fl_submission_input = None)
    job = Job('ad_truncSVD_randomForest_category_manual/model', cv = cv_n_fold_dl, n_threads = 1, save_model_tf = True)
    path = configData.get_path(configData.model_scoring, job.job_name, 'model.pkl')
    try:
        modelLoad = joblib.load(path)
    except Exception as e:
        modelLoad = 0
        print(str(e))
    return modelLoad 

# call the method for load model    
model = unpickle_data()




def post_process_observation(problem_description, out):
    #columns=['title', 'problem_description', 'status']
    #columns=['Incident', 'Summary', 'Reported By', 'Ticketing source', 'Category']
    #values=[title, problem_description, status]
    #classes = ['code inspection', 'configuration validation', 'design review', 'function test', 'gui review', 'information development review', 'performance scalability', 'requirements review', 'system test', 'unit test'] 
    classes = ['access','accessible','backup failed','backup missed','backup service missing','backups failed','blocking lock','bounds','broken jobs','c drive','cache','citrix issues','connection refused','cpu load','cpu utilization','daily backup report','dead lock','disk critical','disk warning','drives','heart beat','host','host unreachable','inode usage','itm agent offline','jobs failed','live sessions','lockout','login issue','memory usage','output returned','output stdout','pages flushed paged','paging file usage','password issue','permission','plugin time','port','ram critical','ram warning','reboot','respone time','rta','service','service check timed','service running','shutdown','socket timeout','swap usage','take full backup','take full db backup','unexpected exception']
    out1 = np.ndarray.transpose(out)
    out2 = np.ndarray.tolist(out1)

    advisoryDetailsList = []
    #print(out2)
    #print(type(out2))
    #print(type(out2[0]))

    for i in range(len(classes)):

        info = OrderedDict()
        info["Category"] = classes[i]
        info["accuracy"] = out2[i][0]
        
        advisoryDetailsList.append(info)

    #print("\n advisoryDetailsList: ", advisoryDetailsList)
    advisoryDetailsList = sorted(advisoryDetailsList, key=lambda k: k['accuracy'], reverse=True) 
    #print(advisoryDetailsList[len(classes)-4:len(classes)])
    #jsonForm =[json.dumps(advisoryDetailsList[len(classes)-4:len(classes)])]
    #print(advisoryDetailsList[0:4])

    advisoryDict = dict()
    advisoryDict['CategoryRecommendations'] = advisoryDetailsList[0:4]

    output = json.dumps(advisoryDict)
    #print(type(output))
    print("\n output: ", output)
    print("\n")
    return (output)  
def words_data(col):

    clean_text = re.sub("[^a-zA-Z0-9]", " ", col) 
    words = clean_text.lower().split()      
   #remove tester details 
    if(words):
      if(words[0] == 'tester'):
        i=0
        for word in words:
            i=i+1
            if(word == 'description'):
                words = words[i:len(words)-1]
                break
    stops = set(stopwords.words("english"))                  
    meaningful_words = [w for w in words if not w in stops]   
    return( " ".join( meaningful_words ))  
    
def pre_process_observation(load_data_input):
    load_data_input = load_data_input.split()
    clean_data_input = [words_data(doc) for doc in load_data_input]
    return [" ".join(clean_data_input)]
@require_http_methods(["GET", "POST"])        
def predict(request):
        ret = {}
        try:
            summary = vars['ticket_summary']
        except:
            summary = ''
        obs = pre_process_observation(summary)
        try:
            pred_num = model.predict_proba(obs)
        except Exception as e:
            status = {'Error':[{'error_code':'model_prediction_failed'}, {'error_log':str(e)}]}
            ret['status'] = status
            return HttpResponse(json.dumps(ret), content_type="application/json")#json.dumps(ret)
        
        out1= pred_num.round(2)
        out2 = (100*out1).astype(float)
        formatted_output = post_process_observation(obs, out2)
        
        return HttpResponse(json.dumps(formatted_output), content_type="application/json")

