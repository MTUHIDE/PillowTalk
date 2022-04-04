import bluetooth
import os
import json
import requests


power_on = True

# TODO: Update for new MotorControl functions
def run_server():
    url = 'http://localhost:3000/motorcontrol'
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
            
            params = json.loads(data)
            print(params)
            
            r = requests.post(url = url, json = params)
            print(r)

            # send the command back up to the app so that it can verify it sent
            client_sock.send(data)  # currently echos the data sent
    except OSError:
        pass
    

    print("Disconnected.")

    client_sock.close()
    server_sock.close()
    print("All done.")


def main():
    os.system('sudo hciconfig hci0 piscan')
    while power_on:
        run_server()


if __name__ == "__main__":
    main()
