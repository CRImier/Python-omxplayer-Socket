import socket


class omxClient():

    def __init__(self, address = ('', 23000)):
        self.omxSocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        self.address = address
        self.omxSocket.settimeout(1)

    def connect(self):
        self.omxSocket.connect(self.address)

    def command(self, message):
        self.omxSocket.send(message)
        response = self.omxSocket.recv(1024)
        return response

    def shutdown(self):
        self.omxSocket.close()


if __name__ == "__main__":
    client = omxClient()
    client.connect()
    print("Examples:")
    print("client.command('play /path/to/movie/movie.mkv omxsound=hdmi')")
    print("client.command('forward_bit')")
    print("""response = client.command('status')
if response.startswith('Playing'):
    client.command('stop')""")
    print("In the end, use:")
    print("client.shutdown()")


