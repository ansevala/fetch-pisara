#!/usr/bin/env python3
from enum import Enum
import json
import requests
import argparse

veribarometri_url = "https://www.veripalvelu.fi/_vti_bin/Innofactor.Veripalvelu.Web/BarometerService.svc/GetBarometerValues"
supply_messages = {
    "en": "The blood supply for blood group",
    "fi": "Veren tarjonta veriryhmälle"
}
verbs = {
    "en": "is",
    "fi": "on"
}
good_supply = {
    "en": "fairly good",
    "fi": "hyvä"
}
low_supply = {
    "en": "low",
    "fi": "alhainen"
}
critical_supply = {
    "en": "critically low",
    "fi": "erittäin alhainen"
}

parser = argparse.ArgumentParser(description='Get blood supply information in Finland.')
parser.add_argument('-t', '--type', dest='type', type=str.upper,
                    choices=["A+", "A-", "O+", "O-",
                             "B+", "B-", "AB+", "AB-"],
                    help='Blood type')
parser.add_argument('-f', '--format', dest='format', choices=['text', 'json'],
                    default='text', help='Output format')
parser.add_argument('-l', '--lang', dest='lang', choices=['fi', 'en'],
                    type=str.lower, default='fi')
parser.add_argument('--brief', action='store_true')
args = parser.parse_args()

class Supply(Enum):
    A = good_supply[args.lang]
    B = low_supply[args.lang]
    C = critical_supply[args.lang]

status_s = requests.post(veribarometri_url).text
statuses = json.loads(status_s)

if args.type:
    statuses = [x for x in statuses if x['Title'] == args.type]

if args.format == 'json':
    print(statuses)
else:
    for b in statuses:
        if not args.brief:
            print("{} {} {} {}".format(
                supply_messages[args.lang],
                b['Title'],
                verbs[args.lang],
                Supply[b['Bloodtypevalue']].value
                )
            )
        else:
            print("{}: {}".format(
                b['Title'],
                Supply[b['Bloodtypevalue']].value
                )
            )
