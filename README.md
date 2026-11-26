# 壁画复制样张补色点选色

弥光壁画复制室按翻印样张毫米坐标试色，保留边界修订和干样证据，用带不确定区间的补色建议签认可预约的试色位。

## 现场工作与联系人

模拟客户为弥光壁画复制室。原画区域、调色色料试样、置信区间、补色坐标；保护边界外不得领用试色位。

- 复制样张边界 `proof_regions`，字段为 `label`（样张区域）、`pigment_family`（色样册）、`width_mm`（样张宽 mm）、`height_mm`（样张高 mm）、`frame_inset`（保护留边 mm）、`hold_x1`（留白起 X）、`hold_y1`（留白起 Y）、`hold_x2`（留白止 X）、`hold_y2`（留白止 Y）、`revision`（边界版次）。模型约束位于 `backend/domain/proof_regions_model.py`，规则位于 `proof_regions_service.py`。
- 干样点测色样 `dry_swatches`，字段为 `family`（色样册）、`fraction`（调色比例）、`ground_l`（底样 Lab 亮度）、`delta_e`（干样与复制参考 ΔE76）、`sample_ref`（点测凭证）、`dry_hours`（静置小时）、`witnessed`（已验真）。模型约束位于 `backend/domain/dry_swatches_model.py`，规则位于 `dry_swatches_service.py`。
- 色差区间签认 `shade_studies`，字段为 `panel`（样张）、`revision`（连续边界版次）、`x_mm`（补色点 X）、`y_mm`（补色点 Y）、`ground_l`（样张底色亮度）、`fraction`（建议调色比例）、`mean_de`（预测 ΔE76）、`lower_de`（95% 区间下端）、`upper_de`（95% 区间上端）、`test_mae`（留出格 MAE）、`token`（拟合凭证）。模型约束位于 `backend/domain/shade_studies_model.py`，规则位于 `shade_studies_service.py`。
- 试色位及试色回执 `patch_slots`，字段为 `panel`（样张）、`study`（签认簿）、`x_mm`（坐标 X）、`y_mm`（坐标 Y）、`site_key`（样张坐标索引）、`reader`（试色位责任人）、`delta_seen`（点测 ΔE76）、`receipt`（回执编号）、`state`（试色状态）。模型约束位于 `backend/domain/patch_slots_model.py`，规则位于 `patch_slots_service.py`。

团队为模拟的5 人复制室，负责干样补色和样张点位确认。

配色师分开维护色卡、区域草图和领样簿。未足时静置的色样偶尔混入对照，保护边界靠手工描图，细小色差的区间难随领用单追溯。

上游是原画保护框和干样色差读数，复制师接收带坐标的试色位。

### 一天的业务操作

1. 08:40 周潼确认 PANEL-W8 样张第 1 版保护边界和内保留区。
2. 09:10 季桥登记 SAND-BATCH 调色比例 .51 的 26 小时干样，凭证 COLOR-QA。静置只有 8 小时的样片被送回复测。
3. 10:00 读取样张底色 L*=58，提交 (32,21) 的候选色差计算。
4. 10:25 核对拟合均值与 95% 区间后签认。发现 (60,45) 落在内保留区，领位被拒。
5. 11:05 使用已签认的 (32,21) 领取试色位，重复请求被阻止。
6. 13:10 点测 ΔE76 为 3.9，试色转到待复样。复测 1.52 后完成签收 PROOF-QA11。
7. 14:00 记录边界第 2 版，先前拟合任务的边界版本不再可用于新签认。

## 启动

```sh
cp .env.example .env
docker compose up -d --build --wait
docker compose exec -T backend python -m scripts.seed_demo
```

打开 `http://127.0.0.1:18313`。FastAPI OpenAPI 在 `http://127.0.0.1:19313/docs`。
Compose 运行 Nginx、Python FastAPI、独立 Redis 消费进程、SQL 数据库和 Redis，SQL 与 Redis 使用命名卷。
本机开发时，在 Python 3.11 环境安装 `backend/requirements.txt` 后从 backend 目录运行 `uvicorn core.app:app`。须提供 `DATABASE_URL`、`REDIS_URL`、`JWT_SECRET`，`SEED_DEMO` 控制演示初始化。

| 演示账号 | 权限 |
|---|---|
| operator@demo.test | 提交领域记录和计算请求 |
| reviewer@demo.test | 提交记录并执行有业务约束的复核操作 |
| viewer@demo.test | 浏览业务台账 |

三个本地演示账号均使用 `DemoC0de!2026`。角色在 `backend/core/roles.py` 和 `frontend/src/store.js` 中声明。计算状态在 worker、queueing、API 和同一前端 store 中使用。

## 页面与接口

| 业务任务 | FastAPI 路由 | 页面 |
|---|---|---|
| 复制样张边界 | `/proof_regions` /proof_regions/revise-mask | `frontend/src/pages/proof_regions.js` |
| 干样点测色样 | `/dry_swatches` /dry_swatches/record-swatch，/dry_swatches/witness-swatch | `frontend/src/pages/dry_swatches.js` |
| 色差区间签认 | `/shade_studies` /shade_studies/fit-at-point，/shade_studies/confirm-color | `frontend/src/pages/shade_studies.js` |
| 试色位及试色回执 | `/patch_slots` /patch_slots/reserve-patch，/patch_slots/consume-patch | `frontend/src/pages/patch_slots.js` |

SQL 实体与约束在 `backend/domain` 下维护。前端使用原生 ES modules。核心算子为 GaussianProcessRegressor。两输入为色料比例与归一后的底色 L*，Matérn 3/2 核和白噪声核，固定参数和种子 1089。每五个干样按比例等顺序留一，报告验证 MAE，再用全样本搜索 41 格并以均值+0.8σ排序。区间为模型正态预测区间，负下界截到 0。

所有样张都是模拟翻印件，坐标原点在左上角；此流程限定在纸面复制件。色差区间依赖固定核参数和合成数据，业务阈值用于演练。保留区为矩形，未内置扫描图像辨色或实物采集。

[MIT](LICENSE)
