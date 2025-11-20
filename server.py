import socket
import pickle
import numpy as np
import sys

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
    data = conn.recv(10_000_000)
    subA, matrixB = pickle.loads(data)
    print(f"Received subA shape: {subA.shape}, matrixB shape: {matrixB.shape}")
    result = multiply(subA, matrixB)
    conn.sendall(pickle.dumps(result))
    conn.close()
    print("Result sent back to client")