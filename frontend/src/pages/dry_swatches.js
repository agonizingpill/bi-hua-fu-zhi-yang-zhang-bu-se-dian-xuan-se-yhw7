        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "色样册干样点测",
  "module": "干样点测色样",
  "caption": "干样点测色样",
  "detail": "同底色不同配比的干样记录供回归估计。静置时间和凭证经二次复核后方能参与计算。",
  "path": "/dry_swatches",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "family",
      "label": "色样册"
    },
    {
      "name": "fraction",
      "label": "调色比例"
    },
    {
      "name": "ground_l",
      "label": "底样 Lab 亮度"
    },
    {
      "name": "delta_e",
      "label": "干样与复制参考 ΔE76"
    },
    {
      "name": "sample_ref",
      "label": "点测凭证"
    },
    {
      "name": "dry_hours",
      "label": "静置小时"
    },
    {
      "name": "witnessed",
      "label": "已验真"
    }
  ],
  "layout": "stack",
  "view": "table",
  "actions": [
    {
      "name": "record_swatch",
      "label": "登记干样点测",
      "path": "/dry_swatches/record-swatch",
      "fields": [
        {
          "name": "code",
          "label": "干样编号",
          "kind": "text",
          "initial": "SWATCH-QA"
        },
        {
          "name": "family",
          "label": "色样册",
          "kind": "text",
          "initial": "SAND-BATCH"
        },
        {
          "name": "fraction",
          "label": "调色比例",
          "kind": "float",
          "initial": 0.51
        },
        {
          "name": "ground_l",
          "label": "底样亮度 Lab L*",
          "kind": "float",
          "initial": 58.2
        },
        {
          "name": "delta_e",
          "label": "ΔE76",
          "kind": "float",
          "initial": 1.44
        },
        {
          "name": "sample_ref",
          "label": "点测凭证",
          "kind": "text",
          "initial": "COLOR-QA"
        },
        {
          "name": "dry_hours",
          "label": "静置小时",
          "kind": "int",
          "initial": 26
        }
      ],
      "help": "录入与复制参考片比较的已测 ΔE76。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "witness_swatch",
      "label": "验真干样点测",
      "path": "/dry_swatches/witness-swatch",
      "fields": [
        {
          "name": "chip",
          "label": "干样编号",
          "kind": "text",
          "initial": "SWATCH-QA"
        }
      ],
      "help": "只有静置满一天且有凭证的数据可进入试色建议。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "dry_swatches";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
