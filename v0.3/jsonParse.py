import json
with open('temp.json','r',encoding='utf-8') as f:
    a=json.loads(f.read())
    print(a)