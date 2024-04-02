import math
from datetime import date

class YourCalendarLib:
    def __init__(self, year, month, day):
        try:
            if not isinstance(year, int):
                raise ValueError('Only integers are allowed for Year.')

            if len(str(year)) != 4:
                raise ValueError('The year should have 4 digits.')

            if year < 0:
                raise ValueError('Negative numbers for year are meaningless.')

            if not isinstance(month, int):
                raise ValueError('Only integers are allowed for Month.')

            if 12 < month < 1:
                raise ValueError('Month should be between 1 to 12.')

            if not isinstance(day, int):
                raise ValueError('Only integers are allowed for Day.')

            if 31 < day < 1:
                raise ValueError('Day should be between 1 to 31.')

            self.year = year
            self.month = month
            self.day = day
        except ValueError as err:
            print(f'{err}')


class jalali(YourCalendarLib):
    def jalali_to_gregorian(self):
        jalali_year = self.year
        jalali_month = self.month
        jalali_day = self.day
        diff = 79
        if jalali_month < 10:
            gregorian_year = jalali_year + 621
        elif jalali_month >= 10:
            gregorian_year = jalali_year + 622

        days_in_month_shamsi = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
        days_in_month_greg = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        r = jalali_year % 4
        if r == 1:
            days_in_month_shamsi[11] = 30
        if gregorian_year % 4 == 0:
            days_in_month_greg[1] = 29
        add = 0
        for j in range(self.month - 1):
            add = add + days_in_month_shamsi[j]
        total_days = add + jalali_day + diff

        if jalali_month > 9:
            total_days = total_days - 365

        for i in range(12):
            remain = total_days - days_in_month_greg[i]
            d = i
            total_days = remain
            if remain < days_in_month_greg[i]:
                break

        gregorian_day = remain + 1
        gregorian_month = d + 1

        return gregorian_year, gregorian_month + 1, gregorian_day - 1

    def jalali_to_hijri(self):
        dates = (self.year - 1) * 365.25
        if self.month > 6:
            dates += (self.month - 6 - 1) * 30 + 6 * 31
        else:
            dates += (self.month - 1) * 31
        dates += self.day - 119
        if dates <= 0:
            return "hijri calendar hadn't been started then"
        dates = math.floor(dates)
        hijri_year = dates // 354.367
        dates %= 354.375
        dates = math.floor(dates)
        hijri_month_days = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29]
        hijri_month = 0
        for i in range(0, 11):
            if hijri_month_days[i] <= dates:
                dates -= hijri_month_days[i]
            else:
                hijri_month = i + 1
                break
        hijri_day = 0
        if dates == 0:
            hijri_day = hijri_month_days[hijri_month - 1]
        else:
            hijri_day = dates
        return int(hijri_year + 1), int(hijri_month), int(hijri_day)

    def weekday(self):
        jy = self.year
        jm = self.month
        jd = self.day

        if jm < 3:
            jy -= 1
            jm += 12

        days = jd + ((jm + 1) * 31) // 12 + jy + jy // 4 + 6
        re = (days + 1) % 7

        jalali_week_days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        return jalali_week_days[re]

    def now():
        a, b, c = gregorian.now()
        jalali = gregorian(a, b, c)
        return jalali.gregorian_to_jalali()

    def elapsedtime(self):
        days = (self.year - 1) * 365.25
        days_in_year = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
        for i in range(self.month - 1):
            days += days_in_year[i]
        days += self.day

        a, b, c = jalali.now()
        jalali_now = jalali(a, b, c)
        days2 = (jalali_now.year - 1) * 365.25
        days_in_year = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
        for i in range(jalali_now.month - 1):
            days2 += days_in_year[i]
        days2 += jalali_now.day
        days = math.floor(days)
        days2 = math.floor(days2)
        diff_days = days2 - days
        if diff_days == 0:
            return 0, 0, 0
        diff_year = diff_days // 365
        diff_days %= 365
        jalali_month_days = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
        diff_month = 0
        last_days = 0
        for i in range(12):
            if jalali_month_days[i] <= diff_days:
                diff_days -= jalali_month_days[i]
            else:
                diff_month = i
                break
        last_days = diff_days

        return int(diff_year), int(diff_month), int(last_days)

