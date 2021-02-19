# Análisis de Carga

A continuación estudiaremos el análisis de carga del stack de aplicaciones de work (`work-stack`) tanto de manera local como distribuida. En el primer análisis ahondaremos en el rendimiento utilizando una sola máquina para todos servicios y luego, en el segundo análisis, veremos varias configuraciones utilizando varias máquinas conectadas formando un cluster de Docker engines también conocido como Swarm.

**¿Objetivo?**

El principal objetivo de este experimento es encontrar el número óptimo de Workers para el hardware disponible.

## Localhost Experiment

En el siguiente informe se detalla diferentes pruebas utilizando configuraciones de los parametros que afectan el scaling de la `work stack`. En este caso las pruebas fueron realizadas en una Dell XPS (1.6 GHz Dual-Core Intel Core i5, 8 GB 1600 MHz DDR3) con Ubuntu 20.04 LTS, y con los recursos provistos (~1.2GB en tiles). [VER ANÁLISIS](./analysis/workers-performance-comparison.pdf)

## Swarm Experiment

En el siguiente informe se detalla un conjunto de pruebas ejecutadas en un cluster de máquinas con Docker, en el que variaremos los diferentes parametros que repercuten en el rendimiento del stack. En este caso las pruebas fueron realizadas en AWS utilizando 6 instancias `t2.micro` (3.3 GHz Intel Xeon 1 Core, 1GB de RAM, 8GB* de almacenaminto). [VER ANÁLISIS](./analysis/aws-performance-comparison.md)

* Todas las instancias salvo el `manager`/`admin` que tiene 30GB de almacenamiento.

## Comparativa

...
