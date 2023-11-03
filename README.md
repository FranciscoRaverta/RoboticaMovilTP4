# RoboticaMovil-TP3

### Instrucciones: 

#### Para correr usando EKF: 
Para correr una vez el algoritmo y graficar la trayectoria con una seed aleatoria:

```
python3 localization.py --plot ekf
```

Para correr una vez el algoritmo y graficar la trayectoria con una seed determinada (0, por ejemplo):

```
python3 localization.py --plot ekf --seed 0
```

Para correr el resto del análisis de ekf, considerando las ponderaciones a alpha y beta:

```
python3 run_tests.py ekf --plot
```


#### Para correr usando Parcticle Filter: 
```
python3 localization.py --plot pf
```

