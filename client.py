import socket

def start_client(host="127.0.0.1", port=8080):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"[Клиент подключён] К серверу {host}:{port}")

    try:
        while True:
            command = input("Введите команду: ").strip()
            if command.lower() == "exit":
                client_socket.sendall(command.encode('utf-8'))
                break

            client_socket.sendall(command.encode('utf-8'))
            response = client_socket.recv(4096).decode('utf-8')
            print(f"[Ответ сервера]: {response}")
    except KeyboardInterrupt:
        print("\n[Отключение клиента]")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
