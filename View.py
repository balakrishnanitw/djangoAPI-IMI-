import os
import mkl
import platform
from sklearn.externals import joblib
from collections import OrderedDict
from django.views.generic import RedirectView


def unpickle_data():
    modelLoad = joblib.load('Trainedmodel.pkl')
    return modelLoad 
model = unpickle_data()    


def post1(self,**vars):#,problem_description, out):
    classes = ['access','accessible','backup failed','backup missed','backup service missing','backups failed','blocking lock','bounds','broken jobs','c drive','cache','citrix issues','connection refused','cpu load','cpu utilization','daily backup report','dead lock','disk critical','disk warning','drives','heart beat','host','host unreachable','inode usage','itm agent offline','jobs failed','live sessions','lockout','login issue','memory usage','output returned','output stdout','pages flushed paged','paging file usage','password issue','permission','plugin time','port','ram critical','ram warning','reboot','respone time','rta','service','service check timed','service running','shutdown','socket timeout','swap usage','take full backup','take full db backup','unexpected exception']
    out=np.ndarray(shape=(len(classes),len(classes)))
    out1 = np.ndarray.transpose(out)
    out2 = np.ndarray.tolist(out1)
    
    advisoryDetailsList = []
    
    for i in range(len(classes)):    
        info = OrderedDict()
        info["Category"] = classes[i]
        info["accuracy"] = out2[i][0]            
        advisoryDetailsList.append(info)
    
    advisoryDetailsList = sorted(advisoryDetailsList, key=lambda k: k['accuracy'], reverse=True) 
    
    advisoryDict = dict()
    advisoryDict['CategoryRecommendations'] = advisoryDetailsList[0:4]
    
#        output = json.dumps(advisoryDict)
#        print("\n output: ", output)
#        print("\n")
    return  HttpResponse(json.dumps(advisoryDict), content_type="application/json")



def predict(self, **vars):
        #ret = {}
#        try:
        #summary = vars['ticket_summary']
#        except:
#            summary = ''
        #obs = self.pre_process_observation(summary)
#        try:
        #pred_num = model.predict_proba(obs)
#        except Exception as e:
        
        ret = {}
        status = {'Error':[{'error_code':'model_prediction_failed'}, ]}#{'error_log':str(e)}]}
        ret['status'] = status
        return HttpResponse(json.dumps(ret), content_type="application/json")
