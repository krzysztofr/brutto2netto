# encoding: utf-8
import argparse
import json
import sys


def calculate_comp(brutto):

    # very ugly code, needs refactoring ;)
    koszt_uzysk_przychodu = 111.25
    emerytalna = .0976
    rentowa = .015
    chorobowa = .0245
    zdrowotne = .09
    zdrowotne2 = .0775
    progi = {
        1: .18,
        2: .32
    }
    limit_prog1 = 85528
    kwota_wolna = 46.33
    zus_limit = 121650

    netto = ()
    brutto_sum = 0
    emer_rent_sum = 0
    prog = 1

    for month in range(1, 13):
        brutto_sum += brutto

        if brutto_sum > zus_limit:
            er_base = brutto - (brutto_sum - zus_limit)
            if er_base < 0:
                er_base = 0
        else:
            er_base = brutto

        emer_rent = er_base*(emerytalna+rentowa)
        emer_rent_sum += emer_rent

        skl_spoleczne = brutto*chorobowa + emer_rent
        skl_zdrowotne = (brutto - skl_spoleczne)*zdrowotne
        skl_zdrowotne2 = (brutto - skl_spoleczne)*zdrowotne2

        zaliczka_podatku = round(brutto - skl_spoleczne - koszt_uzysk_przychodu, 0) * progi[prog] - kwota_wolna

        if brutto_sum >= limit_prog1:
            prog = 2

        podatek = zaliczka_podatku - skl_zdrowotne2

        netto = netto + (int(round(brutto - skl_spoleczne - skl_zdrowotne - podatek,0)),)

    average = sum(netto)/12

    return netto, average


def print_values(netto, average, amount, return_type="text"):
    if return_type == "oneline":
        print "%.0f" % average

    elif return_type == "text":
        print """
        Net compensation:

        January     %.0f PLN
        February    %.0f PLN
        March       %.0f PLN
        April       %.0f PLN
        May         %.0f PLN
        June        %.0f PLN
        July        %.0f PLN
        August      %.0f PLN
        September   %.0f PLN
        October     %.0f PLN
        November    %.0f PLN
        December    %.0f PLN

        average:    %.0f PLN per month

        Disclaimer: calculations may be erroneous. They are roughly rounded and don't include additional
        elements, i.e. sick leave, medical care deduction, English lessons, etc. Values rounded to 1 PLN.
        """ % (netto+(average,))

    elif return_type == "json":
        print json.dumps({
            "amount": amount,
            "compensation": {
                "monthly_avg": round(average, 2),
                "months": netto
            }
        })


parser = argparse.ArgumentParser(description="Calculate net salary from gross salary.")
parser.add_argument('-t', dest="return_type", default="text", choices=["text", "oneline", "json"], help="Select type of response. When 'oneline' selected, it will be only average value.")
parser.add_argument('amount', type=int, help="Gross amount per month.", nargs='?')
parser.add_argument('-i', dest="interactive", action="store_true", help="Enter interactive mode. Type 'exit' or Ctrl+C to finish.")

args = parser.parse_args()

if args.amount is None and not args.interactive:
    parser.print_help()
    sys.exit()

if args.interactive:
    while True:
        line = raw_input('Gross value in PLN ("exit" or Ctrl+C to quit): ')
        if line == 'exit':
            break
        try:
            amount = int(line)  # may throw ValueError
            if amount <= 0:
                raise ValueError
        except ValueError:
            print "Provide numeric value greater than 0."
        else:
            netto, average = calculate_comp(amount)
            print_values(netto=netto, average=average, amount=amount, return_type=args.return_type)

else:
    amount = args.amount
    if amount is None:
        raise ValueError("Provide numeric value greater than 0 as an argument.")
    netto, average = calculate_comp(amount)
    print_values(netto=netto, average=average, amount=amount, return_type=args.return_type)



