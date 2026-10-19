\# Smart Waste Classifier 智能垃圾分类项目

\## 项目简介

机器学习驱动垃圾分类应用；使用DevOps+MLOps，Git/GitHub、Docker、GitHub‑Actions CI/CD；DVC做数据版本管理，MLflow做实验跟踪。



\## 分支策略（课程规定）

\- `feature/\*`：功能开发分支；所有新功能从dev分支切出

\- `dev`：开发集成分支；feature分支通过PR合并进入dev

\- `staging`：预发布验证分支；dev通过PR合并到staging

\- `main`：生产版本分支；staging通过PR合并到main



合并链路：`feature → dev → staging → main`



\### 分支保护规则

dev / staging / main 全部开启分支保护：

1\. 修改必须走Pull Request；禁止直接git push

2\. CI流水线必须全部检查通过，才允许合并PR



\## CI / CD流水线触发说明

1\. \*\*CI(.github/workflows/ci.yml)\*\*

触发事件：向`dev/staging/main`发起Pull Request

执行任务：

\- python依赖安装

\- ruff静态代码检查

\- black代码格式校验

\- pytest完整测试套件（至少3个测试用例，带边界case）

\- docker镜像构建校验



2\. \*\*CD(.github/workflows/deploy.yml)\*\*

触发事件：代码push合并进入staging或者main分支

\- 合并到staging：读取staging环境secrets生成.env，构建staging docker镜像

\- 合并到main：读取production环境secrets生成.env，构建production docker镜像

> 重要说明：本项目只在GitHub runner本地构建镜像，\*\*没有部署到外部服务器\*\*，符合课程要求No release process is requested。



\## MLOps说明

1\. DVC：数据集版本管理，远程存储使用Microsoft Azure Blob Storage；维护v1、v2两个数据集版本，原始数据不提交GitHub。

文档位置：`ml/README\_data.md`

2\. MLflow：模型实验跟踪，基线模型+调优改进模型；文档位置：`ml/README\_experiments.md`



\## 本地运行

```bash

\# 拉取代码

git clone https://github.com/NotFoundStudent/smart‑waste‑classifier.git

cd smart‑waste‑classifier



\# 拉取数据集（需要本地配置Azure SAS令牌）

dvc pull



\# 构建docker镜像

docker build -t waste-app .



\# 启动应用

docker run --rm waste-app



