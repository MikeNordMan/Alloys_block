from requests import get
from requests import post
from urls import urls



def requestsKod():
    url ='http://127.0.0.1:5000/alloys/'
    kod =['find']
    keysForServer = ['kod', 'nameAlloy']
    keys = ['nameAlloy', 'discript', 'tu_Gost']
    d = {'kod': 'del', 'nameAlloy': 'TRT'}
    data = {'nameAlloy': 'FDDF', 'kod': 'update'}
    r = post(url, data)
    message = r.json()
    resMessage = message['numRecord']
    print(resMessage)
requestsKod()