from datetime import date, timedelta

def calculate_streaks(dates: list) -> dict:

    if not dates:
        return {'current_streak': 0, 'longest_streak': 0}

    sorted_dates = sorted(set(dates))

    longest = current = 1

    today = date.today()

    for i in range(1, len(sorted_dates)):
        diff = (sorted_dates[i] - sorted_dates[i - 1]).days

        if diff == 1:
            current += 1
            longest = max(longest, current)
        elif diff > 1:
            current = 1

    last = sorted_dates[-1]
    if last < today - timedelta(days=1):
        current = 0

    return {'current_streak': current, 'longest_streak': longest}            





