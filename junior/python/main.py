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


def get_sub_rectangles_inside_rectangle(
    sub_rect_width: int, sub_rect_height: int, rect_width: int, rect_height: int
) -> tuple[int, tuple[int, int], tuple[int, int], tuple[int, int]]:
    """
    Calculates the amount of sub rectangles that can be placed inside the main rectangle area, it rotates the sub rectangles to check which direction is the best, and also fills the extra area with sub rectangles in the other direction.

    Parameters:
        sub_rect_width [int]
        sub_rect_height [int]
        rect_width [int]
        rect_height [int]

    Returns:
        int: The number of sub rectangles that could be placed inside the main rectangle.
        tuple[int, int]: Unused space at the right, represented as (width, height).
        tuple[int, int]: Unused space at the bottom, represented as (width, height).
        tuple[int, int]: Unused space at right bottom corner, represented as (width, height).
    """
    total, leftover_r_top_to_bottom, leftover_b_left_to_right, overlap_area = (
        0,
        (0, 0),
        (0, 0),
        (0, 0),
    )

    if not sub_rect_width or not sub_rect_height:
        return total, leftover_r_top_to_bottom, leftover_b_left_to_right, overlap_area

    def get_panel_dimensions(rotate: bool = False) -> tuple[int, int]:
        if rotate:
            return sub_rect_height, sub_rect_width
        return sub_rect_width, sub_rect_height

    for rotate_panel in [False, True]:
        sub_rect_w, sub_rect_h = get_panel_dimensions(rotate_panel)
        w, h, rw, rh = calculate_fitted_area_with_remainder(
            rect_width, rect_height, *get_panel_dimensions(rotate_panel)
        )
        main_panels = (w // sub_rect_w) * (h // sub_rect_h)

        is_panel_horizontal = sub_rect_w > sub_rect_h

        # If panel is originally horizontal, next panels can be placed at the right empty space verically,
        # otherwise the can be placed horizontally in the remaining bottom space
        check_width, check_height = (
            (rw, rect_height) if is_panel_horizontal else (rect_width, rh)
        )

        extra_w, extra_h, extra_rw, extra_rh = calculate_fitted_area_with_remainder(
            check_width, check_height, *get_panel_dimensions(not rotate_panel)
        )

        extra_panels = (extra_w // sub_rect_h) * (extra_h // sub_rect_w)

        total_panels = main_panels + extra_panels
        if total_panels < total:
            continue

        total = total_panels
        leftover_r_top_to_bottom = (
            (rw, rect_height - rh)
            if not is_panel_horizontal
            else (extra_rw, rect_height - extra_rh)
        )

        leftover_b_left_to_right = (
            (rect_width - extra_rw, extra_rh)
            if not is_panel_horizontal
            else (rect_width - rw, rh)
        )

        overlap_area = (extra_rw, rh) if not is_panel_horizontal else (rw, extra_rh)

    return total, leftover_r_top_to_bottom, leftover_b_left_to_right, overlap_area


def calculate_panels(
    panel_width: int, panel_height: int, roof_width: int, roof_height: int
) -> int:
    return get_sub_rectangles_inside_rectangle(
        panel_width, panel_height, roof_width, roof_height
    )[0]


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

    def get_panels(width, height):
        return get_sub_rectangles_inside_rectangle(
            panel_width, panel_height, width, height
        )

    rect_13 = get_panels(roof_width, roof_height - height_diff)

    rect_2 = get_panels(
        roof_width + width_diff,
        height_diff,
    )

    rect_46 = get_panels(width_diff, roof_height)  # diff, height
    rect_5 = get_panels(roof_width - width_diff, roof_height + height_diff)

    return max(rect_13[0] * 2 + rect_2[0], rect_46[0] * 2 + rect_5[0])


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
