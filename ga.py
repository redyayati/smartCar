import random 
import pickle
from particle import Particle
total = 100 


def saveVehicle(fitVehicle) : 
    with open('ML/VehiclesDriving/vehicleCar2.obj' , 'wb') as f : 
        pickle.dump(fitVehicle , f)
def loadVehicle() : 
    with open('ML/VehiclesDriving/vehicleCar1.obj' , 'rb') as f : 
        fitVehicle = pickle.load(f)
    return fitVehicle
def runFittestVehicle() : 
    fitVehicle = loadVehicle()
    cars.append(Car(fitVehicle))
    # group.add(cars)