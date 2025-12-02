import socket
import pickle
import numpy as np
import sys
import time

def multiply(subA, matrixB):
    return np.dot(subA, matrixB)

PORT = int(sys.argv[1])

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', PORT))
server_socket.listen(5)
print(f"Server listening on port {PORT}")
while True:
    conn, addr = server_socket.accept()
    print(f"Connection from {addr}")
    data_size = int.from_bytes(conn.recv(8), "big")
    data = b""
    while len(data) < data_size:
        packet = conn.recv(4096)
        if not packet:
            break
        data += packet
    subA, matrixB = pickle.loads(data)
    print(f"Received subA shape: {subA.shape}, matrixB shape: {matrixB.shape}")
    t0 = time.perf_counter()
    result = multiply(subA, matrixB)
    t1 = time.perf_counter()
    elapsed = t1 - t0
    print(f"    [server:{PORT}] Tempo multiplicação = {elapsed:.6f}s")
    response = pickle.dumps(result)
    conn.sendall(len(response).to_bytes(8, "big"))
    conn.sendall(response)
    conn.close()
    print("Result sent back to client")