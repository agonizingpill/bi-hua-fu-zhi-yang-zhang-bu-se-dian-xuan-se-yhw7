        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "Gaussian Process 色差与区间",
  "module": "色差区间签认",
  "caption": "色差区间签认",
  "detail": "以底样亮度和试色比例估计复制样张色差。模型返回候选均值与区间，审核签认后方可占用试色位。",
  "path": "/shade_studies",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "panel",
      "label": "样张"
    },
    {
      "name": "revision",
      "label": "连续边界版次"
    },
    {
      "name": "x_mm",
      "label": "补色点 X"
    },
    {
      "name": "y_mm",
      "label": "补色点 Y"
    },
    {
      "name": "ground_l",
      "label": "样张底色亮度"
    },
    {
      "name": "fraction",
      "label": "建议调色比例"
    },
    {
      "name": "mean_de",
      "label": "预测 ΔE76"
    },
    {
      "name": "lower_de",
      "label": "95% 区间下端"
    },
    {
      "name": "upper_de",
      "label": "95% 区间上端"
    },
    {
      "name": "test_mae",
      "label": "留出格 MAE"
    },
    {
      "name": "token",
      "label": "拟合凭证"
    }
  ],
  "layout": "flip",
  "view": "grid",
  "actions": [
    {
      "name": "fit_at_point",
      "label": "计算指定点试色建议",
      "path": "/shade_studies/fit-at-point",
      "fields": [
        {
          "name": "panel",
          "label": "样张编号",
          "kind": "text",
          "initial": "PANEL-W8"
        },
        {
          "name": "x_mm",
          "label": "补色点 X",
          "kind": "int",
          "initial": 32
        },
        {
          "name": "y_mm",
          "label": "补色点 Y",
          "kind": "int",
          "initial": 21
        },
        {
          "name": "ground_l",
          "label": "点位底色 Lab L*",
          "kind": "float",
          "initial": 58
        }
      ],
      "help": "量化不确定性，候选在干样配比范围内搜索。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "confirm_color",
      "label": "签认拟合与不确定区间",
      "path": "/shade_studies/confirm-color",
      "fields": [
        {
          "name": "code",
          "label": "签认簿号",
          "kind": "text",
          "initial": "COLOR-QA"
        },
        {
          "name": "token",
          "label": "拟合凭证",
          "kind": "token",
          "initial": ""
        }
      ],
      "help": "固化当次训练区间、点位坐标和样张边界修订号。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "shade_studies";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
