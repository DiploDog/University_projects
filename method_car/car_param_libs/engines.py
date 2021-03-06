# Параметры двигателей

# Ne [кВт]; ne[об/мин], d[мм], s[мм], V[л], gен[г/кВт*ч]

YAMZ_7511_10 = {
    'Ne': 294,
    'ne': 1900,
    'i': '8V',
    'd': 130,
    's': 140,
    'V': 14.85,
    'G': 1215,
    'gен': 194
}

YAMZ_240m2 = {
    'Ne': 266,
    'ne': 2100,
    'i': '12V',
    'd': 130,
    's': 140,
    'V': 22.3,
    'G': 1550,
    'gен': 228
}

KAMAZ_740_50_360 = {
    'Ne': 265,
    'ne': 2200,
    'i': '8V',
    'd': 120,
    's': 130,
    'V': 11.76,
    'G': 885,
    'gен': 202
}

YAMZ_7512_10 = {
    'Ne': 264,
    'ne': 1900,
    'i': '8V',
    'd': 130,
    's': 140,
    'V': 14.86,
    'G': 1215,
    'gен': 194
}

YAMZ_238D_8 = {
    'Ne': 243,
    'ne': 2000,
    'i': '8V',
    'd': 130,
    's': 140,
    'V': 14.86,
    'G': 1130,
    'gен': 204
}

KAMAZ_740_30_260 = {
    'Ne': 191.1,
    'ne': 2200,
    'i': '8V',
    'd': 120,
    's': 120,
    'V': 10.85,
    'G': 885,
    'gен': 207
}

YAMZ_238M2 = {
    'Ne': 176,
    'ne': 2100,
    'i': '8V',
    'd': 130,
    's': 140,
    'V': 14.86,
    'G': 1075,
    'gен': 214
}

KAMAZ_740_10 = {
    'Ne': 154.5,
    'ne': 2600,
    'i': '8V',
    'd': 120,
    's': 120,
    'V': 10.85,
    'G': 750,
    'gен': 224
}

YAMZ_236A = {
    'Ne': 143,
    'ne': 2100,
    'i': '6V',
    'd': 130,
    's': 140,
    'V': 11.15,
    'G': 880,
    'gен': 214
}

YAMZ_236N = {
    'Ne': 132.4,
    'ne': 2100,
    'i': '6V',
    'd': 130,
    's': 140,
    'V': 11.15,
    'G': 880,
    'gен': 214
}

ZIL_509_10 = {
    'Ne': 129,
    'ne': 3200,
    'i': '8V',
    'd': 108,
    's': 95,
    'V': 7,
    'G': 490,
    'gен': 215
}

ZIL_508_10 = {
    'Ne': 110,
    'ne': 3200,
    'i': '8V',
    'd': 100,
    's': 95,
    'V': 6,
    'G': 490,
    'gен': 292
}

MMZ_D_245_9_E = {
    'Ne': 110,
    'ne': 2400,
    'i': '8P',
    'd': 110,
    's': 125,
    'V': 4.75,
    'G': 430,
    'gен': 210
}

ZMZ_5233_10 = {
    'Ne': 96.3,
    'ne': 3200,
    'i': '8V',
    'd': 92,
    's': 88,
    'V': 4.67,
    'G': 265,
    'gен': 279
}

engines_dict = {
    # Библиотека двигателей и их параметров
    'ЯМЗ-7511.10': YAMZ_7511_10,
    'ЯМЗ 240м2': YAMZ_240m2,
    'КАМАЗ 740.50-360': KAMAZ_740_50_360,
    'ЯМЗ-7512.10': YAMZ_7512_10,
    'ЯМЗ-238Д-8': YAMZ_238D_8,
    'КАМАЗ 740.30-260': KAMAZ_740_30_260,
    'ЯМЗ 238М2': YAMZ_238M2,
    'КАМАЗ 740.10': KAMAZ_740_10,
    'ЯМЗ 236А': YAMZ_236A,
    'ЯМЗ 236Н': YAMZ_236N,
    'ЗИЛ 509.10': ZIL_509_10,
    'ЗИЛ 508.10': ZIL_508_10,
    'ММЗ Д-245.9 Е': MMZ_D_245_9_E,
    'ЗМЗ-5233.10': ZMZ_5233_10
}
