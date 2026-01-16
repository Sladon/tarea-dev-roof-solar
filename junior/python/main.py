import json
from typing import Dict, List


def get_min_max(*args):
    min_val = min(args)
    max_val = max(args)
    return min_val, max_val


def get_amount(
    area_x_size: int,
    area_y_size: int,
    element_x_size: int,
    element_y_size: int,
    rotate: bool = False,
):
    if rotate:
        x_size = element_y_size
        y_size = element_x_size
    else:
        x_size = element_x_size
        y_size = element_y_size

    def area_axis_elements(x_space: int, y_space: int):
        return (x_space // x_size), (y_space // y_size)

    x_amount, y_amount = area_axis_elements(area_x_size, area_y_size)
    main_amount = x_amount * y_amount

    used_x_space = x_amount * x_size
    remaining_x_space = area_x_size - used_x_space
    remaining_y_space = area_y_size - (y_amount * y_size)

    right_x_amount, right_y_amount = area_axis_elements(area_y_size, remaining_x_space)
    right_amount = right_x_amount * right_y_amount

    bottom_x_amount, bottom_y_amount = area_axis_elements(
        remaining_y_space, used_x_space
    )
    bottom_amount = bottom_x_amount * bottom_y_amount

    return main_amount + right_amount + bottom_amount


def calculate_panels(
    panel_width: int, panel_height: int, roof_width: int, roof_height: int
) -> int:
    x_roof, y_roof = get_min_max(roof_width, roof_height)
    x_panel, y_panel = get_min_max(panel_width, panel_height)

    if y_panel > y_roof or x_panel > x_roof:
        return 0

    can_rotate = y_panel <= x_roof
    x_amount = x_roof // x_panel

    if not can_rotate:
        return x_amount

    rotated_amount = get_amount(x_roof, y_roof, x_panel, y_panel, True)
    not_rotated_amount = get_amount(x_roof, y_roof, x_panel, y_panel)

    return max(rotated_amount, not_rotated_amount)


def run_tests() -> None:
    with open("test_cases.json", "r") as f:
        data = json.load(f)
        test_cases: List[Dict[str, int]] = [
            {
                "panel_w": test["panelW"],
                "panel_h": test["panelH"],
                "roof_w": test["roofW"],
                "roof_h": test["roofH"],
                "expected": test["expected"],
            }
            for test in data["testCases"]
        ]

    print("Corriendo tests:")
    print("-------------------")

    for i, test in enumerate(test_cases, 1):
        result = calculate_panels(
            test["panel_w"], test["panel_h"], test["roof_w"], test["roof_h"]
        )
        passed = result == test["expected"]

        print(f"Test {i}:")
        print(
            f"  Panels: {test['panel_w']}x{test['panel_h']}, "
            f"Roof: {test['roof_w']}x{test['roof_h']}"
        )
        print(f"  Expected: {test['expected']}, Got: {result}")
        print(f"  Status: {'✅ PASSED' if passed else '❌ FAILED'}\n")


def main() -> None:
    print("🐕 Wuuf wuuf wuuf 🐕")
    print("================================\n")

    run_tests()


if __name__ == "__main__":
    main()
