#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import rospy
from geventwebsocket.handler import WebSocketHandler
from gevent import pywsgi
from raspimouse_ros.srv import *

ws_list = set()

class WebOperator:
    def __init__(self):
        self.server = pywsgi.WSGIServer(('0.0.0.0', 8000), self.res, handler_class=WebSocketHandler)
        rospy.on_shutdown(self.server.close)
        self.server.serve_forever()

    def operation(self, environ, start_response):
        ws = environ['wsgi.websocket']
        ws_list.add(ws)
        while True:
            msg = ws.receive()
            if msg is None:
                break
            remove = set()
            for s in ws_list:
                try:
                    print msg
                    s.send(msg)
                    rospy.wait_for_service('/switch_motors')
                    p = rospy.ServiceProxy('/switch_motors', SwitchMotors)
                    if msg == "fw":
                        res = p(True)
                    else:
                        res = p(False)
                except Exception:
                    remove.add(s)
            for s in remove:
                ws_list.remove(s)
    
    def res(self, environ, start_response):  
        path = environ["PATH_INFO"]
        if path == "/": 
            start_response("200 OK", [("Content-Type", "text/html")])  
            return self.operation(environ, start_response)
        else:
            start_response("200 OK", [("Content-Type", "text/html")])  
            return "NOT FOUND"

if __name__ == "__main__":
    rospy.init_node("web_console")
    op = WebOperator()
    #server = pywsgi.WSGIServer(('0.0.0.0', 8000), res, handler_class=WebSocketHandler)
