# from bluetooth import *
# import os
#
#
# class BluetoothService:
#
#     def __init__(self, server_socket=None, client_socket=None):
#         if server_socket is None:
#             self.server_socket = server_socket
#             self.client_socket = client_socket
#             self.service_name = "BluetoothServices"
#             self.uuid = "79bf39f7-54a4-4015-b27e-0b4be44b506d"
#         else:
#             self.server_socket = server_socket
#             self.client_socket = client_socket
#
#     def get_socket(self):
#         try:
#             self.server_socket = BluetoothSocket(RFCOMM)
#         except (BluetoothError, SystemExit, KeyboardInterrupt) as e:
#             print("Failed to create the bluetooth server socket " + e)
#
#     def get_connection(self):
#         try:
#             self.server_socket.bind(("", PORT_ANY))
#             print("Bluetooth server socket bind successfully on host "" to PORT_ANY...")
#         except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
#             print("Failed to bind server socket on host to PORT_ANY ... " + e)
#
#         try:
#             self.server_socket.listen(1)
#             print("Bluetooth server socket put to listening mode successfully ...")
#         except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
#             print("Failed to put server socket to listening mode  ... " + e)
#
#         try:
#             port = self.server_socket.getsockname()[1]
#             print("Waiting for connection on RFCOMM channel %d" % port)
#         except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
#             print("Failed to get connection on RFCOMM channel  ... " + e)
#
#     def advertise(self):
#         try:
#             advertise_service(self.server_socket, self.service_name,
#                               service_id=self.uuid,
#                               service_classes=[self.uuid, SERIAL_PORT_CLASS],
#                               profiles=[SERIAL_PORT_PROFILE],
#                               #                   protocols = [ OBEX_UUID ]
#                               )
#             print("%s advertised successfully ..." % self.service_name)
#         except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
#             print("Failed to advertise bluetooth services  ... " + e)
#
#     def accept_connection(self):
#         try:
#             self.client_socket, client_info = self.server_socket.accept()
#             print("Accepted bluetooth connection from %s", client_info)
#         except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
#             print("Failed to accept bluetooth connection ... " + e)
#
#     def recv_data(self):
#         try:
#             while True:
#                 data = self.client_socket.recv(1024)
#                 if not data:
#                     break
#                 message = str.decode(data, 'uft-8')
#                 print(message)
#         except (Exception, IOError, BluetoothError):
#             pass
#
#     def close_socket(self):
#         try:
#             self.client_socket.close()
#             self.server_socket.close()
#             print("Bluetooth sockets successfully closed ...")
#         except (Exception, BluetoothError) as e:
#             print("Failed to close the bluetooth sockets " + e)
#
#     def start(self):
#         self.get_socket()
#         self.get_connection()
#         self.advertise()
#         self.accept_connection()
#
#     def stop(self):
#         # Disconnecting bluetooth sockets
#         self.close_socket()
#
#
# if __name__ == '__main__':
#     os.system('sudo hciconfig hci0 piscan')
#     bluetooth_service = BluetoothService()
#     bluetooth_service.start()
#     while True:
#         bluetooth_service.recv_data()
#     bluetooth_service.stop()
import bluetooth
import os


def command(string):
    c = string.split()
    if c[0] == 'inflates':
        if c[1] == 'cushion_1':
            print('inflates cushion_1 for ' + c[2] + ' seconds')
        elif c[1] == 'cushion_2':
            print('inflates cushion_2 for ' + c[2] + ' seconds')

    if c[0] == 'deflates':
        if c[1] == 'cushion_1':
            print('deflates cushion_1 for ' + c[2] + ' seconds')
        elif c[1] == 'cushion_2':
            print('deflates cushion_2 for ' + c[2] + ' seconds')


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
        command(data)
        print(data)
except OSError:
    pass

print("Disconnected.")

client_sock.close()
server_sock.close()
print("All done.")
