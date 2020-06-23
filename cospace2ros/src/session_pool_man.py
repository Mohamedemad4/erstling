import os
import rospy
import subprocess as sp
from multiprocessing import Process

class session_pool():
    """
    Session_pool is used to run long running processes in the background
    Usage:
        sess_pool=session_pool()
    
        sess_pool.run_session_process("command")
        sess_pool.kill_session_process("command")
    NOTICE: supply command without the & argument run_session_process() handles pushing to the background for
    """
    def __init__(self):
        self.process_dict={}
        
    def session_process_thread(self,cmd):
        "Internal Method where the actual thread runs"
        exit_code=sp.call('({0})'.format(cmd),stdout=open(os.devnull, 'wb'),shell=True,executable='/bin/bash')
        return self.on_exit(cmd,exit_code)

    def run_session_process(self,cmd):   
        """run Session Process (nonblocking)"""
        proc_thread=Process(target=self.session_process_thread,args=(cmd,))
        proc_thread.start()
        rospy.loginfo("started Process with Cmd: "+cmd)
        self.process_dict.update({cmd:proc_thread})
        return proc_thread

    def kill_session_process(self,cmd):
        proc_thread=self.process_dict[cmd]
        proc_thread.terminate()
        del self.process_dict[cmd]

    def on_exit(self,cmd,exit_code):
        "Runs on command exit"
        if exit_code==0:
            rospy.loginfo("{0} exited with exit code 0".format(cmd))
        else:
            rospy.logwarn("{0} existed with NON zero exit code ".format(cmd))