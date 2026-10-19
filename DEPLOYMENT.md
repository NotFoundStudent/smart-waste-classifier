

\### 📄DEPLOYMENT.md（根目录）

```markdown

\# DEPLOYMENT.md

\## 流水线说明

本项目使用 GitHub Actions实现自动化构建，\*\*没有部署到外部云服务器，仅在GitHub runner本地构建Docker镜像\*\*。



1\. CI流水线（ci.yml）

触发：所有Pull Request指向 `dev / staging / main`

执行：依赖安装、ruff静态检查、black格式校验、pytest测试套件、docker镜像构建校验。

规则：CI检查不通过，PR禁止合并（分支保护规则）。



2\. CD流水线(deploy.yml)

\- push到 `staging`分支：加载GitHub Environment【staging】的Secrets，生成.env，构建waste‑app:staging镜像

\- push到 `main`分支：加载GitHub Environment【production】的Secrets，生成.env，构建waste‑app:production镜像



\### Secrets管理

环境变量密钥存储在GitHub Repository → Settings → Environments，不会写入代码仓库。

密钥名称：`APP\_ENV\_API\_KEY`



