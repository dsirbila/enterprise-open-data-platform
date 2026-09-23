"""lecture 6 (დამატება): Slowly Changing Dimension (SCD) Type 2 — testable ლოგიკა."""

def scd2_upsert(existing_rows: list, new_version: dict, key_field: str, tracked_fields: list, effective_date: str) -> list:
    key_value = new_version[key_field]
    current_row = next(
        (r for r in existing_rows if r[key_field] == key_value and r.get("is_current")), None
    )

    if current_row is None:
        new_row = {**new_version, "valid_from": effective_date, "valid_to": None, "is_current": True}
        return existing_rows + [new_row]

    changed = any(current_row.get(f) != new_version.get(f) for f in tracked_fields)
    if not changed:
        return existing_rows

    updated_rows = [
        {**r, "valid_to": effective_date, "is_current": False} if r is current_row else r
        for r in existing_rows
    ]
    new_row = {**new_version, "valid_from": effective_date, "valid_to": None, "is_current": True}
    return updated_rows + [new_row]

if __name__ == "__main__":
    # Test 1: პირველი ვერსიის დამატება
    db = []
    db = scd2_upsert(db, {'city': 'Tbilisi', 'population_category': 'medium'}, 'city', ['population_category'], '2026-01-01')
    assert len(db) == 1 and db[0]['is_current'] is True, "Test 1 failed"
    print("Test 1 passed:", db[0])

    # Test 2: ცვლილების გარეშე (არაფერი უნდა შეიცვალოს)
    db = scd2_upsert(db, {'city': 'Tbilisi', 'population_category': 'medium'}, 'city', ['population_category'], '2026-05-01')
    assert len(db) == 1, "Test 2 failed"
    print("Test 2 passed: row-ების რაოდენობა უცვლელია — ცვლილება არ დაფიქსირდა")

    # Test 3: რეალური ცვლილება (ძველი იხურება, ახალი ემატება)
    db = scd2_upsert(db, {'city': 'Tbilisi', 'population_category': 'large'}, 'city', ['population_category'], '2026-09-01')
    assert len(db) == 2, "Test 3 failed"
    print("Test 3 passed:")
    for row in db:
        print("  ", row)

    print("\n[OK] ყველა 3 სცენარი (პირველი ჩანაწერი, ცვლილების გარეშე, რეალური ცვლილება) სწორად მუშაობს")
