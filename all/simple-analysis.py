import pandas as pd
import numpy as np
import sys


def sparse(x: np.ndarray) -> float:
    w: int = int(x.shape[0])
    h: int = int(x.shape[1])
    full: int = w * h
    sp: int = 0

    for i in range(w):
        for j in range(h):
            if x[i, j] == 0:
                sp += 1
    return float(sp) / float(full)


def distance(x: np.ndarray) -> float:
    w: int = int(x.shape[0])
    h: int = int(x.shape[1])
    full: int = w * h
    sp: int = 0

    for i in range(w):
        for j in range(h):
            if x[i, j] != 0:
                sp += (i - j) ** 2
    return float(sp) / float(full)


def distance_amount(x: np.ndarray) -> float:
    w: int = int(x.shape[0])
    h: int = int(x.shape[1])
    full: int = w * h
    sp: int = 0

    for i in range(w):
        for j in range(h):
            if x[i, j] != 0:
                sp += x[i, j] * (i - j) ** 2
    return float(sp) / float(full)


def main():
    s: list[tuple[str, float]] = []
    d: list[tuple[str, float]] = []
    da: list[tuple[str, float]] = []

    for f in sys.argv[1:]:
        print(f"Reading: {f}")
        data: pd.DataFrame = pd.read_csv(f)
        data_np: np.ndarray = data.to_numpy()[:, 1:]

        s.append((f, sparse(data_np)))
        d.append((f, distance(data_np)))
        da.append((f, distance_amount(data_np)))

    print("Sparsity")
    for ss in sorted(s, key=lambda x: x[1]):
        print(f"{ss[0]}, {ss[1] * 100:>.2f}%")
    print()
    print("Distance")
    for ds in sorted(d, key=lambda x: x[1]):
        print(f"{ds[0]}, {ds[1]:>.2f}")
    print()
    print("Distance & Amount")
    for das in sorted(da, key=lambda x: x[1]):
        print(f"{das[0]}, {das[1]:>.2f}")


if __name__ == "__main__":
    main()
