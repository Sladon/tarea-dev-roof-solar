import json
from typing import Dict, List


def calculate_fitted_area_with_remainder(
    a_width: int, a_height: int, e_width: int, e_height: int
):
    """
    Given an area of certain width and height, and an element area of certain width and height, determine the area that contains most of the panels.

    Parameters:
        a_width  [int]: width of the main area
        a_height [int]: height of the main area
        e_width  [int]: width of the element
        e_height [int]: height of the element

    Returns:
        int: width of area that contains most panels
        int: height of area that contains most panels
        int: remaining right width, not used
        int: remaining bottom height, not used
    """

    if not a_width or not a_height or not e_width or not e_height:
        return 0, 0, 0, 0

    min_e, max_e = (e_width, e_height) if e_width < e_height else (e_height, e_width)
    min_a, max_a = (a_width, a_height) if a_width < a_height else (a_height, a_width)

    if max_e > max_a or min_e > min_a:
        return 0, 0, 0, 0

    elem_in_width, elem_in_height = (a_width // e_width, a_height // e_height)
    if not elem_in_width or not elem_in_height:
        return 0, 0, a_width, a_height

    main_width, main_height = (elem_in_width * e_width, elem_in_height * e_height)
    remaining_width, remaining_height = (a_width - main_width, a_height - main_height)

    return (
        main_width,
        main_height,
        remaining_width,
        remaining_height,
    )


def get_panels_inside_rectangle(
    panel_width: int, panel_height: int, roof_width: int, roof_height: int
):
    if not panel_width or not panel_height:
        return 0

    def get_panel_dimensions(rotate: bool = False) -> tuple[int, int]:
        if rotate:
            return panel_height, panel_width
        return panel_width, panel_height

    w, h, rw, rh = calculate_fitted_area_with_remainder(
        roof_width, roof_height, *get_panel_dimensions()
    )
    main_panels = (w // panel_width) * (h // panel_height)

    is_panel_horizontal = panel_width > panel_height

    # If panel is originally horizontal, next panels can be placed at the right empty space verically,
    # otherwise the can be placed horizontally in the remaining bottom space
    if is_panel_horizontal:
        extra_w, extra_h, _, _ = calculate_fitted_area_with_remainder(
            rw, roof_height, *get_panel_dimensions(True)
        )
    else:
        extra_w, extra_h, _, _ = calculate_fitted_area_with_remainder(
            roof_width, rh, *get_panel_dimensions(True)
        )

    extra_panels = (extra_w // panel_height) * (extra_h // panel_width)
    total = main_panels + extra_panels
    return total


def calculate_panels(
    panel_width: int, panel_height: int, roof_width: int, roof_height: int
) -> int:
    return max(
        get_panels_inside_rectangle(panel_width, panel_height, roof_width, roof_height),
        get_panels_inside_rectangle(
            panel_height,  # Rotate panels 90° degrees
            panel_width,  # Rotate panels 90° degrees
            roof_width,
            roof_height,
        ),
    )


def get_overlapping_roofs_panels(
    panel_width: int,
    panel_height: int,
    roof_width: int,
    roof_height: int,
    roof_width_transform: int,
    roof_height_transform: int,
) -> int:
    """
    Calculates the panels in a overlapping roof of 2 equal rectangles overlaping

    Parameters:
        panel_width [int]
        panel_height [int]
        roof_width [int]
        roof_height[int]
        roof_width_transform [int]: Moves the second rectangle away from the first one, starts in same width.
        roof_height_transform [int]: Moves the second rectangle away from the first one, starts in same height.
    Returns:
        Number of panels
    """
    width_diff = abs(roof_width_transform)
    height_diff = abs(roof_height_transform)
    if (
        width_diff > roof_width
        or width_diff < 1
        or height_diff > roof_height
        or height_diff < 1
    ):
        return 0

    rect_13 = (roof_width, roof_height - height_diff)
    rect_2 = (
        roof_width + width_diff,
        height_diff,
    )

    w_13, h_13, rw_13, rh_13 = calculate_fitted_area_with_remainder(
        rect_13[0], rect_13[1], panel_width, panel_height
    )
    rect_13_rotated = w_13 + rw_13 != rect_13[0]

    w_2, h_2, rw_2, rh_2 = calculate_fitted_area_with_remainder(
        rect_2[0], rect_2[1], panel_width, panel_height
    )
    rect_2_rotated = w_2 + rw_2 != rect_2[0]

    rect_13_panels = 2 * calculate_panels(
        panel_width, panel_height, rect_13[0], rect_13[1]
    )
    rect_2_panels = calculate_panels(panel_width, panel_height, rect_2[0], rect_2[1])
    total_panels_1 = rect_13_panels + rect_2_panels

    rect_46 = (width_diff, roof_height)  # diff, height
    rect_5 = (roof_width - width_diff, roof_height + height_diff)
    rect_46_panels = 2 * calculate_panels(
        panel_width, panel_height, rect_46[0], rect_46[1]
    )
    rect_5_panels = calculate_panels(panel_width, panel_height, rect_5[0], rect_5[1])
    total_panels_2 = rect_46_panels + rect_5_panels

    return max(total_panels_1, total_panels_2)


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
    print(get_overlapping_roofs_panels(3, 2, 12, 8, 5, 3))


if __name__ == "__main__":
    main()
