from typing import List
import argparse
import time

def multiply_serial(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    
    if not A or not B:
        raise ValueError("Empty matrices not allowed")
    n = len(A)
    m = len(A[0])
    p = len(B[0])
    if any(len(row) != m for row in A):
        raise ValueError("Inconsistent row sizes in A")
    if len(B) != m:
        raise ValueError(f"Inner dimensions must match: A is {n}x{m}, B is {len(B)}x{p}")

    
    C = [[0.0 for _ in range(p)] for _ in range(n)]

    
    for i in range(n):
        for k in range(m):
            aik = A[i][k]
            if aik == 0:
                continue
            row_bk = B[k]
            row_ci = C[i]
            for j in range(p):
                row_ci[j] += aik * row_bk[j]

    return C

def as_list(matrix):
    
    try:
        import numpy as _np
    except Exception:
        _np = None
    if _np is not None and isinstance(matrix, _np.ndarray):
        return matrix.tolist()
    return matrix

def pretty_print_matrix(name: str, M: List[List[float]]):
    print(f"{name} (shape {len(M)}x{len(M[0])}):")
    for row in M:
        print("  ", row)

def main():
    parser = argparse.ArgumentParser(description="Serial matrix multiplication demo")
    parser.add_argument("--numpy", action="store_true", help="Use numpy.dot if available")
    args = parser.parse_args()

    
    A = [[1, 0, -1],
         [4, -1, 2],
         [-1, 2, 4]]

    B = [[-1, 2, -3],
         [5, -4, 2],
         [4, 1, 0]]

    pretty_print_matrix("Matriz A", A)
    print()
    pretty_print_matrix("Matriz B", B)
    print()

    if args.numpy:
        try:
            import numpy as np
            A_np = np.array(A)
            B_np = np.array(B)
            t0 = time.perf_counter()
            C_np = np.dot(A_np, B_np)
            t1 = time.perf_counter()
            C = as_list(C_np)
            print(f"[serial] Tempo numpy.dot = {t1 - t0:.6f}s")
        except Exception as e:
            print("Numpy not available or error using numpy, falling back to pure Python:", e)
            t0 = time.perf_counter()
            C = multiply_serial(A, B)
            t1 = time.perf_counter()
            print(f"[serial] Tempo pure-Python = {t1 - t0:.6f}s")
    else:
        t0 = time.perf_counter()
        C = multiply_serial(A, B)
        t1 = time.perf_counter()
        print(f"[serial] Tempo pure-Python = {t1 - t0:.6f}s")

    print("==============================")
    print(" MATRIZ RESULTANTE FINAL C = A × B")
    print("==============================")
    pretty_print_matrix("Matriz C", C)

if __name__ == '__main__':
    main()
