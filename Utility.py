	
seasonDict = {0:'Spring', 1:'Summer', 2:'Fall', 3:'Winter'}

def _dayToYear(day):
	return (day-1) // 112

def _dayToSeason(day):
	season = (day-1) // 28 % 4
	season = season if season in seasonDict.keys() else 0
	return seasonDict[season]

def dayToYSD(day):
	year = _dayToYear(day)
	season = _dayToSeason(day)
	day = 28 if day % 28==0 else day % 28
	YSD = 'Year: %1d Season: %s Day: %2d'%(year+1,season,day)
	return YSD

def ysdToDay(input):
	year = "";
	season = "";
	day = "";
	lookingForYear = True
	for c in input:
		if lookingForYear:
			try:
				digit = int(c)
				year = year + c;
				continue
			except:
				lookingForYear = False
		if not lookingForYear:
			try:
				digit = int(c)
				day = day + c
			except:
				season = season + c.upper()

	for c in season:
		if c == "F":
			seasonNumber = 2
			break
		if c == "W":
			seasonNumber = 3
			break
		if c == "P":
			seasonNumber = 0
			break
		if c == "U":
			seasonNumber = 1
			break

	return (int(year)-1) * 112 + seasonNumber * 28 + int(day)

if __name__ == '__main__':
	print(ysdToDay("1F14"))
	print(ysdToDay("1F16"))
	print(ysdToDay("1F26"))
	print(ysdToDay("1F28"))
	print(ysdToDay("1F23"))
	print(ysdToDay("1F25"))