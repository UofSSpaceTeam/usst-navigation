import vrep
import sys
from pynput.keyboard import Key, Listener

def on_press(key):
    try: k = key.char 
    except: k = key.name 
    if k == 'a':
        res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'K3_robot',vrep.sim_scripttype_childscript, 'getHandle',[],[],[],'',vrep.simx_opmode_blocking)
     
    if k == 'up':
        res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'K3_robot',vrep.sim_scripttype_childscript, 'forward',[],[],[],'',vrep.simx_opmode_blocking)
       
    if k == 'down':
        res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'K3_robot',vrep.sim_scripttype_childscript, 'backward',[],[],[],'',vrep.simx_opmode_blocking)
       
    if k == 'left':
        res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'K3_robot',vrep.sim_scripttype_childscript, 'turnLeft',[],[],[],'',vrep.simx_opmode_blocking)
       
    if k == 'right':
        res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'K3_robot',vrep.sim_scripttype_childscript, 'turnRight',[],[],[],'',vrep.simx_opmode_blocking)
       
    if k == 's':
        res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'K3_robot',vrep.sim_scripttype_childscript, 'stop',[],[],[],'',vrep.simx_opmode_blocking)
       
      
    if k == 'o':
        res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'K3_robot',vrep.sim_scripttype_childscript, 'openFinger',[],[],[],'',vrep.simx_opmode_blocking)
        
    if k == 'c':
        res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'K3_robot',vrep.sim_scripttype_childscript, 'closeFinger',[],[],[],'',vrep.simx_opmode_blocking)
        
    if k == 'u':
        res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'K3_robot',vrep.sim_scripttype_childscript, 'ArmUp',[],[],[],'',vrep.simx_opmode_blocking)
    
    if k == 'd':
        res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'K3_robot',vrep.sim_scripttype_childscript, 'ArmDown',[],[],[],'',vrep.simx_opmode_blocking)
       
    if k == 'e':
        res,retInts,retFloats,retStrings,retBuffer=vrep.simxCallScriptFunction(clientID,'K3_robot',vrep.sim_scripttype_childscript, 'exit',[],[],[],'',vrep.simx_opmode_blocking)
        

def on_release(key):
    if key == Key.esc:
        # Stop listener
        return False




vrep.simxFinish(-1)
clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
if clientID!= -1:
    print("Connected to remote server")
else:
    print('Connection not successful')
    sys.exit('Could not connect')
  
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()