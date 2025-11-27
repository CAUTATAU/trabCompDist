import socket
import pickle
import numpy as np
import time

def split_matrix(matrix, num_splits):
    return np.array_split(matrix, num_splits)

def send_to_server(subA, matrixB, server_ip, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))
    payload = pickle.dumps((subA, matrixB))
    start = time.perf_counter()
    sock.sendall(payload)

    result = sock.recv(10_000_000)
    result = pickle.loads(result)
    end = time.perf_counter()
    sock.close()
    elapsed = end - start
    print(f"    [client] Tempo envio/recebimento {server_ip}:{server_port} = {elapsed:.6f}s")
    return result

A = np.array([[1, 0, -1],
                  [4, -1, 2],
                  [-1, 2, 4]])

B = np.array([[-1, 2, -3],
                  [5, -4, 2],
                  [4, 1, 0]])

print("Matriz A:")
print(A)
print("\nMatriz B:")
print(B)

servers = [
        ("localhost", 5000),
        ("localhost", 5001)
    ]

num_servers = len(servers)

submatrices = split_matrix(A, num_servers)
print("\nEnviando submatrizes para servidores...")

results = []
total_start = time.perf_counter()
for i, (host, port) in enumerate(servers):
    subA = submatrices[i]
    print(f" --> Enviando {subA.shape} para {host}:{port}")
    result = send_to_server(subA, B, host, port)
    results.append(result)
total_end = time.perf_counter()
print(f"[client] Tempo total de envio/recebimento para todos servidores = {total_end - total_start:.6f}s")

C = np.vstack(results)
print("\n==============================")
print(" MATRIZ RESULTANTE FINAL C = A × B")
print("==============================")
print(C)