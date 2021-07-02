from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Show

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatDay(self, day, shows):
        shows_per_day = shows.filter(startDate__day=day)
        d = ''
        for show in shows_per_day:
            d += f'<li> {show.title} </li>'

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"

        return '<td></td>'

    def formatWeek(self, theWeek, shows):
        week = ''
        for d, weekday in theWeek:
            week += self.formatDay(d, shows)
        return f'<tr> {week} </tr>'

    def formatMonth(self, withyear=True):
        shows = Show.objects.filter(startDate__year=self.year, startDate__month=self.month)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatWeek(week, shows)}\n'
        return cal