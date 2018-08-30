yarpserver 
load_gazebo911.sh 
gzserver-9.1.1 ball_icub
yarpmotorgui --robot icubSim
gzclient
killall -9 gzserver-9.1.1 


