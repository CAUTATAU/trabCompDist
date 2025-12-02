import socket
import pickle
import numpy as np
import time

# -----------------------------
# MULTIPLICAÇÃO SERIAL
# -----------------------------
def multiply_serial(A, B):
    n, m = A.shape
    m2, p = B.shape

    if m != m2:
        raise ValueError(f"Dimensões incompatíveis: A é {n}x{m} e B é {m2}x{p}")

    C = np.zeros((n, p))

    for i in range(n):
        for k in range(m):
            aik = A[i, k]
            if aik == 0:
                continue
            for j in range(p):
                C[i, j] += aik * B[k, j]

    return C

# -----------------------------
# MULTIPLICAÇÃO DISTRIBUÍDA
# -----------------------------
def split_matrix(matrix, num_splits):
    return np.array_split(matrix, num_splits)

def send_to_server(subA, matrixB, server_ip, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))

    payload = pickle.dumps((subA, matrixB))
    sock.sendall(len(payload).to_bytes(8, "big"))
    start = time.perf_counter()
    sock.sendall(payload)

    data_size = int.from_bytes(sock.recv(8), "big")

    data = b""
    while len(data) < data_size:
        packet = sock.recv(4096)
        if not packet:
            break
        data += packet

    result = pickle.loads(data)
    end = time.perf_counter()

    sock.close()
    print(f"    [client] Tempo envio/recebimento {server_ip}:{server_port} = {end - start:.6f}s")
    return result

# -----------------------------
# ENTRADA DO USUÁRIO (SHAPE)
# -----------------------------
try:
    n = int(input("Digite o número de linhas de A: "))
    m = int(input("Digite o número de colunas de A (e linhas de B): "))
    p = int(input("Digite o número de colunas de B: "))
except:
    print("Erro: valores inválidos!")
    exit()

# -----------------------------
# GERA MATRIZES ALEATÓRIAS
# -----------------------------
A = np.random.randint(-10, 10, size=(n, m))
B = np.random.randint(-10, 10, size=(m, p))

print("\nMatriz A:")
print(A)

print("\nMatriz B:")
print(B)

# -----------------------------
# PROCESSAMENTO SERIAL
# -----------------------------
print("\n==============================")
print(" PROCESSAMENTO SERIAL ")
print("==============================")

try:
    t0 = time.perf_counter()
    C_serial = multiply_serial(A, B)
    t1 = time.perf_counter()
    print(f"[serial] Tempo total = {t1 - t0:.6f}s")
except ValueError as e:
    print("Erro na multiplicação serial:", e)
    exit()

# -----------------------------
# PROCESSAMENTO DISTRIBUÍDO
# -----------------------------
servers = [
    ("localhost", 5000),
    ("localhost", 5001),
    ("localhost", 5002)
]

num_servers = len(servers)
submatrices = split_matrix(A, num_servers)

print("\n==============================")
print(" PROCESSAMENTO DISTRIBUÍDO ")
print("==============================")

results = []
total_start = time.perf_counter()

for i, (host, port) in enumerate(servers):
    subA = submatrices[i]
    print(f" --> Enviando {subA.shape} para {host}:{port}")
    result = send_to_server(subA, B, host, port)
    results.append(result)

total_end = time.perf_counter()
print(f"[distribuído] Tempo total = {total_end - total_start:.6f}s")

C_dist = np.vstack(results)

# -----------------------------
# COMPARAÇÃO FINAL
# -----------------------------
print("\n==============================")
print(" MATRIZ RESULTANTE SERIAL ")
print("==============================")
print(C_serial)

print("\n==============================")
print(" MATRIZ RESULTANTE DISTRIBUÍDA ")
print("==============================")
print(C_dist)

# -----------------------------
# VERIFICAÇÃO DE CORRETUDE
# -----------------------------
if np.allclose(C_serial, C_dist):
    print("\n✅ SUCESSO: As matrizes serial e distribuída são IGUAIS.")
else:
    print("\n❌ ERRO: As matrizes são DIFERENTES!")
