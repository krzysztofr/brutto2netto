brutto = 20000

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

# skl = skladka


# uwagi do limitow
# - po przekroczeniu limitu (e i r) zus emerytalne i rentowe w danym miesiacu tylko do czesci, ktora
#   nie przekroczy, a potem juz w ogole
# - podatek - 32% w kolejnym miesiacu po przekroczeniu progu

# for 1..12:
#  netto dla kazdego miesiaca
#  sumowanie skladek e i r
#  sumowanie netto
#  prog podatkowy (przekroczenie?)

netto = {}
netto_sum = 0
brutto_sum = 0
emer_rent_sum = 0
prog = 1

for miesiac in range(1, 13):
    brutto_sum += brutto

    if brutto_sum > zus_limit:
        er_base = brutto - (brutto_sum - zus_limit)
        if er_base < 0:
            er_base = 0
    else:
        er_base = brutto

    emer_rent = er_base*(emerytalna+rentowa)
    emer_rent_sum += emer_rent

    print er_base, er_base*emerytalna, er_base*rentowa


    skl_spoleczne = brutto*chorobowa + emer_rent
    skl_zdrowotne = (brutto - skl_spoleczne)*zdrowotne
    skl_zdrowotne2 = (brutto - skl_spoleczne)*zdrowotne2


    # podstawa - OK
    zaliczka_podatku = round(brutto - skl_spoleczne - koszt_uzysk_przychodu, 0) * progi[prog] - kwota_wolna

    if brutto_sum >= limit_prog1:
        prog = 2

    podatek = zaliczka_podatku - skl_zdrowotne2


    netto[miesiac] = int(round(brutto - skl_spoleczne - skl_zdrowotne - podatek,0))
    netto_sum += netto[miesiac]


print netto