import os
import shutil
import socket
import threading

# Указываем рабочую директорию сервера
WORKING_DIR = os.path.join(os.getcwd(), "server_directory")
os.makedirs(WORKING_DIR, exist_ok=True)

def handle_client(client_socket):
    def send_response(response):
        client_socket.sendall(response.encode('utf-8'))

    while True:
        try:
            request = client_socket.recv(1024).decode('utf-8').strip()
            if not request:
                break

            print(f"[Запрос клиента]: {request}")
            command, *args = request.split(' ', 1)
            args = args[0] if args else ""

            if command == "LIST":
                files = os.listdir(WORKING_DIR)
                response = "\n".join(files) if files else "Директория пуста"
                send_response(response)

            elif command == "MKDIR":
                folder_name = os.path.join(WORKING_DIR, args)
                os.makedirs(folder_name, exist_ok=True)
                send_response(f"Папка '{args}' создана.")

            elif command == "RMDIR":
                folder_name = os.path.join(WORKING_DIR, args)
                if os.path.isdir(folder_name):
                    shutil.rmtree(folder_name)
                    send_response(f"Папка '{args}' удалена.")
                else:
                    send_response(f"Папка '{args}' не найдена.")

            elif command == "RMFILE":
                file_name = os.path.join(WORKING_DIR, args)
                if os.path.isfile(file_name):
                    os.remove(file_name)
                    send_response(f"Файл '{args}' удалён.")
                else:
                    send_response(f"Файл '{args}' не найден.")

            elif command == "RENAME":
                old_name, new_name = args.split(' ', 1)
                old_path = os.path.join(WORKING_DIR, old_name)
                new_path = os.path.join(WORKING_DIR, new_name)
                if os.path.exists(old_path):
                    os.rename(old_path, new_path)
                    send_response(f"'{old_name}' переименован в '{new_name}'.")
                else:
                    send_response(f"'{old_name}' не найден.")

            elif command == "UPLOAD":
                file_name, file_content = args.split(' ', 1)
                with open(os.path.join(WORKING_DIR, file_name), 'w') as file:
                    file.write(file_content)
                send_response(f"Файл '{file_name}' загружен на сервер.")

            elif command == "DOWNLOAD":
                file_name = os.path.join(WORKING_DIR, args)
                if os.path.isfile(file_name):
                    with open(file_name, 'r') as file:
                        send_response(file.read())
                else:
                    send_response(f"Файл '{args}' не найден.")

            elif command == "EXIT":
                send_response("Отключение...")
                break

            else:
                send_response("Неизвестная команда.")
        except Exception as e:
            send_response(f"Ошибка: {e}")
            break

    client_socket.close()

def start_server(host="0.0.0.0", port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[Сервер запущен] Слушаю на {host}:{port}...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[Новое подключение] {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_server()
