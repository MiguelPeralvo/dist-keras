"""Scripts which is able to start the dist-keras native Daemons."""

## BEGIN Imports. ##############################################################

from distkeras.native.daemon import Daemon

import optparse

import os

import signal

import sys

## END Imports. ################################################################

## BEGIN Globals. ##############################################################

# Specify the Daemon global. We need this for signal handling.
g_daemon = None

## END Globals. ################################################################

def parse_arguments():
    parser = optparse.OptionParser()
    parser.set_defaults(multicast_port=Daemon.PORT_MULTICAST, allocation_port=0)
    parser.add_option('--port-multicast', action='store', dest='multicast_port', type='int')
    parser.add_option('--port-allocation', action='store', dest='allocation_port', type='int')
    (options, args) = parser.parse_args()

    return options

def allocate_daemon(port_multicast, port_allocation):
    daemon = Daemon()
    daemon.set_port_multicast(port_multicast)
    daemon.set_port_allocation(port_allocation)

    return daemon

def handle_signal_sigint(signal, frame):
    global g_daemon

    g_daemon.stop()

def main():
    global g_daemon

    # Parse the program arguments.
    options = parse_arguments()
    port_multicast = options.multicast_port
    port_allocation = options.allocation_port
    # Set the signal handlers.
    signal.signal(signal.SIGINT, handle_signal_sigint)
    # Allocate the daemon, and start the process.
    daemon = allocate_daemon(port_multicast, port_allocation)
    g_daemon = daemon
    daemon.start()
    signal.pause()
    daemon.join()

if __name__ == '__main__':
    main()