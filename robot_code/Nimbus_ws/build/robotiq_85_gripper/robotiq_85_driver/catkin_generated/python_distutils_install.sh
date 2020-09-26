#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
    DESTDIR_ARG="--root=$DESTDIR"
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/lnair3/Nimbus_ws/src/robotiq_85_gripper/robotiq_85_driver"

# snsure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/lnair3/Nimbus_ws/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/lnair3/Nimbus_ws/install/lib/python2.7/dist-packages:/home/lnair3/Nimbus_ws/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/lnair3/Nimbus_ws/build" \
    "/usr/bin/python" \
    "/home/lnair3/Nimbus_ws/src/robotiq_85_gripper/robotiq_85_driver/setup.py" \
    build --build-base "/home/lnair3/Nimbus_ws/build/robotiq_85_gripper/robotiq_85_driver" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/home/lnair3/Nimbus_ws/install" --install-scripts="/home/lnair3/Nimbus_ws/install/bin"
