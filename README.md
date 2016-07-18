omxSocket
=======================

Socket Interface for omxplayer using Python. Written by @stifi, heavily refactored by @CRImier. 

Installation:

pip install omxSocket

To use the server, run  "python -m omxSocket.omxServer". Theoretically, it should work, in practice you might need launch it in a certain way or fix permissions so that the omxplayer can run.

To use the client interactively, use "python -i -m omxSocket.omxClient.py", where -i would drop you into the console with the "client" object already initialized and connected. You'll get status responses printed back.

#### Commands:
* play /path/to/file [audio=hdmi] - starts the omxplayer instance with given path 
* pause - toggles pause
* stop - stops the omxplayer instance
* halt - closes the omxplayer instance and shuts down the server
* kill - forcibly exits the omxplayer instance
* status - returns "Playing /path/to/file" while omxplayer is running and "Stopped None" when it's not.
* custom_cmd keystroke - Send a custom keystroke 
* forward_bit - Forward 600s
* forward_lot - Forward 30s
* backward_bit - Backward 600s
* backward_lot - Backward 30s 
* toggle_subs
* show_subs
* hide_subs
* next_subs
* prev_subs
* volume_up
* volume_down
* next_audio
* prev_audio
* next_chapter
* prev_chapter
* increase_speed

### TODO:
* remake it to use subprocess.Popen
* enable debug logging
* enable omxplayer output parsing for error and status messages
