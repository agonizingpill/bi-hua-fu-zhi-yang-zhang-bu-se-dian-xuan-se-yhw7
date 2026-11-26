        import {workspace} from '../workspace.js';
        import {el} from '../dom.js';

        const page = {
  "title": "试色位领用与回执",
  "module": "试色位及试色回执",
  "caption": "试色位及试色回执",
  "detail": "预约坐标必须与签认点一致。落到保护留边或内保留区时记录保持不变。点测偏差过大则转待复样。",
  "path": "/patch_slots",
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
      "name": "study",
      "label": "签认簿"
    },
    {
      "name": "x_mm",
      "label": "坐标 X"
    },
    {
      "name": "y_mm",
      "label": "坐标 Y"
    },
    {
      "name": "site_key",
      "label": "样张坐标索引"
    },
    {
      "name": "reader",
      "label": "试色位责任人"
    },
    {
      "name": "delta_seen",
      "label": "点测 ΔE76"
    },
    {
      "name": "receipt",
      "label": "回执编号"
    },
    {
      "name": "state",
      "label": "试色状态"
    }
  ],
  "layout": "flip",
  "view": "table",
  "actions": [
    {
      "name": "reserve_patch",
      "label": "领取样张试色位",
      "path": "/patch_slots/reserve-patch",
      "fields": [
        {
          "name": "code",
          "label": "试色位号",
          "kind": "text",
          "initial": "SLOT-QA"
        },
        {
          "name": "study",
          "label": "签认簿号",
          "kind": "text",
          "initial": "COLOR-QA"
        },
        {
          "name": "x_mm",
          "label": "预约坐标 X",
          "kind": "int",
          "initial": 32
        },
        {
          "name": "y_mm",
          "label": "预约坐标 Y",
          "kind": "int",
          "initial": 21
        },
        {
          "name": "reader",
          "label": "点测员",
          "kind": "text",
          "initial": "季桥"
        }
      ],
      "help": "已使用或其他人员占用的坐标不会重复发出。",
      "roles": [
        "operator",
        "reviewer"
      ],
      "success": "已写入"
    },
    {
      "name": "consume_patch",
      "label": "验收试色回执",
      "path": "/patch_slots/consume-patch",
      "fields": [
        {
          "name": "slot",
          "label": "试色位号",
          "kind": "text",
          "initial": "SLOT-QA"
        },
        {
          "name": "receipt",
          "label": "回执编号",
          "kind": "text",
          "initial": "PROOF-QA11"
        },
        {
          "name": "observed_de",
          "label": "再次测得 ΔE76",
          "kind": "float",
          "initial": 1.52
        }
      ],
      "help": "报告值超过区间上界与 0.5 的复样余量时保留该试色位并要求复样。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "patch_slots";
        export async function render(root, role) {
          await workspace(root, role, page);

        }
