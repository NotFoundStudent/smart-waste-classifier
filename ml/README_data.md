\# README\_data.md 数据集说明

\## 数据源

>【A同学填写数据集来源】



\## DVC远程存储配置

Azure Blob Storage

\- Storage‑Account：wut2026

\- Container：dvc

\- 路径前缀：smart‑waste‑classifier/

> SAS鉴权令牌保存在本地 .dvc/config.local，\\\*\\\*该文件不会提交到Git仓库\\\*\\\*。



\## Dataset v1

\- 描述：第一版原始垃圾分类数据集 `data/waste.csv`

\- Git commit hash：【粘贴v1的commit hash】

\- 存储位置：Azure远程 smart‑waste‑classifier/ 前缀下



\## Dataset v2

\- v1 → v2变更说明：【A同学填写，例：去除异常样本、类别样本均衡、增加合成样本】

\- Git commit hash：【粘贴v2的commit hash】

\- 存储位置：Azure远程 smart‑waste‑classifier/ 前缀下



\### 复现操作

```bash

\\# 获取数据集

dvc pull



\\# 切换回v1版本示例

git switch <v1‑commit‑hash>

dvc pull



\\# 切回开发分支最新版本

git switch dev

dvc pull




