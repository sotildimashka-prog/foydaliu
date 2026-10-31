from dataclasses import dataclass


@dataclass(frozen=True)
class City:
    key: str
    name: str
    lat: float
    lon: float


CITIES: dict[str, City] = {
    c.key: c
    for c in (
        City("tashkent", "Toshkent", 41.2995, 69.2401),
        City("samarkand", "Samarqand", 39.6542, 66.9597),
        City("bukhara", "Buxoro", 39.7681, 64.4556),
        City("andijan", "Andijon", 40.7821, 72.3442),
        City("fergana", "Farg'ona", 40.3842, 71.7843),
        City("namangan", "Namangan", 40.9983, 71.6726),
        City("karshi", "Qarshi", 38.8606, 65.7891),
        City("nukus", "Nukus", 42.4531, 59.6103),
        City("urgench", "Urganch", 41.5500, 60.6333),
        City("jizzakh", "Jizzax", 40.1158, 67.8422),
        City("termez", "Termiz", 37.2242, 67.2783),
        City("navoi", "Navoiy", 40.0844, 65.3792),
        City("gulistan", "Guliston", 40.4897, 68.7842),
    )
}
