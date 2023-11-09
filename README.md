# RoboticaMovil-TP4

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
Para correr una vez el algoritmo y graficar la trayectoria con una seed aleatoria:

```
python3 localization.py --plot pf
```

Para correr una vez el algoritmo y graficar la trayectoria con una seed determinada (0, por ejemplo), y con un determinado número de partículas:

```
python3 localization.py --plot pf --seed 0 --num-particles 100
```

Para correr el resto del análisis de ekf, considerando las ponderaciones a alpha y beta, comparando para 20, 50 y 500 particulas:

```
python3 run_tests.py pf --plot --num_particles 100
```
