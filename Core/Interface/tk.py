import os
import tkinter as tk
from tkinter.ttk import Frame, Label, Style
from tkinter import ttk
import time
import json
from Core.l2.SyncSwapL2 import SyncAccManager
from Core.l2.json.first import JsonGenerator
from Core.l2.json.second import setJsonAcc
import threading
from Core.l0.Account.Status import check_if_ready

class Testing:
    gg = False
    # timewas = time.time() - 5
    final_message = ''
    returnData = {'space': False, 'eralend': False, 'reactor': False, 'domain': False}
    flag_start = 0
    width = 0
    height = 0
    # timewas = 0
    responce = {}
    btnstarted = False

    def __init__(self):
        self.timewas = time.time() -5
        self.getPer()
        self.build_logic()
        self.place()
        self.bind_func()
        self.cheking_thread()
        self.mainloop()

    def getPer(self):
        root = tk.Tk()
        self.width = int(root.winfo_screenwidth() / 3)
        self.height = int(root.winfo_screenheight() / 2)
        self.Wwidth = root.winfo_screenwidth()
        self.Wheight = root.winfo_screenheight()
        # self.perX = int(root.winfo_screenwidth()/100)
        # self.perY = int(root.winfo_screenheight()/100)
        root.destroy()

    def pX(self, p):
        return int((self.width / 100) * p)

    def pY(self, p):
        return int((self.height / 100) * p)

    def build_logic(self):
        self.root = tk.Tk()
        self.root.title("ZkSync by @SwissScripts")
        self.root.geometry(f"{int(self.Wwidth / 1.25)}x{int(self.Wheight / 2.37)}")

        self.zkSync = ttk.Label(self.root, text='ZkSync by @SwissScripts', font=("Arial", int(self.pY(15) * 0.45)))
        self.zkSync.configure(background="#f5b0b0")

        textk = 0.3

        self.swaps_lab = ttk.Label(self.root, text='swaps туда и обратно', font=("Arial", int(self.pY(15) * textk)),
                                   anchor="center")
        self.swaps_lab.configure(background="#dea9c6")
        self.swaps_enter = ttk.Entry(self.root, font=("Arial", int(self.pY(15) * textk)))
        self.swaps_price = ttk.Label(self.root, text='', font=("Arial", int(self.pY(15) * textk)), anchor="center")
        self.swaps_price.configure(background="#dea9e6")

        self.vol_lab = ttk.Label(self.root, text='vol usd', font=("Arial", int(self.pY(15) * textk)), anchor="center")
        self.vol_lab.configure(background="#b0e7f5")
        self.vol_enter = ttk.Entry(self.root, font=("Arial", int(self.pY(15) * 0.25)))
        self.vol_price = ttk.Label(self.root, font=("Arial", int(self.pY(15) * textk)), anchor="center")
        self.vol_price.configure(background="#c2c6f2")

        self.gas_lab = ttk.Label(self.root, text='gas per swap usd', font=("Arial", int(self.pY(15) * textk)),
                                 anchor="center")
        self.gas_lab.configure(background="#dea9c6")
        self.gas_enter = ttk.Entry(self.root, font=("Arial", int(self.pY(15) * 0.25)))
        self.gas_price = ttk.Label(self.root, text='', font=("Arial", int(self.pY(15) * textk)), anchor="center")
        self.gas_price.configure(background="#dea9e6")

        self.time_lab = ttk.Label(self.root, text='time in hours', font=("Arial", int(self.pY(15) * textk)),
                                  anchor="center")
        self.time_lab.configure(background="#b0e7f5")
        self.time_enter = ttk.Entry(self.root, font=("Arial", int(self.pY(15) * textk)))
        self.time_price = ttk.Label(self.root, font=("Arial", int(self.pY(15) * textk)), anchor="center")
        self.time_price.configure(background="#c2c6f2")
        # self.space_price.place(x=self.pX(83), y=self.pY(17), width=self.pX(17), height=self.pY(15))

        style = ttk.Style()
        style.configure("Custom.TButton", font=("Arial", int(self.pY(15) * 0.26)))
        self.buton_gg = ttk.Button(self.root, text='check & start', style="Custom.TButton")
        # self.buton_gg.configure(background="#c2f2e2")
        self.button_label = ttk.Label(self.root, font=("Arial", int(self.pY(15) * 0.2)))
        self.button_label.configure(background="#f59d9d")
        self.okno = tk.Text(self.root, height=10, width=40)

        # self.okno = ttk.Scrollbar(command=text_widget.yview)

    def place(self):
        height = 11
        self.zkSync.place(x=0, y=0, width=self.pX(87), height=self.pY(15))

        wxpos = 55
        wxpos1 = 10
        wxpos3 = 18
        xpos1 = wxpos + 2
        xpos2 = xpos1 + wxpos1 + 2

        posy4 = 17
        self.swaps_lab.place(x=self.pX(0), y=self.pY(posy4), width=self.pX(wxpos), height=self.pY(height))
        self.swaps_enter.place(x=self.pX(xpos1), y=self.pY(posy4), width=self.pX(wxpos1), height=self.pY(height))
        self.swaps_price.place(x=self.pX(xpos2), y=self.pY(posy4), width=self.pX(wxpos3), height=self.pY(height))

        posy3 = 30
        self.vol_lab.place(x=0, y=self.pY(posy3), width=self.pX(wxpos), height=self.pY(height))
        self.vol_enter.place(x=self.pX(xpos1), y=self.pY(posy3), width=self.pX(wxpos1), height=self.pY(height))
        self.vol_price.place(x=self.pX(xpos2), y=self.pY(posy3), width=self.pX(wxpos3), height=self.pY(height))

        posy = 43
        self.gas_lab.place(x=self.pX(0), y=self.pY(posy), width=self.pX(wxpos), height=self.pY(height))
        self.gas_enter.place(x=self.pX(xpos1), y=self.pY(posy), width=self.pX(wxpos1), height=self.pY(height))
        self.gas_price.place(x=self.pX(xpos2), y=self.pY(posy), width=self.pX(wxpos3), height=self.pY(height))

        posy1 = 56
        self.time_lab.place(x=0, y=self.pY(posy1), width=self.pX(wxpos), height=self.pY(height))
        self.time_enter.place(x=self.pX(xpos1), y=self.pY(posy1), width=self.pX(wxpos1), height=self.pY(height))
        self.time_price.place(x=self.pX(xpos2), y=self.pY(posy1), width=self.pX(wxpos3), height=self.pY(height))

        self.okno.place(x=self.pX(89), y=self.pY(0), width=self.pX(150), height=self.pY(84))

        posy2 = 69
        wb = 30
        self.buton_gg.place(x=0, y=self.pY(posy2), width=self.pX(wb), height=self.pY(15))
        self.button_label.place(x=self.pX(wb + 2), y=self.pY(posy2), width=self.pX(55), height=self.pY(15))

    def mainloop(self):
        self.root.mainloop()

    # def sign_events(self):

    #     def show_space(event):
    #         self.space_price['text'] = str(float(self.space_swaps.get()) * 0.5) + ' $'

    #     self.space_swaps.bind("<Key>", show_space)

    #     def show_vol(event):
    #         if int(self.space_volume_enter.get())<0:
    #             self.space_volume_price['text'] = '<0'
    #         if int(self.space_volume_enter.get())<95:
    #             self.space_volume_price['text'] = 'Good'
    #         # self.space_volume_price['text'] = str(float(self.space_volume_enter.get()) * 0.5)
    #     def try_int(val):
    #         try:
    #             int(val)
    #             if int(val)>0:
    #                 return True
    #             else:
    #                 return False
    #         except:
    #             return False

    #     def get_total(event):
    #         if (time.time() - self.timewas) > 5:
    #             toDo = True
    #             self.timewas = time.time()
    #             if self.space_swaps.get() != '' and try_int(self.space_swaps.get()):
    #                 message = 'Got Swaps'
    #             else:
    #                 message = 'Swaps Error: must be int>=1'
    #                 toDo = False

    #             if self.space_volume_enter.get() != '' and try_int(self.space_volume_enter.get()):
    #                 if int(self.space_volume_enter.get())>0:
    #                     message = message + '\nGot volume'
    #                 else:
    #                     message = message + '\nSwaps ERROR'
    #                     toDo = False

    #             else:
    #                 message = message + '\nVolume Error'
    #                 toDo = False
    #             if toDo:
    #                 self.button_label['text'] = message + '\nPress again to start'
    #             else:
    #                 self.button_label['text'] = message

    #         elif (time.time() - self.timewas) < 5:

    #             toDo = True
    #             self.timewas = time.time()
    #             if self.space_swaps.get() != '' and try_int(self.space_swaps.get()):
    #                 message = 'Got Swaps'
    #             else:
    #                 message = 'Swaps Error: must be int>=1'
    #                 toDo = False

    #             if self.space_volume_enter.get() != '' and try_int(self.space_volume_enter.get()):
    #                 if int(self.space_volume_enter.get())>0:
    #                     message = message + '\nGot Volume'
    #                 else:
    #                     message = message + '\nLess then 0'
    #                     toDo = False

    #             else:
    #                 message = message + '\nVolume Error'
    #                 toDo = False
    #             if toDo:
    #                 self.button_label['text'] = 'starting script...'
    #                 self.form_responce(int(self.space_volume_enter.get()),int(self.space_swaps.get()))
    #     self.space_volume_enter.bind("<Key>", show_vol)
    #     self.buton_gg.bind("<Button-1>", get_total)

    def form_responce(self,volume,swaps,gas,timep):
        self.responce = {"swaps":swaps,"volume":volume,"tx_costs":gas,"time":timep}

        data = str(self.responce)
        data = str(self.responce).replace('\'', '\"')
        # data = json.loads(data)
        with open('Accs/settings.json','w') as file:
            file.write(data)
        # time.sleep(3)
        # self.root.quit()
        # self.root.quit()
        # return self.responce

    #     # def show_eralend(event):
    #     #     self.space_volume_price['text'] = str(float(self.space_volume_enter.get()) * 0.275 + 0.6)
    #     #
    #     # self.eralend_volume.bind("<Key>", show_eralend)

    def cheking_thread(self):
        got_gas = False
        swaps = 0

        def try_int(val):
            try:
                int(val)
                if int(val) <= 0:
                    return False
                return True
            except:
                return False

        def try_float(val):
            try:
                float(val)
                if float(val) <= 0:
                    return False
                return True
            except:
                return False

        def write_check():
            swaps = 0
            got_gas = False
            self.gg = True
            # swaps_enter
            if try_int(self.swaps_enter.get()) and int(self.swaps_enter.get()) <= 999:
                # self.swaps_price['text'] = 'Good'
                swaps = int(self.swaps_enter.get())
                self.swaps_price['text'] = 'Good'
            else:
                self.gg = False
                self.swaps_price['text'] = 'Error'

            if try_float(self.vol_enter.get()):
                self.vol_price['text'] = 'Good'
            else:
                self.gg = False
                self.vol_price['text'] = 'Error'

            if try_float(self.gas_enter.get()):
                self.gas_price['text'] = 'Good'
                gas = float(self.gas_enter.get())
                got_gas = True
            else:
                self.gas_price['text'] = 'Error'
                self.gg = False

            if try_float(self.time_enter.get()):
                self.time_price['text'] = 'Good'
            else:
                self.time_price['text'] = 'Error'
                self.gg = False
            if bool(swaps) and got_gas:
                self.swaps_price['text'] = str(round(gas * swaps * 2 * 0.8, 2)) + '$'
                #     # str(float(self.gas_enter.get())*0.8*float(self.swaps_enter.get()))
            if self.button_label['text'] == 'Press in 5 secs to start' and time.time() - self.timewas > 5:
                self.button_label['text'] = ''
            if self.button_label['text'] == 'Press in 5 secs if files are prepared' and time.time() - self.timewas > 5:
                self.button_label['text'] = ''
        def print_info():
            while True:
                time.sleep(1)
                write_check()
                # if bool(swaps):
                #     self.swaps_price['text'] = 'huy'
                #     # str(float(self.gas_enter.get())*0.8*float(self.swaps_enter.get()))

        proc = threading.Thread(target=print_info)
        proc.start()

    # def sign_events(self):
    #     def starting_backs():
    #         if self.gg:
    def bind_func(self):
        self.buton_gg.bind("<Button-1>", self.button_ggs)
    def checker_after_json_before_start(self):
        message = ''
        how_many_ready = 0
        how_many_null = 0
        how_many_can = 0
        wall_list = []
        wallet_list = os.listdir('Accs')

        for i,v in enumerate(wallet_list):
            if v == 'settings.json':
                wallet_list.pop(i)

        if len(wallet_list) != 0:
            for i in wallet_list:
                try:
                    with open(f'Accs/{i}') as file:
                        wall_list.append(json.load(file))
                except:
                    message = message + f'{i} reading error\n'
            for i in wall_list:
                address = i['address']
                volume = i['modules']['syncSwap']['volume']
                tx_costs = i['modules']['syncSwap']['tx_costs']
                tx_how_many = i['modules']['syncSwap']['swaps']
                b,h = check_if_ready(address,volume,tx_costs,tx_how_many)
                message = message + f'{address} enough: {b} how many: {round(h,2)}\n'

                if b==False and h==0:
                    how_many_null = how_many_null + 1

                if b==False and h>1:
                    how_many_can = how_many_can + 1

                if b==True:
                    how_many_ready = how_many_ready + 1

            message = message + f'ready: {how_many_ready}\ncan: {how_many_can}\nnull: {how_many_null}\n'
        self.okno.insert(tk.END,message)

    def button_ggs(self,event):

        def th1():
            self.timewas = time.time()
            self.button_label['text'] = 'Press in 5 secs if files are prepared'
            if self.gg == True:
                volume = float(self.vol_enter.get())
                swaps = int(self.swaps_enter.get())
                gas = float(self.gas_enter.get())
                timep = float(self.time_enter.get())
                self.form_responce(volume,swaps,gas,timep)
                d = setJsonAcc()
                d.syncSwap()
                JsonGenerator(d,self.okno)
                self.timewas = time.time()
                self.checker_after_json_before_start()
                self.button_label['text'] = 'Press in 5 secs to start'
                # time.sleep(5)
                # self.btnstarted = False



        if time.time() - self.timewas < 5:
            print('huy')
            def start_tasks():
                list_wallets = os.listdir('Accs')
                for i,v in enumerate(list_wallets):
                    if v == 'settings.json':
                        with open(f'Accs/{v}') as settings:
                            data = json.load(settings)

                        list_wallets.pop(i)
                # arr = [i for i in range(len(list_wallets))]
                for i,v in enumerate(list_wallets):

                    path = f'Accs/{v}'
                    timep = threading.Thread(target=SyncAccManager,args=(path,data['time'],self.okno))
                    timep.start()
            start_tasks()

        elif True:
            self.btnstarted = True
            th1o = threading.Thread(th1())
            th1o.start()



# data = Testing()