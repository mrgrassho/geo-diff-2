# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 21:07:41 2021

@author: rolon
"""

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import datetime

# Graficar relacion entre dos atributos de un dataframe
def graph_xy(df,columnX, columnY, label1, label2, title):
    if columnX=="": valuesX = np.arange(0, len(resume_log), 1)
    else: valuesX = df[[columnX]]
    
    valuesY = df[[columnY]]
    fig, ax = plt.subplots()
    ax.plot(valuesX, valuesY)
    ax.set(xlabel=label1, ylabel=label2,
           title=title)
    ax.grid()
    
    
# Cambiar numero de experimento y worker para obtener los graficos
log = pd.read_csv('./experiment_1/worker1.csv') 
log = log[(log['NAME'] == "geo-diff-work_worker")]

uptime_prev = 'sas'
# Datadrame con la información de la VM agrupada por unidad de tiempo.
resume_log = pd.DataFrame(columns = ['time','cpu_perc','ram_mb','ram_perc_avg','net_in','net_out'])

sum_cpu_perc = 0          # Sumo los porcentajes
sum_ram_bytes = 0         # Sumo los bytes, luego convierto a Mb
sum_ram_perc = 0          # Promedio de porcentaje de ram usado
sum_net_in_bytes = 0      # Sumo los bytes recibidos
sum_net_out_bytes = 0     # Sumo los bytes enviados
count = 0 
initial_time= datetime.datetime(2020,1,1,
                            int(log["UPTIME"][1][0:2]), 
                            int(log["UPTIME"][1][3:5]), 
                            int(log["UPTIME"][1][6:8]))

for i in log.index:
  if str(log["UPTIME"][i])!=uptime_prev and i!=1:   # Si la unidad de tiempo cambia.
    # añado nueva instancia al dataframe resume_log
    current_time = datetime.datetime(2020,1,1,
                                int(log["UPTIME"][i][0:2]), 
                                int(log["UPTIME"][i][3:5]), 
                                int(log["UPTIME"][i][6:8]))
    diff_time = (current_time-initial_time).total_seconds() / 60
    new_row = {'time': diff_time,
               'cpu_perc': sum_cpu_perc,
               'ram_mb': sum_ram_bytes/1000000 ,
               'ram_perc_avg': sum_ram_perc/count,
               'net_in': sum_net_in_bytes/1000000 ,
               'net_out': sum_net_out_bytes/1000000 
               }
    resume_log = resume_log.append(new_row, ignore_index=True)
    # reinicio contadores y sumas
    count= 0      
    sum_cpu_perc = 0                                   
    avg_ram_perc = 0
    sum_ram_bytes = 0   
    sum_net_in_bytes = 0
    sum_net_out_bytes = 0
  
  # Suma de los bytes es igual al primer servicio en esa unidad de tiempo 
  sum_cpu_perc+= float(log["CPU %"][i][:-1])
  sum_ram_bytes+=log["MEM USAGE"][i]                
  sum_ram_perc+= float(log["MEM %"][i][:-1]) 
  sum_net_in_bytes+=log[" NET I"][i]
  sum_net_out_bytes+=log["NET O"][i]
  count+= 1 
  uptime_prev = log['UPTIME'][i]


graph_xy(resume_log,"time",'ram_mb','tiempo (min)','uso de ram (mb)','relacion tiempo y uso de ram')
graph_xy(resume_log,"time",'ram_perc_avg','tiempo (min)','% ram promedio','relacion tiempo y uso de ram ')
graph_xy(resume_log,"time",'net_out','tiempo (min)','uso de la red (mb enviados)','relacion tiempo y uso de la red')
graph_xy(resume_log,"time",'cpu_perc','tiempo (min)','uso de cpu (%)','relacion tiempo y uso de cpu')
