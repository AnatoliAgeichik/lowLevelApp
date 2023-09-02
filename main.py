import socket


URLS = {"/": "Hello, World", "/team": "Hello, Team"}


def get_body(status: int, url: str):
    if status == 200:
        return f"<h1>{URLS.get(url)}</h1>"
    elif status == 404:
        return f"<h1>404</h1><p>Not found</p>"
    elif status == 405:
        return f"<h1>405</h1><p>Method not allowed</p>"


def parse_method_and_url_from_request(request: str) -> tuple[str]:
    request_list = request.split()
    return (request_list[0].decode(), request_list[1].decode())


def get_status(method: str, url: str) -> int:
    if url not in URLS.keys():
        return 404
    if method != "GET":
        return 405
    return 200


def get_header(status: int) -> tuple:
    if status == 200:
        return "HTTP/1.0 200 OK\n\n"
    elif status == 404:
        return "HTTP/1.1 404 Not found\n\n"
    elif status == 405:
        return "HTTP/1.1 405 Method not allowed\n\n"


def generate_response(request: str):
    method, url = parse_method_and_url_from_request(request)
    status = get_status(method, url)
    header = get_header(status)
    body = get_body(status, url)
    return (header + body).encode()


def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 5005))
    server_socket.listen()

    while True:
        client_socket, address = server_socket.accept()
        request = client_socket.recv(1024)
        client_socket.sendall(generate_response(request))
        client_socket.close()


if __name__ == "__main__":
    run()
