import math

TAU = 2.0 * math.pi

def get_eot_min_D(D):
	W = TAU / 365.24
	A = W * (D + 10)
	B = A + 2*0.0167*math.sin(W * (D-2))
	C = (A - math.atan(math.tan(B) / math.cos(math.radians(23.44)))) / (TAU/2)
	eot = 720 * (C - int(C + 0.5))
	return eot

def get_solar_noon_D(lon, D):
	mean_solar_noon = D - (lon / 360.)
	return mean_solar_noon - (get_eot_min_D(D) / (24*60))

def get_hour_angle_D(lat, lon, D):
	mean_solar_noon = D - (lon / 360.)
	M = (357.5291 + 0.98560028 * mean_solar_noon) % 360.0
	C = 1.9148*math.sin(math.radians(M)) + 0.0200*math.sin(math.radians(2*M)) + 0.0003*math.sin(math.radians(3*M))
	ecliplic_lon = (M + C + 180 + 102.9372) % 360.0
	declination = math.asin(math.sin(math.radians(ecliplic_lon)) * math.sin(math.radians(23.44)))
	hour_angle = math.acos(
		(math.sin(math.radians(-0.83)) - math.sin(math.radians(lat)) * math.sin(declination))
		/
		(math.cos(math.radians(lat)) * math.cos(declination))
	)
	return hour_angle

import datetime

def get_solar_noon(lon, day):
	jd_origin = datetime.datetime(2000, 1, 1, 12, tzinfo=datetime.timezone.utc)
	D = (datetime.datetime(year=day.year, month=day.month, day=day.day, hour=12, tzinfo=datetime.timezone.utc) - jd_origin).total_seconds() / 86400 + 0.0008
	return jd_origin + datetime.timedelta(days=get_solar_noon_D(lon, D))

def get_eot(day):
	jd_origin = datetime.datetime(2000, 1, 1, 12, tzinfo=datetime.timezone.utc)
	D = (datetime.datetime(year=day.year, month=day.month, day=day.day, hour=12, tzinfo=datetime.timezone.utc) - jd_origin).total_seconds() / 86400 + 0.0008
	return datetime.timedelta(minutes=get_eot_min_D(D))

def get_hour_angle(lat, lon, day):
	jd_origin = datetime.datetime(2000, 1, 1, 12, tzinfo=datetime.timezone.utc)
	D = (datetime.datetime(year=day.year, month=day.month, day=day.day, hour=12, tzinfo=datetime.timezone.utc) - jd_origin).total_seconds() / 86400 + 0.0008
	return get_hour_angle_D(lat, lon, D)

def get_sunrise_and_sunset(lat, lon, day):
	hd = datetime.timedelta(days=(get_hour_angle(lat, lon, day) / TAU))
	return get_solar_noon(lon, day) - hd, get_solar_noon(lon, day) + hd

import unittest

class TestSolarCalculations(unittest.TestCase):
	def assertDatetimesEqual(self, a, b, delta_sec=120):
		ds = abs(a.timestamp() - b.timestamp())
		if (ds > delta_sec):
			raise AssertionError("%s !~= %s (delta=%g, diff=%g)" % (a, b, delta_sec, ds))

	def test_sunrise_and_sunset(self):
		day = datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc)
		sunrise, sunset = get_sunrise_and_sunset(0, 0, day)
		self.assertDatetimesEqual(day + datetime.timedelta(hours=6,  minutes=0), sunrise)
		self.assertDatetimesEqual(day + datetime.timedelta(hours=18, minutes=7), sunset)

		day = datetime.datetime(2002, 8, 9, tzinfo=datetime.timezone.utc)
		sunrise, sunset = get_sunrise_and_sunset(0, 0, day)
		self.assertDatetimesEqual(day + datetime.timedelta(hours=6,  minutes=2), sunrise)
		self.assertDatetimesEqual(day + datetime.timedelta(hours=18, minutes=9), sunset)

		day = datetime.datetime(2019, 3, 14, tzinfo=datetime.timezone.utc)
		sunrise, sunset = get_sunrise_and_sunset(41, 29, day)
		self.assertDatetimesEqual(day + datetime.timedelta(hours=4,  minutes=18), sunrise)
		self.assertDatetimesEqual(day + datetime.timedelta(hours=16, minutes=9),  sunset)

		day = datetime.datetime(2005, 1, 15, tzinfo=datetime.timezone.utc)
		sunrise, sunset = get_sunrise_and_sunset(60, 25, day)
		self.assertDatetimesEqual(day + datetime.timedelta(hours=7,  minutes=8), sunrise)
		self.assertDatetimesEqual(day + datetime.timedelta(hours=13, minutes=52), sunset)

		day = datetime.datetime(2006, 5, 4, tzinfo=datetime.timezone.utc)
		sunrise, sunset = get_sunrise_and_sunset(60, 25, day)
		self.assertDatetimesEqual(day + datetime.timedelta(hours=2,  minutes=11), sunrise)
		self.assertDatetimesEqual(day + datetime.timedelta(hours=18, minutes=25), sunset)

#		day = datetime.datetime(2090, 11, 5, tzinfo=datetime.timezone.utc)
#		sunrise, sunset = get_sunrise_and_sunset(42, -87.5, day)
#		self.assertDatetimesEqual(day + datetime.timedelta(hours=12, minutes=28), sunrise)
#		self.assertDatetimesEqual(day + datetime.timedelta(hours=22, minutes=38), sunset)

#		day = datetime.datetime(2090, 11, 30, tzinfo=datetime.timezone.utc)
#		sunrise, sunset = get_sunrise_and_sunset(42, -87.5, day)
#		self.assertDatetimesEqual(day + datetime.timedelta(hours=12, minutes=58), sunrise)
#		self.assertDatetimesEqual(day + datetime.timedelta(hours=22, minutes=20), sunset)
