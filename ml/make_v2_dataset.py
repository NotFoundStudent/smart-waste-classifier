
from pathlib import Path

import numpy as np
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "waste.csv"
NUMERIC_COLS = ["weight_g", "moisture_pct"]
TARGET = "category"
TARGET_PER_CLASS = 16
SEED = 42


def make_v2():
    df = pd.read_csv(DATA_PATH)

    # 1) 清洗：去掉完全重复的行
    df = df.drop_duplicates().reset_index(drop=True)

    # 2) 增强：每个类别扩充到 TARGET_PER_CLASS 个样本
    rng = np.random.default_rng(SEED)
    parts = []
    for cat in df[TARGET].unique():
        sub = df[df[TARGET] == cat]
        need = TARGET_PER_CLASS - len(sub)
        if need > 0:
            extra = sub.sample(n=need, replace=True, random_state=SEED).copy()
            extra[NUMERIC_COLS] = extra[NUMERIC_COLS].astype(float)
            noise = rng.normal(0, 0.02, size=(len(extra), len(NUMERIC_COLS)))
            extra[NUMERIC_COLS] = extra[NUMERIC_COLS].to_numpy() + noise
            extra["weight_g"] = extra["weight_g"].clip(lower=0.0)
            extra["moisture_pct"] = extra["moisture_pct"].clip(lower=0.0, upper=100.0)
            parts.append(pd.concat([sub, extra], axis=0))
        else:
            parts.append(sub)

    v2 = pd.concat(parts, axis=0).reset_index(drop=True)
    v2 = v2.sample(frac=1.0, random_state=SEED).reset_index(drop=True)
    v2.to_csv(DATA_PATH, index=False)
    print(f"已写入 v2: {DATA_PATH}")
    print(f"行数: {len(df)} -> {len(v2)}")
    print(v2[TARGET].value_counts())


if __name__ == "__main__":
    make_v2()
