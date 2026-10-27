"""lecture 20: Custom partitioning სტრატეგია — გეოგრაფიული მდებარეობით, event_id-ის მაგივრად, რომ ერთი რეგიონის ყველა მოვლენა ერთ partition-ში მოხვდეს."""
GEORGIA_REGIONS = {
    "west": (41.0, 43.6, 40.0, 43.0),   # დასავლეთი (Batumi/Kutaisi მხარე)
    "east": (41.0, 43.6, 43.0, 46.7),   # აღმოსავლეთი (Tbilisi/Telavi მხარე)
}

def get_partition_key(latitude: float, longitude: float) -> str:
    """
    კოორდინატებს ერთ-ერთ coarse რეგიონს (west/east) მიაკუთვნებს — ეს string
    გამოიყენება Kafka-ს `key`-დ, რომ ერთი რეგიონის events ერთსა და იმავე
    partition-ში 'დაჯგუფდეს'.
    """
    for region, (min_lat, max_lat, min_lon, max_lon) in GEORGIA_REGIONS.items():
        if min_lat <= latitude <= max_lat and min_lon <= longitude <= max_lon:
            return region
    return "unknown"
