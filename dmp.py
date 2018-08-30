import yarp;
import time
import pickle


import numpy as np
import matplotlib.pyplot as plt

import pydmps
import pydmps.dmp_discrete

yarp.Network.init();

# prepare a property object
props = yarp.Property()
props.put("device","remote_controlboard")
props.put("local","/client/right_arm")
props.put("remote","/icubSim/right_arm")

# create remote driver
armDriver = yarp.PolyDriver(props)
time.sleep(1)

#query motor control interfaces
iPos = armDriver.viewIPositionControl()
iVel = armDriver.viewIVelocityControl()
iEnc = armDriver.viewIEncoders()
time.sleep(1)

#retrieve number of joints
jnts=iPos.getAxes()

print 'Controlling', jnts, 'joints'

# read encoders
encs=yarp.Vector(jnts)
iEnc.getEncoders(encs.data())

## store as home position
home=yarp.Vector(jnts, encs.data())
time.sleep(1)
#initialize a new tmp vector identical to encs
tmp=yarp.Vector(jnts)
for i in range(jnts):
    tmp.set(i, encs.get(i))

motions={}
with open('recorded.pickle', 'rb') as handle:
    motions = pickle.load(handle)
print(motions)


N=1000
demo = np.zeros((N, jnts))

ystart = [encs.get(i) for i in range(jnts)]

ymiddle = motions["neutraldown"]

yend = motions["stableup"]

for i in range(jnts):
    demo[0:int(N/2), i] = np.linspace(ystart[i], ymiddle[i], int(N/2))
    demo[int(N/2):N, i] = np.linspace(ymiddle[i], yend[i], int(N/2))

#y_des = np.load('2.npz')['arr_0'].T
#y_des -= y_des[:, 0][:, None]
y_des = demo.T

# test normal run
dmp = pydmps.dmp_discrete.DMPs_discrete(n_dmps=jnts, n_bfs=500, ay=np.ones(jnts)*10.0, dt=0.01)

dmp.imitate_path(y_des=y_des)

#y_track, dy_track, ddy_track = dmp.rollout()

# run while moving the target up and to the right
y_track = []
dmp.reset_state()
_error=0
for t in range(5*dmp.timesteps):
    y, _, _ = dmp.step(error=_error)
    y_track.append(np.copy(y))
    # move the target slightly every time step
    #dmp.goal += np.array([1e-2, 1e-2])

    for i in range(y.shape[0]):
        tmp.set(i, y[i])
    
    iPos.positionMove(tmp.data())
    time.sleep(0.1)
    iEnc.getEncoders(encs.data())
    time.sleep(0.1)
    encs_now=yarp.Vector(jnts, encs.data())
    qs = np.array([encs.get(i) for i in range(jnts)])
    _error = np.linalg.norm(y-qs)/16
    if np.isnan(_error):
        _error=0.001

    print(t)
    print(y)
    print(qs)
    print(_error)

y_track = np.array(y_track)


end=False
while end==False:
    cmd=raw_input("?")
    if cmd=="q":
        with open('filename.pickle', 'wb') as handle:
            pickle.dump(motions, handle, protocol=pickle.HIGHEST_PROTOCOL)
        end=True
    if cmd=="r":
        iEnc.getEncoders(encs.data())
        encs_now=yarp.Vector(jnts, encs.data())
        time.sleep(0.1)
        name=raw_input("name?")
        qs = [encs.get(i) for i in range(jnts)]
        motions[name]=qs
    if cmd=='p':
        name=raw_input("name?")
        tmp=yarp.Vector(jnts)
        try:
            for i in range(jnts):
                tmp.set(i, motions[name][i])
            iPos.positionMove(tmp.data())
        except KeyError:
            print("does not exist")



