Python-omxplayer-Socket
=======================

Socket Interface for omxplayer using Python. Written by @stifi, heavily refactored by @CRImier.

To use the server, run it as "python omxServer.py". Theoretically, it should work, in practice you might need launch it in a certain way or fix permissions so that the omxplayer can run.

To use the client interactively, use "python -i omxClient.py", where -i would drop you into the console with the "client" object already initialized and connected. You'll get status responses printed back.

### TODO:
* as for now, list of commands is available by looking through server code, needs to be exported somewhere
* remake it to use subprocess.Popen.
* enable debug logging
* enable omxplayer output parsing for error and status messages
