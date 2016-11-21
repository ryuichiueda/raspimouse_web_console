#!/usr/bin/env python
import rospy, os
import CGIHTTPServer

def kill():
    os.system("kill -KILL " + str(os.getpid()))

os.chdir(os.path.dirname(__file__))
rospy.init_node("webserver")
rospy.on_shutdown(kill)
CGIHTTPServer.test()
