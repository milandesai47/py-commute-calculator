import json
from datetime import datetime
from collections import namedtuple
from itertools import takewhile
from geopy.distance import geodesic
from itertools import groupby
from matplotlib import pyplot
import sys

Point = namedtuple('Point', 'latitude, longitude, datetime' )

def read_points():
  with open('abc2.json') as file:
    data = json.load(file)
  for point in data['locations']:
    yield Point(
        point['latitudeE7'] / 10 ** 7,
        point['longitudeE7'] / 10 ** 7,
        datetime.fromtimestamp(int(point['timestampMs']) / 1000)
    )
points = read_points()

#print(*points)
from_date = datetime(2017, 11, 1)
after_move = takewhile(lambda point: point.datetime >= from_date,points)


work_days = (point for point in after_move
             if point.datetime.weekday() < 5)

from_home = 8.15
reahced_to_work = 10

commute_time_to_work = (point for point in work_days
                        if from_home <= point.datetime.hour < reahced_to_work)

#print(*commute_time_to_home)
by_days_to_work = groupby(commute_time_to_work, key=lambda point: point.datetime.date())

home = (51.4097548, -2.5509183)
work = (51.5423741, -2.5736942)

max_distance_at_home = 0.060
max_distance_at_work = 0.150

def last_at_home(points):
  result = None
  for point in points:
    if geodesic(home, point[:2]).mi <= max_distance_at_home:
      result = point
  return result

def first_at_work(points, after):
  for point in points:
    if point.datetime > after.datetime and geodesic(work, point[:2]).mi <= max_distance_at_work:
      return point

Commute_to_work = namedtuple('Commute', 'day, start, end, took')


def get_commute_to_work():
  for day, points in by_days_to_work:
    points = [*points][::-1]

    start = last_at_home(points)
    if start is None:
      continue

    end = first_at_work(points, start)
    if end is None:
      continue

    yield Commute_to_work(day.strftime("%b"), start.datetime, end.datetime, end.datetime - start.datetime)

commutes = [*get_commute_to_work()][::-1]

normalised = [commute for commute in commutes
              if(commute.took.total_seconds()) < 70 * 60]
#create a sample graph
fig, ax = pyplot.subplots()
ax.scatter([commute.day for commute in normalised],
        [commute.took.total_seconds() / 60 for commute in normalised])

ax.set(xlabel='Month', ylabel='commute (minutes)',
       title='Daily commute')
ax.grid()
pyplot.show()