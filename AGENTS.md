# AGENTS.md

## 仓库定位

工作流插件仓库 (Codex marketplace, 名 `math-research`): 4 个插件组成 管理-研究-验证 一体化数学研究工作流.

## 目录结构

- `.agents/plugins/marketplace.json` — marketplace 清单 (插件顺序 = Codex 渲染顺序)
- `plugins/<plugin-name>/` — 每个插件: `.codex-plugin/plugin.json` + `skills/<skill-name>/SKILL.md`
- `scripts/validate_all.py` — 仓库级校验入口 (本地与 CI 共用)
- `.github/workflows/validate.yml` — CI 校验

## 维护规则

1. 每次变更后运行 `python scripts/validate_all.py` (Python 3.10+, 建议 `PYTHONUTF8=1`).
2. 修改 `skills/<name>/` 内文件后, 若该 skill 带 `MANIFEST.sha256`, 必须重新生成并提交 (sha256 逐文件).
3. 修改插件元数据或 SKILL 内容后, 按语义化版本升级 `version` (大版本 = 架构/能力代际, 小版本 = 功能批次, 补丁 = 纯修复); 不再使用日期后缀.
4. marketplace 插件顺序即 Codex UI 渲染顺序; 编排插件置顶, 新增插件追加到列表末尾.
5. 所有文本文件 UTF-8 无 BOM, 换行 LF (`.gitattributes` 已强制).
6. 同步顺序: 先 push 父仓库 `xsoc1/rigorous-open-math-research`, 再用 GitHub merge-upstream 同步 fork `Zhongshan-Big-Jun/rigorous-open-math-research`.
7. 如实记录: 不编造验证结果, 无法验证的能力明确标注为未验证.

## 注意事项 (Notes for future agents)

- **推送顺序**: `project.json` 配置 `git_sync.push_order = ["origin", "fork"]`, 提交后
  先 push `xsoc1/rigorous-open-math-research` (父仓库), 再 push
  `Zhongshan-Big-Jun/rigorous-open-math-research` (fork).
- **fork 自动同步**: 已提供 `.github/workflows/sync-fork.yml`, 但需要仓库 secret
  `FORK_PAT` 才会生效; 未配置时用 `scripts/sync-fork.sh` 手动同步.
- **本地 canonical clone**: DSH 适配仓库的同步源是
  `~/.dsh/_math-research-upstream/rigorous-open-math-research`, 不是工作区里的
  `_xsoc1_work`; 保持该 canonical clone 与 origin/main 同步.
- **DSH 适配依赖**: `xsoc1/math-research-dsh` 单向消费本仓库内容; 本仓库内容变更后,
  需在 DSH 仓库重跑 `scripts/sync-from-parent.py` 继承.
- **版本管理**: 修改插件元数据或 SKILL 内容后按语义化版本升级
  `version` (大版本 = 架构/能力代际, 小版本 = 功能批次, 补丁 = 纯修复);
  不再使用 cachebuster 日期后缀. rigorous 当前为 `1.12.0`, workflow 当前为 `1.15.0`,
  manage 当前为 `1.8.1`, lean-verify 当前为 `1.6.0`.
- **GitHub 网络**: 直连 github.com 失败时, 用本地代理 push:
  `git -c http.proxy=http://127.0.0.1:7897 push origin main` (本机实测可用).

## 会话记录

- 完整旧记录: [AGENTS_HISTORY.md](AGENTS_HISTORY.md). 仅在查找历史决策, benchmark 或故障证据时按关键词读取相关段落.
- 2026-09-05 用户要求: 根据既有 benchmark 优化 Codex 研究插件, 重点完善真实文献读取, agent 可注释工具库与指针表, 以及额度中断续接; 额度恢复后继续实施.
- 本轮方法: 先做确定性 L0, 使用隔离的真实工具卡和 sequence-26 工件回放; 保留主项目原文件和数学状态. 高成本 solver A/B 留待后续匹配实验.
- 功能与验证证据见父仓库 docs/optimization-20260905-results.md; 发布和恢复入口见 docs/optimization-20260905-progress.md. 每次维护在本节追加简短结果, 长证据放专门报告.
- 2026-09-06 用户报告额度恢复后完成发布核对: manage 1.8.1 的 BOM/旧卡片修复和真实 L0 回放已发布, 父仓库与 DSH 1.15.1 CI 通过, Codex 和 DSH helper 哈希一致. 新数学 A/B 尚未运行, 同名技能副本只诊断和记录来源.
- 2026-09-06 用户批准三臂 benchmark 开始. 恢复入口为 benchmarks/codex-20260906-l1/STATUS.md. 先冻结旧版/新版/空白环境及相同模型预算, 用无模型 probe 核实隔离, 再逐臂运行并记录实际额度. 真实 cwd 已纠正, 不从桌面误传路径创建项目.
- 2026-09-06 用户要求继续. 改用 WSL 的固定 0.153.4 CLI 和新隔离目录, 现有代理已可用. T1 三臂完成文件/网络隔离与本地请求清单预检, 修复配置重写丢失插件启用项的问题; 新增限时单写运行器, 同 session 续接和 4 项无模型测试. 正式运行状态和剩余额度仍以 benchmark STATUS.md 及外部 run/state.json 为准.
- 2026-09-06 T1 初次空白组因 code-mode host 关闭导致工具不可用, 62.29 秒后停止并排除计分. r1 六个全新环境启用并固定匹配宿主, T1 三组通过真实工具调用和模拟同 ID 续接检查. 剩余额度低于启动门槛, 续接时直接读取 STATUS.md 的 r1 入口, 不重做准备, 不续接无效尝试.
- 2026-09-06 用户再次要求继续, 五小时额度恢复而周额度剩余 21%. 原 25% 周保留线为协调器策略, 在 r1 首次求解前记录资源修订为周剩余 <=10% 时停止; 本轮先推进 T1 空白组及盲审. 复用已通过预检的环境, 不改题目, 模型, 时间上限或评分.
- 2026-09-06 用户明确要求不需要保留额度. 取消全部人为额度保留线; 耗尽, 状态过期和固定运行时间仍触发检查点. 已运行段保留原代码哈希, 如旧门槛触发则按同会话及剩余预算续接. 未授权使用重置积分.
- 2026-09-06 T1 r1 空白组完成并冻结, 443.19 秒, 7 次有用量记录的响应; 41354 非缓存输入, 86272 缓存输入, 13231 输出 token. 尚待独立匿名盲审, 不将求解器自称证明完成直接计为通过. 用 response_id 去重继承用量, 未知项保留 null.
- 2026-09-06 T1 空白组独立盲审 PASS 100/100, 无实质缺口或补证. 求解 443.19 秒, 盲审 393.09 秒, 共 74002 非缓存输入和 25255 输出 token. 已保存匿名审计及 response_id 去重指标; 开始旧版插件 A 组, 不提前推断插件收益.
- 2026-09-06 用户要求继续. A 组日志确认此前因真实额度耗尽退出, 已按原 session 续接, 保留 451.422577 秒消耗和现有证明工件, 剩余 1348.577423 秒. 用户不保留额度的要求继续有效, 未兑换重置积分. 该自然中断不替代新版恢复功能的受控对照.
- 2026-09-06 A 组完成, 累计 1277.998 秒, 含一次内部审计, 返回 123374 非缓存输入和 35714 输出 token. 已按原字节处理冻结副本的目录内文件链接, 保留收据. 外部盲审仅去掉首行旧审计状态, 正文和原答案保持哈希绑定; 尚不计外部通过. 恢复入口仍为 benchmark STATUS.md.
