import urllib.request, re

header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}

day = 1440
month = {"Jan": 0,"Feb": 44640,"Mar": 84960,"Apr": 129600,"May": 172800,"Jun": 217440,"Jul": 260640,"Aug": 305280,"Sep": 349920,"Oct": 393120,"Nov": 437760,"Dec": 480960}
year = 525600

# required percentage increase (1 = 100%) to justify a break in mining
REQUIRED_INCREASE = 100

def get(address):
    #returns an array of 2 length tuples containing the grlc increase and time in that order
    URL = "https://explorer.grlc-bakery.fun/address/" + address
    request = urllib.request.Request(URL, None, header)
    page = urllib.request.urlopen(request)
    rows = re.findall(r'<tr>(.*?)</tr>',re.findall(r'<tbody>(.*?)</tbody>', str(page.read()).replace("\n","").replace("info","success"))[2])
    row_data = []
    for row in rows:
        row_data.append((float(re.findall(r'<td class="success">(.*?)</td>', row)[0].split(" ")[1]), re.findall(r'<td class="hidden-xs">(.*?)</td>', row)[0]))
    return row_data[::-1]

def convert_to_mins(time):
    #28th Jan 2018 13:49:09 example format : 1060746589

    total = 0
    total += day * int(time[0:2])
    total += month[time[5:8]]
    total += year * int(time[9:13])
    total += 60 * int(time.strip(" ").split(" ")[-1].split(":")[0])
    total += int(time.strip(" ").split(" ")[-1].split(":")[1])
    return total

def get_difference(time2, time1):
    #finds the difference in minutes between two times
    return convert_to_mins(time1) - convert_to_mins(time2)

def get_average_per_minute(address):
    #finds average garlicoins per minute by adding total garlicoin change and time change
    history = get(address)
    time_skips = [get_difference(history[0][1], history[1][1])]
    total = history[0][0]
    total_time = get_difference(history[0][1], history[1][1])
    for i in range(1, len(history)-1):
        total += history[i][0]
        dif = get_difference(history[i][1], history[i+1][1])
        if not ((dif/(total_time/len(time_skips))) > REQUIRED_INCREASE):
            time_skips.append(dif)
            total_time += dif
    return total / total_time

#print(get_average_per_minute("Gh86Zs3ek69sNdfebaE7DkhDHTYoKF99kL"))
