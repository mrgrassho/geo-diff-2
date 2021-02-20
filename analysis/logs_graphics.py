# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 21:07:41 2021

@author: matiasrolon
"""

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import datetime

# Graficar relacion entre dos atributos de un dataframe
def graph_xy(valuesX, valuesY, namesX, labelX, labelY, title):
    fig, ax = plt.subplots()
    
    for i in range(0,len(valuesX)):
        ax.plot(valuesX[i], valuesY[i], label=namesX[i])         # grafico cada serie del array valuesX.
    ax.set(xlabel=labelX, ylabel=labelY, title=title)
    plt.legend(loc='best')
    #plt.xlim(0, 10)                                             # Cambiar zoom al eje X
    ax.grid() 
    
# VARIABLES GLOBALES     
# ---------------------------------------------------------------------------------------------
experiment = 4
path_logs =  ['./logs/experiment_'+str(experiment)+'/worker1.csv',
              './logs/experiment_'+str(experiment)+'/worker2.csv',
              './logs/experiment_'+str(experiment)+'/worker3.csv',
              './logs/experiment_'+str(experiment)+'/worker4.csv',
              './logs/experiment_'+str(experiment)+'/manager.csv'
              ]

services = ["geo-diff-work_worker","geo-diff-work_updater","geo-diff-work_admin-worker",
            "geo-diff-work_dealer","geo-diff-work_rabbitmq-server"]
#El servicio que queremos comparar entre logs de VMs
selected_service = services[0]
# ---------------------------------------------------------------------------------------------
time_by_log = []
ramMB_by_log = []
ramPerc_by_log = []
cpuPerc_by_log = []
netOut_by_log = []
netIn_by_log = []
xnames_by_log = []

# Recorre todos los logs y hace un grafico comparativo de como funciona el servicio geodif_worker en esa VM.
for current_path in path_logs:    
    # Cambiar numero de experimento y worker para obtener los graficos
    log = pd.read_csv(current_path) 
    log = log[(log['NAME'] == selected_service)]
    if len(log)>0:    
        print('[+] Se encontraton '+str(len(log))+' intancias del servicio ' + selected_service + ' para el log ' + current_path)
        uptime_prev = ''
        # Dataframe con la información de la VM agrupada por unidad de tiempo.
        resume_log = pd.DataFrame(columns = ['time','cpu_perc','ram_mb','ram_perc_avg','net_in','net_out'])
        
        sum_cpu_perc = 0          # Sumo los porcentajes
        sum_ram_bytes = 0         # Sumo los bytes, luego convierto a Mb
        sum_ram_perc = 0          # Promedio de porcentaje de ram usado
        sum_net_in_bytes = 0      # Sumo los bytes recibidos
        sum_net_out_bytes = 0     # Sumo los bytes enviados
        count = 0 
        initial_time= datetime.datetime(2020,1,1,
                                    int(log.iloc[0]["UPTIME"][0:2]), 
                                    int(log.iloc[0]["UPTIME"][3:5]), 
                                    int(log.iloc[0]["UPTIME"][6:8]))
        
        for i in range(0,len(log)-1):
          if str(log.iloc[i]["UPTIME"])!=uptime_prev and i!=0:   # Si la unidad de tiempo cambia.
            # añado nueva instancia al dataframe resume_log
            current_time = datetime.datetime(2020,1,1,
                                        int(log.iloc[i]["UPTIME"][0:2]), 
                                        int(log.iloc[i]["UPTIME"][3:5]), 
                                        int(log.iloc[i]["UPTIME"][6:8]))
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
            sum_ram_perc = 0
            sum_ram_bytes = 0   
            sum_net_in_bytes = 0
            sum_net_out_bytes = 0
          
          # Suma de los bytes es igual al primer servicio en esa unidad de tiempo 
          sum_cpu_perc+= float(log.iloc[i]["CPU %"][:-1])
          sum_ram_bytes+=log.iloc[i]["MEM USAGE"]              
          sum_ram_perc+= float(log.iloc[i]["MEM %"][:-1]) 
          sum_net_in_bytes+=int(log.iloc[i][" NET I"])
          sum_net_out_bytes+=int(log.iloc[i]["NET O"])
          count+= 1 
          uptime_prev = log.iloc[i]['UPTIME']
        
        time_by_log.append(resume_log["time"])
        ramMB_by_log.append(resume_log["ram_mb"])
        cpuPerc_by_log.append(resume_log["cpu_perc"])
        ramPerc_by_log.append(resume_log["ram_perc_avg"])
        netOut_by_log.append(resume_log["net_out"])
        netIn_by_log.append(resume_log["net_in"])
        xnames_by_log.append(current_path.replace('.csv','')[7:])
    else: print('[-] No se encontraron instancias del servicio '+ selected_service +' para el log '+current_path)    
    
print('[+] Generando graficos...')
graph_xy(time_by_log,
         ramMB_by_log,
         xnames_by_log,
         'tiempo (min)',
         'ram (mb)',
         'relacion tiempo y uso de ram en servicio '+ selected_service.split('_')[1]) 

graph_xy(time_by_log,
         cpuPerc_by_log,
         xnames_by_log,
         'tiempo (min)',
         'cpu (%)',
         'relacion tiempo y uso de cpu en servicio '+ selected_service.split('_')[1])

graph_xy(time_by_log,
         netOut_by_log,
         xnames_by_log,
         'tiempo (min)',
         'bytes enviados (mb)',
         'relacion tiempo y uso de red en servicio '+ selected_service.split('_')[1])    

graph_xy(time_by_log,
         netIn_by_log,
         xnames_by_log,
         'tiempo (min)',
         'bytes recibidos (mb)',
         'relacion tiempo y uso de red en servicio '+ selected_service.split('_')[1])     
