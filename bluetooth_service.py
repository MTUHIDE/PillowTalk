import bluetooth
import os
import TextParser

textParser = TextParser.TextParser()
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "79bf39f7-54a4-4015-b27e-0b4be44b506d"

os.system('sudo hciconfig hci0 piscan')
bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            # protocols=[bluetooth.OBEX_UUID]
                            )

print("Waiting for connection on RFCOMM channel", port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from", client_info)

try:
    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        data = data.decode('utf-8')
        # todo send data to TextParser.py 
        #print(data)
        command = textParser.commandSearch(data)
        if command is not -1 and command is not -2:
            relayCommand = textParser.returnRelay(command)
            print(relayCommand)
except OSError:
    pass

print("Disconnected.")

client_sock.close()
server_sock.close()
print("All done.")
