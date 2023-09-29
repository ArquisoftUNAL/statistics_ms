GET_HAB_QUERY = """
SELECT hab_is_yn, hab_freq_type, hab_goal
FROM habit 
WHERE hab_id = :hab_id
"""

GET_HABIT_DATA_QUERY = """
SELECT hab_dat_amount, hab_dat_collected_at
FROM habit_data_collected
WHERE hab_id = :hab_id
ORDER BY hab_dat_collected_at DESC
"""