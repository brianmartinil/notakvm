from subprocess import Popen, PIPE
from time import sleep

import wmi, sys, os, psutil

## Change these to match your monitor's inputs
THIS_COMPUTER_INPUT_ID = 15
OTHER_COMPUTER_INPUT_ID = 17

CREATE_NEW_PROCESS_GROUP = 0x00000200
DETACHED_PROCESS = 0x00000008

script_dir = os.path.dirname(os.path.realpath(__file__))

current_input = THIS_COMPUTER_INPUT_ID

# This verion uses an external program to send the DDC/CI command to the monitor.  It is doable
# from code but it is a lot chunky Win32 stuff.  This is easier.
def switch_input(input):
    global current_input # I don't understand why this is necessary
    if current_input != input:
        os.system("%s\\ControlMyMonitor.exe /SetValue Primary 60 %s" % (script_dir, input))
        current_input = input

# See if a previous instance of the script is running and kill it
def kill_previous_instance():
    for proc in psutil.process_iter():
        if is_prev_instance(proc):
            print("Found a running version with PID %s, killing." % proc.pid)

            try:
                proc.kill()
            except:
                print("Kill failed, you might end up with multiple instances running.")

def is_prev_instance(proc):
    try:
        cmd_line = proc.cmdline()
    except psutil.AccessDenied:
        # We don't own this process, so it can't be a previous instance
        return False

    # Avoid finding the "launch" process
    if len(cmd_line) != 2:
        return False

    if os.path.realpath(sys.executable) == os.path.realpath(cmd_line[0]) and os.path.realpath(__file__) == os.path.realpath(cmd_line[1]):
       return True

def main(launch=False):
    # If we are started with the parameter "launch", we run another version of ourselves but omit 
    #  the "launch" parameter, and use popen to spawn it in the background.  This will be our 
    #  long-running background process.
    if launch:
        kill_previous_instance()

        # launch ourselves without the "launch" parameter
        # we always launch with the executable directly and __file__ so that we can find it
        # in the process list
        p = Popen([sys.executable, __file__], stdin=PIPE, stdout=PIPE, stderr=PIPE,
            creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)
        exit()

    # If we've made it here, we are the background process not the launcher, or we chose not to use the 
    # launcher

    # Set up the WMI watchers that will detect device plugging / unplugging
    raw_connect_wql = "SELECT * FROM __InstanceCreationEvent WITHIN 2 WHERE TargetInstance ISA \'Win32_Keyboard\'"
    raw_disconnect_wql = "SELECT * FROM __InstanceDeletionEvent WITHIN 2 WHERE TargetInstance ISA \'Win32_Keyboard\'"
    c = wmi.WMI()
    connected_watcher = c.watch_for(raw_wql=raw_connect_wql)
    disconnected_watcher = c.watch_for(raw_wql=raw_disconnect_wql)

    current_input = THIS_COMPUTER_INPUT_ID
    switch_input(current_input)

    # THe main event loop, check to see if the watched device has been plugged in or unplugged and 
    # switch to the appropriate input
    while 1:
        try:
            connected = connected_watcher(timeout_ms=0)
        except wmi.x_wmi_timed_out:
            pass
        else:
            if connected:
                switch_input(THIS_COMPUTER_INPUT_ID)

        try:
            disconnected = disconnected_watcher(timeout_ms=0)
        except wmi.x_wmi_timed_out:
            pass
        else:
            if disconnected:
                switch_input(OTHER_COMPUTER_INPUT_ID)

        sleep(.1)

# If the script is launched from the setuptools alias
def setuptools_launch():
    do_launch = len(sys.argv) > 1 and sys.argv[1] == 'launch'
    sys.exit(main(do_launch))

# If the script is launched from the command line
if __name__ == "__main__":
    do_launch = len(sys.argv) > 1 and sys.argv[1] == 'launch'
    sys.exit(main(do_launch))