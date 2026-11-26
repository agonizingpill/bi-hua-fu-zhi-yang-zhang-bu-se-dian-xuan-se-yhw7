import {workspace} from '../workspace.js';

const page = {
  "title": "整碗配色与整组领位",
  "module": "整碗颜料工作台",
  "caption": "整碗颜料工作台",
  "detail": "一碗颜料补样张上多个点：先排除任一点预测区间过宽的比例，再选最差点色差上界最低的一档。整组签认后一起领位，任一点已被领则全组退回；同一请求键重试取回原组。",
  "path": "/color_bowls",
  "columns": [
    {"name": "code", "label": "整碗编号"},
    {"name": "panel", "label": "样张"},
    {"name": "revision", "label": "签认边界版次"},
    {"name": "fraction", "label": "共用调色比例"},
    {"name": "mean_de", "label": "组内平均 ΔE76"},
    {"name": "lower_de", "label": "最宽区间下端"},
    {"name": "upper_de", "label": "最宽区间上端"},
    {"name": "max_upper_de", "label": "最差点色差上界"},
    {"name": "test_mae", "label": "留出格 MAE"},
    {"name": "points", "label": "整组点（坐标/底色/逐点区间）"},
    {"name": "token", "label": "试算凭证"}
  ],
  "layout": "flip",
  "view": "grid",
  "actions": [
    {
      "name": "fit_bowl",
      "label": "整碗试算（多点选一档比例）",
      "path": "/color_bowls/fit-bowl",
      "fields": [
        {"name": "panel", "label": "样张编号", "kind": "text", "initial": "PANEL-W8"},
        {"name": "points", "label": "整组点 JSON（x_mm/y_mm/ground_l）", "kind": "json",
         "initial": [
           {"x_mm": 32, "y_mm": 21, "ground_l": 58},
           {"x_mm": 40, "y_mm": 22, "ground_l": 58},
           {"x_mm": 50, "y_mm": 26, "ground_l": 58}
         ]}
      ],
      "help": "逐点预测后先剔除任一点区间宽度 > 3.0 的比例，再取最差点上界最低的一档；全组共用该比例。",
      "roles": ["operator", "reviewer"],
      "success": "试算已完成"
    },
    {
      "name": "confirm_bowl",
      "label": "整组签认",
      "path": "/color_bowls/confirm-bowl",
      "fields": [
        {"name": "code", "label": "整碗编号", "kind": "text", "initial": "BOWL-QA1"},
        {"name": "token", "label": "试算凭证", "kind": "token", "initial": ""}
      ],
      "help": "固化共用比例、逐点区间与边界版次，并为每个点生成签认簿。",
      "roles": ["reviewer"],
      "success": "整组已签认"
    },
    {
      "name": "reserve_bowl",
      "label": "整组领取试色位",
      "path": "/color_bowls/reserve-bowl",
      "fields": [
        {"name": "bowl", "label": "整碗编号", "kind": "text", "initial": "BOWL-QA1"},
        {"name": "claim_key", "label": "领位请求键（重试保持不变）", "kind": "text", "initial": "CLAIM-001"},
        {"name": "reader", "label": "试色位责任人", "kind": "text", "initial": "季桥"}
      ],
      "help": "整组原子领位：任一点已被领则全组退回；同一请求键重复提交只取回原组，不重复占位。",
      "roles": ["operator", "reviewer"],
      "success": "整组已领取"
    }
  ]
};

export const {title} = page;
export const key = "color_bowls";
export async function render(root, role) {
  await workspace(root, role, page);
}
