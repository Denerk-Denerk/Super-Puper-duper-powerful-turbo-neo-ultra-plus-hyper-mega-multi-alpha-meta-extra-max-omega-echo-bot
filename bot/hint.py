
"""
    if not args:
        stats = read_csv_file(fname=settings.STATS_FILE, fields=["user_name", "count"])
        msg = "\n".join([f"{row.get("user_name")}: {row.get("count")}" for row in stats])
        await message.answer(msg)
        return


    def update_stats(message):
    user_name = message.from_user.first_name
    stats = read_csv_file(fname=STATS_FILE, fields=["user_name", "count", "last_msg_id"])
    user_has_stats = False

    data = {}
    for row in stats:
        if row.get("user_name") == user_name:
            row["count"] = int(row["count"]) + 1
            row["last_msg_id"] = str(message.message_id)
            user_has_stats = True

    if not user_has_stats:
        data.update(
            {
                "user_name": user_name,
                "count": 1,
                "last_msg_id": message.message_id,
            }
        )

    write_to_csv_file(fname=STATS_FILE, data=data, mode='w')

"""