import json
from Core.l2.json.second import setJsonAcc
import tkinter as tk
class JsonGenerator:
    data = ''
    def __init__(self,config,consol):
        self.consol = consol
        self.read_wallets()
        self.generate(config)

    def read_wallets(self,file='wallets.txt'):
        try:

            with open(file) as f:
                data = f.readlines()
            if len(data) == 0:
                self.consol.insert(tk.END,'Wallets.txt is empty\n')
                # raise Exception('Wallets.txt is empty')
            for i,v in enumerate(data):
                data[i] = v.replace('\n','')
            self.data = data
        except:
            self.consol.insert(tk.END, 'Can not open wallets.txt\n')

    def generate(self,configuration:setJsonAcc,papka='Accs'):
        for i in self.data:
            data = json.loads(configuration.setInfo(i))
            if data != 'ERROR':
                with open(f"{papka}/{data['address']}.json",'w') as file:
                    json.dump(data,file)

