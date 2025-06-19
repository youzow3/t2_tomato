import pandas as pd
import numpy as np
import PIL.Image

import sys


def main():
    for f in sys.argv[1:]:
        print(f"Reading: {f}")
        data: pd.DataFrame = pd.read_csv(f)
        data_np: np.ndarray = data.to_numpy()[:, 1:]

        PIL.Image.fromarray((data_np / np.max(data_np) * 255
                             ).astype(np.uint8)
                            ).save(f"{f}-image-heat.png")

        data_np = data_np / np.maximum(data_np, 1)
        data_np = data_np.astype(np.uint8) * 255
        PIL.Image.fromarray(data_np).save(f"{f}-image.png")


if __name__ == "__main__":
    main()
