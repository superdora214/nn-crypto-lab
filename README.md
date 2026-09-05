# nn-crypto-lab

研究生课题实验仓库：神经网络 × 密码学方向。

## 课题简介

（在这里用 3-5 句话写清：研究什么问题、现有方法的不足、你的切入点。写论文时这段可以直接改造成摘要初稿。）

## 环境搭建

环境由 conda 管理，定义见 `environment.yml`。

```bash
# 从定义文件重建环境（新机器上执行）
conda env create -f environment.yml
conda activate pytorch-gpu

# 安装本项目的包（开发模式，src 下的代码可直接 import）
pip install -e .
```

## 目录结构

```
├── src/            # 核心代码：模型、密码学模块（可复用，写成包）
├── experiments/    # 实验脚本：一次实验一个文件，结果落到 results/
├── notebooks/      # Jupyter 探索性分析（实验性代码，验证后再进 src/）
├── tests/          # 正确性验证：加密模块用标准测试向量做 pytest 用例
├── data/           # 数据集（不入库）
├── results/        # 输出：图表、指标、checkpoints（不入库）
└── environment.yml # conda 环境定义，保证可复现
```

## 使用约定

- **每次实验可复现**：实验脚本开头固定随机种子（`torch.manual_seed`、`numpy.random.seed`），并把超参数、Git commit hash 一起写进 results。
- **核心函数必须先过测试**：涉及字节序列、随机数、模运算的函数，用 NIST 标准测试向量在 `tests/` 里验证后再用于实验。
- **提交规范**：一个功能/一次实验改动一个 commit，说明写清楚改了什么、为什么。

## 运行实验

```bash
python experiments/<实验名>.py
```

结果输出到 `results/<实验名>/<时间戳>/`。
