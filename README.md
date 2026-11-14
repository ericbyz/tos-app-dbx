# tos-app-dbx

将开源数据库客户端 [DBX](https://github.com/t8y2/dbx)（Apache-2.0）封装为 [铁威马 TOS](https://www.terra-master.com) 应用中心 **deb 类应用**（x86_64 + aarch64 双架构）。

**这是什么**：TOS deb 元数据壳 + 可复现构建脚本。不修改、不重编译上游代码——直接锁定上游官方发布的 `dbx-web`（musl 静态二进制，自带 Web 前端），按《TOS 7 应用开发指南》第 8 章规范打包。

| 项目 | 值 |
|---|---|
| 应用 ID | `dbx` |
| 应用形态 | deb 类 · 外开模式（`open_path`）· 端口模式 |
| 访问地址 | `http://<NAS IP>:18224` |
| 上游版本 | v0.6.70（见 [UPSTREAM](UPSTREAM) 锁定） |
| 上游许可证 | Apache-2.0（本封装仓库同以 Apache-2.0 发布） |
| 运行依赖 | 无（上游为 musl 静态链接二进制，无 glibc 版本要求） |
| 数据目录 | `/var/lib/dbx`（`dbx.db` + 加密密钥 `.dbx/secret.key`） |

## 目录结构

```
tos-app-dbx/
├── config.ini            # TOS 平台元数据（JSON 内容，规范第 8 章）
├── dbx.lang              # 26 种语言的应用名称/描述
├── dbx.env               # 服务环境变量（端口/数据目录）
├── UPSTREAM              # 上游版本锁定（版本、资产名、SHA256）
├── DEBIAN/               # control + postinst/prerm/postrm
├── init.d/dbx.service    # systemd 服务单元（含安全加固）
├── images/icons/dbx.svg  # 应用图标
├── scripts/
│   ├── fetch_upstream.sh # 下载并校验上游资产（SHA256 强制核对）
│   ├── build_deb.py      # 纯 Python 的 dpkg-deb 兼容打包器（确定性构建）
│   ├── validate.py       # 按 TOS 审核规则校验元数据
│   ├── make_lang.py      # 生成 dbx.lang
│   └── bump_upstream.sh  # 升级上游版本（UPSTREAM/config.ini/control 联动）
├── build.sh              # 一键构建 ./build.sh [x86_64|aarch64]
└── .github/workflows/    # CI：校验 + 双架构构建 + Release 发布
```

## 本地构建

依赖：bash、curl、tar、python3（任意平台；有 dpkg-deb 时自动优先使用）。

```bash
./build.sh                # 双架构
./build.sh aarch64        # 单架构
./scripts/validate.py     # 元数据校验
```

产物：`build/output/dbx_<platform>.deb` + `.sha256`。

## 开发流程

### 分支与版本

- `main` 分支随时可构建；**发布只认 tag**：`v<上游版本>`（如 `v0.6.70`）。
- deb 包版本 = 上游 dbx 版本（config.ini `version`、DEBIAN/control `Version`、UPSTREAM `UPSTREAM_VERSION` 三处必须一致，CI 强制校验）。

### 日常修改（元数据/脚本/服务）

1. 修改 `config.ini` / `dbx.env` / `init.d/` / `DEBIAN/` 等；
2. `./scripts/validate.py` 本地校验；
3. 提交 PR → CI 自动跑 validate.yml；
4. 合并后无需发版（不改变包内容的改动可以攒着随下次上游升级一起发）。

### 升级上游版本

1. 查看 [dbx Releases](https://github.com/t8y2/dbx/releases) 新版本及其变更说明；
2. `./scripts/bump_upstream.sh <new-version>`（联动更新 UPSTREAM / config.ini / control）；
3. 从新版 Release 页下载 `.sha256` 文件，把两个 SHA256 填入 `UPSTREAM`；
4. `./build.sh && ./scripts/validate.py` 全量构建校验；
5. 在 TOS 虚拟机/实机上安装冒烟测试（安装 → 启动 → 打开页面 → 卸载）；
6. 提交 PR 合并，打 tag 触发 CI 发布（见下）。

### 发布（tag → CI → Release）

```bash
git tag v0.6.70
git push origin main v0.6.70
```

CI（build-deb.yml）自动：双架构构建 → `dpkg-deb -I/-c` 校验 → lintian（Error 级失败即阻断）→ 生成 SHA256 → 上传到 GitHub Release。

**发布后不得改动 Release 资产**——TOS 上架时锁定的版本号与 SHA256 必须与 Release 实际下载物一致，擅改会导致下架并取消奖励。

## 上架 TOS 开发者平台（ Checklist）

1. ☐ 在 [developer.terra-master.com](https://developer.terra-master.com) 用**外部邮箱**注册开发者账号（内部邮箱收不到验证码）；
2. ☐ x86_64 与 ARM **分别创建应用**（各自独立 App ID，应用名称相同或能相互对应，同一账号提交）；
3. ☐ 提交 `dbx_x86_64.deb` 与 `dbx_aarch64.deb`（Release 直链），锁定版本号与 SHA256；
4. ☐ 客服/反馈入口填写本仓库 Issues 链接；
5. ☐ 应用详情：名称、简介、图标、截图（在 TOS 实机截取，体现应用名称与主要功能界面）；
6. ☐ 声明上游许可证 Apache-2.0，提供上游源码仓库 https://github.com/t8y2/dbx 及本仓库构建脚本（可复现构建）；
7. ☐ 提交《参与报名表》登记（姓名、工号、开发者账号、应用名称、App ID，上传运行佐证材料）；
8. ☐ 双架构均过审并在应用中心展示后开始计奖；30 天内保持 Issue 响应。

> 提交前先查《已上线应用列表》确认无重复上架。

## 合规声明

- 本仓库仅做**封装与分发**，不包含对上游代码的修改；应用功能全部来自上游 [t8y2/dbx](https://github.com/t8y2/dbx)。
- 上游采用 [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0) 许可证，允许商用与再分发；本仓库保留版权与许可声明（见 LICENSE 与 NOTICE）。
- 安装包内容：上游官方 Release 的 `dbx-web` 静态二进制（SHA256 锁定，见 UPSTREAM）+ 本仓库元数据文件，无其他二进制。
- 本应用不收集任何用户数据；数据库连接凭据由上游机制加密存储于 `/var/lib/dbx/dbx.db`。

## 服务细节

- systemd 单元按 TOS 规范加固（`NoNewPrivileges`、`ProtectSystem=strict` 等），数据目录仅 `ReadWritePaths=/var/lib/dbx`；
- 未配置 `Restart=`（TOS 平台管理服务生命周期）；
- 端口 18224 位于 TOS 推荐区间 8000–19999，不与保留端口冲突；
- 端口模式下 TOS 平台不参与鉴权，建议安装后在 `dbx.env` 中设置 `DBX_PASSWORD` 启用 Web 登录保护。
