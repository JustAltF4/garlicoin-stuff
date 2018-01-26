
import urllib.request

USER_AGENT = \
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"
HEADERS = {"User-Agent":USER_AGENT,}

def get_value(address):
    request = urllib.request.Request("https://explorer.grlc-bakery.fun/ext/getbalance/" + address, None, HEADERS)
    response = urllib.request.urlopen(request)
    return response.read()

def load(address_dict):
    for k in address_dict.keys():
        address_dict[k] = str(get_value(address_dict[k]))[2:-1]
        if "{" in list(address_dict[k]):
            address_dict[k] = 0.0
        address_dict[k] = float(address_dict[k])
    return address_dict

def output(values):
    for k in values.keys():
        print(k + ": " + str(values[k]))
    total_supply = 721761.70263962 # float(get_value("https://explorer.grlc-bakery.fun/ext/getmoneysupply")) not working
    total = sum(values.values())
    print("Total: " + str(total))
    print("Percentage: " + str((total/total_supply) * 100) + "%")

def main():
    adr_file = open("addresses.txt","r")
    data = adr_file.read().split("\n")[:-1]
    adr_dict = {}
    for l in data:
        adr_dict[l.split(" ")[0]] = l.split(" ")[1]
    val_dict = load(adr_dict)
    output(val_dict)

if __name__ == "__main__":
    main()