class hijri(YourCalendarLib):
    def hijri_to_gregorian(self):
        days = (self.year - 1) * 354.375
        days += self.day
        hijri_month_days = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29]
        if self.month > 1:
            for i in range(0, self.month - 1):
                days += hijri_month_days[i]
        days += 227019.25
        days = math.floor(days)
        gregorian_year = days // 365.25
        days %= 365.25
        days = math.floor(days)
        gregorian_month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        gregorian_month = 0
        for i in range(0, 11):
            if gregorian_month_days[i] <= days:
                days -= gregorian_month_days[i]
            else:
                gregorian_month = i + 1
                break
        gregorian_day = 0
        if days == 0:
            gregorian_day = gregorian_month_days[gregorian_month - 1]
        else:
            gregorian_day = days
        return int(gregorian_year + 1), gregorian_month, gregorian_day

    def hijri_to_jalali(self):
        days = (self.year - 1) * 354.375
        days += self.day
        hijri_month_days = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29]
        if self.month > 1:
            for i in range(0, self.month - 1):
                days += hijri_month_days[i]
        days += 119
        days = math.floor(days)
        jalali_year = days // 365.25
        days %= 365.25
        days = math.floor(days)
        jalali_month_days = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
        jalali_month = 0
        for i in range(0, 11):
            if jalali_month_days[i] <= days:
                days -= jalali_month_days[i]
            else:
                jalali_month = i + 1
                break
        jalali_day = 0
        if days == 0:
            jalali_day = jalali_month_days[jalali_month - 1]
        else:
            jalali_day = days
        return int(jalali_year + 1), jalali_month, jalali_day


    def weekday(self):
        days = (self.year - 1) * 365.367
        hijri_month_days = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29]
        if self.month > 1:
            for i in range(0, self.month - 1):
                days += hijri_month_days[i]
        days += self.day
        days = math.floor(days)
        re = days % 7
        re -= 1
        hijri_week_days = ["Friday", "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
        return hijri_week_days[re]

    def now():
        a, b, c = gregorian.now()
        hijri = gregorian(a, b, c)
        return hijri.gregorian_to_hijri()

    def elapsedtime(self):
        days = (self.year - 1) * 354.367
        days += self.day
        hijri_month_days = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29]
        if self.month > 1:
            for i in range(0, self.month - 1):
                days += hijri_month_days[i]
        a, b, c = gregorian.now()
        hijri_date = gregorian(a, b, c)
        a, b, c = hijri_date.gregorian_to_hijri()
        hijri_now = hijri(a, b, c)
        days2 = (hijri_now.year - 1) * 354.367
        days2 += hijri_now.day
        hijri_month_days = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29]
        if hijri_now.month > 1:
            for i in range(0, self.month - 1):
                days2 += hijri_month_days[i]
        diff_days = math.floor(days2 - days)
        if diff_days == 0:
            return 0, 0, 0
        diff_year = diff_days // 354
        diff_days += (diff_year // 3)
        diff_days %= 354
        hijri_month_days = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29]
        diff_month = 0
        last_days = 0
        for i in range(0, 11):
            if hijri_month_days[i] <= diff_days:
                diff_days -= hijri_month_days[i]
            else:
                diff_month = i
                break

        last_days = diff_days
        return diff_year, diff_month, last_days

class gregorian(YourCalendarLib):
    def gregorian_to_hijri(self):
        dates = 0
        dates += (self.year - 1) * 365.25
        dates += self.day
        gregorian_month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if self.month > 1:
            for i in range(0, self.month - 1):
                dates += gregorian_month_days[i]
        dates -= 227019.25
        if dates < 1:
            return "hijri calendar hadn't been started then"
        dates = math.floor(dates)
        hijri_year = dates // 354.367
        dates %= 354.372
        hijri_month_days = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29]
        hijri_month = 0
        for i in range(0, 11):
            if hijri_month_days[i] <= dates:
                dates -= hijri_month_days[i]
            else:
                hijri_month = i + 1
                break
        hijri_day = 0
        if dates == 0:
            hijri_day = hijri_month_days[hijri_month - 1]
        else:
            hijri_day = dates
        return int(hijri_year + 1), int(hijri_month), int(hijri_day)

    def gregorian_to_jalali(self):
        days = (self.year - 1) * 365.25
        gregorian_month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if self.month > 1:
            for i in range(0, self.month - 2):
                days += gregorian_month_days[i]
        days += self.day
        days -= 226900.25 - 396
        days = math.floor(days)
        if days < 1:
            return "jalali calendar hadn't been started then"
        solar_year = days // 365.25
        days %= 365.25
        days = math.floor(days)
        solar_month_days = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]
        solar_month = 0
        for i in range(0, 11):
            if solar_month_days[i] <= days:
                days -= solar_month_days[i]
            else:
                solar_month = i + 1
                break
        solar_day = 0
        if days == 0:
            solar_day = solar_month_days[solar_month - 1]
        else:
            solar_day = days
        return int(solar_year), solar_month, solar_day

    def weekday(self):
        days = (self.year - 1) * 365.25
        gregorian_month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if self.month > 1:
            for i in range(0, self.month - 1):
                days += gregorian_month_days[i]
        days += self.day
        days = math.floor(days - 1)
        re = days % 7
        gregorian_week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        return gregorian_week_days[re]

    def now():
        time = date.today()
        strtime = time.strftime('%Y-%m-%d')
        ind = strtime.index("-")
        gregorian_year = int(strtime[:ind])
        strtime = strtime[ind + 1:]
        ind = strtime.index("-")
        gregorian_month = int(strtime[:ind])
        strtime = strtime[ind + 1:]
        gregorian_day = int(strtime)
        return gregorian_year, gregorian_month, gregorian_day

    def elapsedtime(self):
        days = (self.year - 1) * 365.25
        gregorian_month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if self.month > 1:
            for i in range(0, self.month - 1):
                days += gregorian_month_days[i]
        days += self.day
        days2 = 0
        time = date.today()
        strtime = time.strftime('%Y-%m-%d')
        ind = strtime.index("-")
        gregorian_year = int(strtime[:ind])
        strtime = strtime[ind + 1:]
        ind = strtime.index("-")
        gregorian_month = int(strtime[:ind])
        strtime = strtime[ind + 1:]
        gregorian_day = int(strtime)
        days2 += (gregorian_year - 1) * 365.25
        gregorian_month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if gregorian_month > 1:
            for i in range(0, gregorian_month - 1):
                days2 += gregorian_month_days[i]
        days2 += gregorian_day
        days = math.floor(days)
        days2 = math.floor(days2)
        diff_days = days2 - days
        if diff_days == 0:
            return 0, 0, 0
        diff_year = diff_days // 365
        diff_days -= (diff_year // 4)
        diff_days %= 365
        gregorian_month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        diff_month = 0
        last_days = 0
        for i in range(0, 11):
            if gregorian_month_days[i] <= diff_days:
                diff_days -= gregorian_month_days[i]
            else:
                diff_month = i
                break
        last_days = diff_days
        return diff_year, diff_month, last_days

