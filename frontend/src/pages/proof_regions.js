        import {workspace} from '../workspace.js';
        import {proofMap} from '../proof-map.js';

        const page = {
  "title": "复制样张可试色边界",
  "module": "复制样张边界",
  "caption": "复制样张边界",
  "detail": "按照实体翻印样张绘出外围保护带和内保留区。边界每次修订递增版次，已领取的试色位也需复核。",
  "path": "/proof_regions",
  "columns": [
    {
      "name": "code",
      "label": "编号"
    },
    {
      "name": "label",
      "label": "样张区域"
    },
    {
      "name": "pigment_family",
      "label": "色样册"
    },
    {
      "name": "width_mm",
      "label": "样张宽 mm"
    },
    {
      "name": "height_mm",
      "label": "样张高 mm"
    },
    {
      "name": "frame_inset",
      "label": "保护留边 mm"
    },
    {
      "name": "hold_x1",
      "label": "留白起 X"
    },
    {
      "name": "hold_y1",
      "label": "留白起 Y"
    },
    {
      "name": "hold_x2",
      "label": "留白止 X"
    },
    {
      "name": "hold_y2",
      "label": "留白止 Y"
    },
    {
      "name": "revision",
      "label": "边界版次"
    }
  ],
  "layout": "split",
  "view": "grid",
  "actions": [
    {
      "name": "revise_mask",
      "label": "签入保护边界修订",
      "path": "/proof_regions/revise-mask",
      "fields": [
        {
          "name": "panel",
          "label": "样张编号",
          "kind": "text",
          "initial": "PANEL-W8"
        },
        {
          "name": "frame_inset",
          "label": "保护留边 mm",
          "kind": "int",
          "initial": 8
        },
        {
          "name": "hold_x1",
          "label": "留白起 X",
          "kind": "int",
          "initial": 44
        },
        {
          "name": "hold_y1",
          "label": "留白起 Y",
          "kind": "int",
          "initial": 30
        },
        {
          "name": "hold_x2",
          "label": "留白止 X",
          "kind": "int",
          "initial": 70
        },
        {
          "name": "hold_y2",
          "label": "留白止 Y",
          "kind": "int",
          "initial": 54
        }
      ],
      "help": "保留区和外围留边均采用样张毫米坐标。",
      "roles": [
        "reviewer"
      ],
      "success": "已写入"
    }
  ]
};

        export const {title} = page;
        export const key = "proof_regions";
        export async function render(root, role) {
          await workspace(root, role, page);
          await proofMap(root);

        }
