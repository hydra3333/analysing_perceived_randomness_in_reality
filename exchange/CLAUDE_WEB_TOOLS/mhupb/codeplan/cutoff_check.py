"""OV-1's cut-off (supplement v0.8 section 6.8): 01:30 UTC on the draw date, checked against Adelaide's clock.
Plan-stage check only (it uses the system's time-zone data; the planned code uses none). Usage: python3 -I cutoff_check.py"""
import datetime as d
import zoneinfo

z = zoneinfo.ZoneInfo('Australia/Adelaide')
n = bad = 0
hours = {}
day = d.date(2026, 11, 17)
while day < d.date(2046, 1, 1):
    if day.weekday() in (1, 3):                       # Tuesday (Oz Lotto), Thursday (Powerball)
        cut = d.datetime(day.year, day.month, day.day, 1, 30, tzinfo=d.timezone.utc)
        local = cut.astimezone(z)
        midnight = d.datetime(day.year, day.month, day.day, 0, 0, tzinfo=z)
        noon = d.datetime(day.year, day.month, day.day, 12, 0, tzinfo=z)
        close = d.datetime(day.year, day.month, day.day, 9, 30, tzinfo=d.timezone.utc)      # 7.30pm AEST (UTC+10)
        ok = (local.date() == day and local.minute == 0 and local.hour in (11, 12) and cut <= noon
              and cut - midnight in (d.timedelta(hours=11), d.timedelta(hours=12)) and close - cut == d.timedelta(hours=8))
        hours[local.hour] = hours.get(local.hour, 0) + 1
        n += 1
        bad += not ok
    day += d.timedelta(days=1)
print(f'Tuesdays and Thursdays from 2026-11-17 to 2045-12-31: {n} checked, {bad} failures')
print(f'local Adelaide time of the cut-off: {sorted(hours.items())} (hour: number of draw dates)')
print('each is on the draw date, never after 12:00 Adelaide, 11 or 12 hours after local midnight, 8 hours before 09:30 UTC')
