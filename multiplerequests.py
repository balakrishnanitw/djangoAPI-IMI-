import time
import requests
url = "http://localhost:8000/predict" 
params = {}
params1 = {}
list = []
params['Summary'] = "Daily reboot of LSEvent & Worklight servers"
list.append(params)
#list.append(params)

params1['Summary'] = "Backup Failures on || Newcrest ||"
list.append(params1)
#
#params['Summary'] = "Backup Failures on || Newcrest ||"
#list.append(params)
#
#params['Summary'] = "Backup Failures on || Newcrest ||"
#list.append(params)
start = time.time()
for i in range(len(list)):
    res = requests.post(url,data=params)
    #print(res.content)
responsetime = time.time() - start

print (responsetime)
