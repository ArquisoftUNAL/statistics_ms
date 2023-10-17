freq_types: dict[str, int] = {
    "daily": 1,
    "daily2": 2,
    "weekly": 3,
    "weekly2": 4,
    "monthly": 5,
    "monthly2": 6,
}

freq_types_inv: dict[int, str] = {
    1: "daily",
    2: "daily2",
    3: "weekly",
    4: "weekly2",
    5: "monthly",
    6: "monthly2",
}

freq_streaks: dict[int, int] = {
    1: 1, # daily
    2: 2, # daily2
    3: 7, # weekly
    4: 14, # weekly2
    5: 30, # monthly
    6: 60, # monthly2
}