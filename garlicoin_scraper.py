import urllib.request, re

header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}

day = 1440
month = {"Jan": 0,"Feb": 44640,"Mar": 84960,"Apr": 129600,"May": 172800,"Jun": 217440,"Jul": 260640,"Aug": 305280,"Sep": 349920,"Oct": 393120,"Nov": 437760,"Dec": 480960}
year = 525600

REQUIRED_INCREASE = 3.5

def get(address):
    URL = "https://explorer.grlc-bakery.fun/address/" + address
    request = urllib2.Request(URL, headers = header)
    page = urllib2.urlopen(request)
    rows = re.findall(r'<tr>(.*?)</tr>',re.findall(r'<tbody>(.*?)</tbody>', page.read().replace("\n",""))[2])
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
    return convert_to_mins(time1) - convert_to_mins(time2)

def get_average_per_minute(address):
    history = get(address)
    time_skips = [get_difference(history[0][1], history[1][1])]
    total = history[0][0]
    total_time = get_difference(history[0][1], history[1][1])
    for i in range(1, len(history)-1):
        print(total)
        print(total_time)
        total += history[i][0]
        dif = get_difference(history[i][1], history[i+1][1])
        if not ((dif/(total_time/len(time_skips))) > REQUIRED_INCREASE):
            time_skips.append(dif)
            total_time += dif
    return total / total_time
 
print(get_average_per_minute("Gh86Zs3ek69sNdfebaE7DkhDHTYoKF99kL"))
