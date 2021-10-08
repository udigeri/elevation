# ELE.PY
Tento skript spracuje .gpx subor pre potreby vytvorenia/najdenia/pridania zlomov.
napr. ele.py -i 2744.gpx -s 15 -r -shifA 12.69 -shiftB -3.25
OPTIONS parametre
-h(help) - vypisanie napovedy napr. (-h)
-i(input) subor.pripona - vstupny subor napr.(-i 8674.gpx)
-r(reverse) - vykresli .gpx subor v opacnom poradi napr. (-r)
-s(step) hodnota - vytvori novu krivku, kde bude pouzity kazdy dalsi bod vacsi ako hodnota (v metroch) napr. (-s 15)
-shiftA(posun) hodnota - posun nadmorskej vysky krivky na zaciatku o uvedenu hodnotu (v metroch) napr. (-shiftA 26.28)
-shiftB(posun) hodnota - posun nadmorskej vysky krivky na konci o uvedenu hodnotu (v metroch) napr. (-shiftB -5.52)

OUTPUT vystupy/subory
subor.pripona_reduced.gpx - novy subor s vynechanim nadbytocnych bodov podla -s (step)
subor.pripona_rounded.gpx - novy subor so zaokruhlenim zemep. dlzky, sirky na 6 desatinnych cisel a nadm vysky na 1 desatinne miesto
subor.pripona_shifted.gpx - novy subor s upravou nadmorskej vysky (nakalibrovanim) podla shiftA a shiftB
subor.pripona_wpt.txt - novy subor s detailnymi informaciami o zaujimavych bodoch (zlomy/TIM/ZK znackovaci kolik ...)
subor.pripona.png - novy subor s detailnymi informaciami o vyskovom profile trasy
