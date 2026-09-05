"""实验模板：每次新实验复制本文件改名。

约定（见 README）：
- 开头固定所有随机种子，保证实验可复现；
- 把超参数、Git commit hash、环境信息一起写进 results/<实验名>/<时间戳>/；
- 图表和指标输出到同一目录，代码在 src/、脚本在 experiments/，不要混。
"""
import json
import random
import subprocess
import time
from pathlib import Path

import numpy as np
import torch

import crypto_utils

# ── 1. 实验配置：所有超参数集中在这里，跑完随结果一起存档 ──────────────
CONFIG = {
    "seed": 42,
    "model": "MLP-2hidden",
    "hidden_dim": 128,
    "epochs": 10,
    "learning_rate": 1e-3,
    "note": "示例实验：演示实验脚本的标准结构",
}


def fix_seed(seed: int) -> None:
    """固定 python/numpy/torch 三个层面的随机种子。"""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def git_commit_hash() -> str:
    """取当前 commit hash，用来标记'这个结果是哪版代码跑出来的'。"""
    try:
        return subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def main() -> None:
    fix_seed(CONFIG["seed"])

    # ── 2. 建立本次实验的输出目录 ──────────────────────────────────────
    exp_name = Path(__file__).stem
    out_dir = Path("results") / exp_name / time.strftime("%Y%m%d-%H%M%S")
    out_dir.mkdir(parents=True, exist_ok=True)

    meta = {
        **CONFIG,
        "git_commit": git_commit_hash(),
        "torch": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu",
    }
    (out_dir / "config.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("实验配置与环境已存档:", out_dir / "config.json")

    # ── 3. 实验主体（示例：演示调用 src/ 里的密码学工具 + 一个小模型）──
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"device = {device}")

    # 示例输入：把一段哈希值当作二分类特征（占位，换成你的课题设定）
    x = torch.tensor(
        [[int(b) for b in crypto_utils.derive_key(b"demo", b"salt", 16)]],
        dtype=torch.float32, device=device,
    )
    model = torch.nn.Sequential(
        torch.nn.Linear(16, CONFIG["hidden_dim"]),
        torch.nn.ReLU(),
        torch.nn.Linear(CONFIG["hidden_dim"], 1),
    ).to(device)
    print("前向输出:", model(x).item())

    # ── 4. 训练循环、指标记录（tensorboard / json）、画图，替换成真实逻辑 ──
    (out_dir / "metrics.json").write_text(
        json.dumps({"status": "template-demo", "output": model(x).item()}, indent=2),
        encoding="utf-8",
    )
    print("实验结束，结果见:", out_dir)


if __name__ == "__main__":
    main()
