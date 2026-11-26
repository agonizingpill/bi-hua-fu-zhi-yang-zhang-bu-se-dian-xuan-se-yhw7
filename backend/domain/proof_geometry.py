from core.records import need


def validate_mask(region):
    margin = region["frame_inset"]
    width, height = region["width_mm"], region["height_mm"]
    need(0 <= margin < min(width, height) / 2, "保护留边超过样张尺寸")
    need(
        margin <= region["hold_x1"] < region["hold_x2"] <= width - margin
        and margin <= region["hold_y1"] < region["hold_y2"] <= height - margin,
        "留白矩形超出保护留边范围",
    )


def demand_point(panel, x, y):
    margin = panel["frame_inset"]
    need(
        margin <= x < panel["width_mm"] - margin and margin <= y < panel["height_mm"] - margin,
        "此坐标超出保护留边可试色范围",
    )
    inside_mask = (
        panel["hold_x1"] <= x <= panel["hold_x2"] and panel["hold_y1"] <= y <= panel["hold_y2"]
    )
    need(not inside_mask, "此坐标落在内保留区，禁止占用试色位")
