import math


def validate_paginated_response(
        response_data: dict,
        page: int,
        size: int,
        total_items: int,
) -> None:
    total_pages = math.ceil(total_items / size)

    assert response_data["total"] == total_items
    assert response_data["page"] == page
    assert response_data["size"] == size
    assert response_data["pages"] == total_pages

    expected_count = total_items % size \
        if page == total_pages & total_items != size \
        else size

    assert len(response_data["items"]) == expected_count
