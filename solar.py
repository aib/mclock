import math

TAU = 2.0 * math.pi

# Based on https://en.wikipedia.org/wiki/Equation_of_time
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

# Based on https://en.wikipedia.org/wiki/Sunrise_equation
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
