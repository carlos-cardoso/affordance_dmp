# Setup

## Install gazebo with dart: [Official Instructions](http://gazebosim.org/tutorials?tut=install_from_source&cat=install)
```
### Make sure you have removed the Ubuntu pre-compiled binaries before installing from source:
sudo apt-get remove '.*gazebo.*' '.*sdformat.*' '.*ignition-math.*' '.*ignition-msgs.*' '.*ignition-transport.*'

sudo apt-get update \
&& sudo apt-get -y install gnupg2 wget lsb-release software-properties-common mercurial cmake libprotobuf-dev protobuf-compiler  \
  qtbase5-dev qtdeclarative5-dev qtmultimedia5-dev \
  qtdeclarative5-qtquick2-plugin qtdeclarative5-window-plugin \
  qtdeclarative5-qtmultimedia-plugin qtdeclarative5-controls-plugin \
  qtdeclarative5-dialogs-plugin libqt5svg5

### Install Required Dependencies
sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'

wget http://packages.osrfoundation.org/gazebo.key -O - |  apt-key add - \
&&  apt-get update

wget https://bitbucket.org/osrf/release-tools/raw/default/jenkins-scripts/lib/dependencies_archive.sh -O /tmp/dependencies.sh

ROS_DISTRO=dummy . /tmp/dependencies.sh
for i in $(sed 's:\\ ::g' <<< $BASE_DEPENDENCIES) $(sed 's:\\ ::g' <<< $GAZEBO_BASE_DEPENDENCIES); do sudo apt-get -y --ignore-missing  install $i; done

sudo apt-get -y install libignition-msgs-dev libignition-math4-dev libignition-transport4-dev libsdformat6-dev libfreeimage-dev libtar-dev libqwt-dev libtbb-dev libogre-1.9-dev libcurl4-gnutls-dev

### DART Support

# Main repository
sudo  apt-add-repository ppa:dartsim \
&&  sudo apt-get update \
&&  sudo apt-get -y install libdart6-dev

# Optional DART utilities
sudo apt-get -y install libdart6-utils-urdf-dev 

# Build And Install Gazebo
hg clone https://bitbucket.org/osrf/gazebo /tmp/gazebo \
&& cd /tmp/gazebo \
&& mkdir build \
&& cd build \
&& cmake ../ \
&& cmake -DCMAKE_INSTALL_PREFIX=/home/$USER/local ../ \
&& make -j4 \
&& make install 
```

## Install yarp with python bindings
```
sudo apt-get update && sudo apt-get -y install cmake libace-dev build-essential git \
  cmake-curses-gui libeigen3-dev libace-dev libedit-dev\
  swig \
  python2.7-dev \
  qtbase5-dev qtdeclarative5-dev qtmultimedia5-dev \
  qtdeclarative5-qtquick2-plugin qtdeclarative5-window-plugin \
  qtdeclarative5-qtmultimedia-plugin qtdeclarative5-controls-plugin \
  qtdeclarative5-dialogs-plugin libqt5svg5
git clone https://github.com/robotology/yarp
cd yarp && mkdir build && cd build && cmake -DYARP_USE_PYTHON_VERSION=2.7 -DBUILD_SHARED_LIBS=ON -DCREATE_PYTHON=ON -DYARP_COMPILE_BINDINGS=ON -DCREATE_GUIS=ON -DCREATE_LIB_MATH=ON .. && make && make install
```
## Install gazebo-yarp-plugins

```
cd ws
git clone https://github.com/robotology/gazebo-yarp-plugins.git
cd gazebo-yarp-plugins \
  && mkdir build \
  && cd build \
  && cmake ../ -DCMAKE_INSTALL_PREFIX=/ws/gazebo-yarp-plugins \
  && make install \
  ```

## Install icub-gazebo

```
cd ws
git clone https://github.com/robotology/icub-gazebo.git
export GAZEBO_MODEL_PATH=/ws/icub-gazebo
```

## Install pydmps
```
git clone https://github.com/studywolf/pydmps.git
sudo python setup.py install
```

## Run
```
yarpserver
```
```
source load_gazebo.sh 
gazebo icub_fixed.world
```

### to control joints directly
```
yarpmotorgui --robot icubSim
```

### run a dmp
```
python dmp.py
```

