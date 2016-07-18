#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License,
    or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, see <http://www.gnu.org/licenses/>.

    Bare client example:
        address = ('', 23000)
        omxSocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        omxSocket.connect(address)
        omxSocket.send('play /path/to/movie/movie.mkv omxsound=hdmi')
        omxSocket.send('forward_bit')
        omxSocket.send('status')
        playing = omxSocket.recv(1024)
        if playing[0:4] == 'True':
           omxSocket.send('stop')
        omxSocket.close()

    Better yet, use the included client
     
"""

__author__ = "Stefan Gansinger"
__version__ = "1.1"
__email__ = "stifi.s@freenet.de"
__credits__ = ["Robin Rawson-Tetley", "Johannes Baiter", "JugglerLKR", "CRImier"]


import pexpect
import select
import socket
import sys
from pipes import quote

# OMXPLAYER = "/usr/bin/omxplayer.bin"
OMXPLAYER = "/usr/bin/omxplayer"
LDPATH = "/opt/vc/lib:/usr/lib/omxplayer"

simple_commands = {
"forward_bit":"\033[C",
"forward_lot":"\033[A",
"backward_bit":"\033[D",
"backward_lot":"\033[B",
"toggle_subs":"s",
"show_subs":"w",
"hide_subs":"x",
"next_subs":"m",
"prev_subs":"n",
"volume_up":"+",
"volume_down":"-",
"next_audio":"k",
"prev_audio":"j",
"next_chapter":"o",
"prev_chapter":"i",
"increase_speed":"1",
"pause":"p"}

quit_command = "q"

def error_wrapper(func): #A safety check wr
    def wrapper(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
            if result or result is None:
                self.respond('OK')
            else:
                self.respond('FAIL')
        except AttributeError:
            if not self.omxProcess or not self.omxProcess.isalive():
                self.respond("PLAYER_NOT_RUNNING")
            else:
                self.respond("UNKNOWN_COMMAND")
        except KeyboardInterrupt:
            self.respond("ERROR")
    return wrapper

class omxPlayerServer():
    omxProcess = None
    omxSocket = None
    current_client = None
    stop_flag = False

    default_sound = "hdmi"
 

    def __init__(self, address = ('', 23000)):
        self.omxSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.playing = False
        self.playUrl = None
        try:
            self.omxSocket.bind(address)
        except socket.error, msg:
            sys.stderr.write("[ERROR] %s.\n" % msg[1])
            sys.exit(1)

    def startServer(self):
        self.stop_flag = False
        try:
            while not self.stop_flag:
                self.receive_message()
        except KeyboardInterrupt:
            self.omxSocket.close()
        finally:
            self.omxSocket.close()

    def receive_message(self):
        message = "" 
        # test if new object is in omxSocket, using a timeout of 10.0s --> "polling for messages"
        if select.select([self.omxSocket],[],[],10.0)[0]:
            # FIXME: maintain message length
            message, clientAddr = self.omxSocket.recvfrom(4096) 
            self.current_client = clientAddr
            if message.strip(' '):
                self.parse_message(message)

    def parse_message(self, message):
        if ' ' in message:
            command, data = message.split(' ', 1)
        else:
            command = message
            data = None
        if hasattr(self, command):
            function = getattr(self, command)
            function(data)
        elif command in simple_commands:
            self.custom_cmd(simple_commands[command])
        else:
            self.custom_cmd(data)

    def respond(self, message):
        self.omxSocket.sendto(message, self.current_client)

    @error_wrapper
    def play(self, data):
        if data == None:
            return False #Nothing to play specified
        if " sound=" in data: #Ugly? Yes. Unlikely to break anything? Yes.
            data, sound = data.rsplit(' ', 1)
            sound = sound[len("sound="):]
        else:
            sound = self.default_sound
        self.playUrl = data
        cmd = [OMXPLAYER,"-r","-o",sound,quote(self.playUrl)]
        if self.omxProcess is None or not self.omxProcess.isalive(): #only play if not already
            self.omxProcess = pexpect.spawn(' '.join(cmd), env = {"LD_LIBRARY_PATH" : LDPATH})
            self.playing = True
        
    @error_wrapper
    def halt(self, *args):
        self.omxProcess.send(quit_command)
        if self.omxProcess.isalive():
            self.omxProcess.wait()
        self.omxSocket.close()
        self.stop_flag = True

    @error_wrapper
    def kill(self, *args):
        self.omxProcess.send(quit_command)
        self.omxProcess.close(force=True)

    @error_wrapper
    def status(self, *args):
        self.respond("{} {}".format("Playing" if self.playing else "Stopped", self.playUrl if self.playing else "None"))
        
    @error_wrapper
    def stop(self, *args):
        self.omxProcess.send(quit_command)
        self.omxProcess.wait() 
        self.playing = False
        
    @error_wrapper
    def custom_cmd(self, message):
        self.omxProcess.send(message)


if __name__ == "__main__":
    socket = omxPlayerServer()
    socket.startServer()
