# coding=utf-8
import glob
import json
import ast
import time
import os

wlan = "eth0"
#devo configurarlo come gateway C

# impostazione indirizzi IP
os.system('sudo ifconfig -v ' + wlan + ':1 172.30.1.1/24')
os.system('sudo ifconfig -v ' + wlan + ':2 172.30.2.1/24')

# cancella le route di default
os.system('sudo route del default')

# aggiunge route per vedere le reti
os.system('sudo route add -net 172.30.1.0 netmask 255.255.255.0 gw 172.30.1.1 dev ' + wlan + ':1')
os.system('sudo route add -net 172.30.2.0 netmask 255.255.255.0 gw 172.30.2.1 dev ' + wlan + ':2')

# abilitare il forwarding dei pacchetti
os.system('sudo sysctl -w net.ipv4.ip_forward=1')

# disabilita ICMP redirect
os.system('sudo sysctl -w net.ipv4.conf.all.accept_redirects=0')
os.system('sudo sysctl -w net.ipv4.conf.all.send_redirects=0')

# default
os.system('sudo sysctl -w net.ipv4.conf.default.accept_redirects=0')
os.system('sudo sysctl -w net.ipv4.conf.default.send_redirects=0')

# dev wlan
os.system('sudo sysctl -w net.ipv4.conf.' + wlan + '.accept_redirects=0')
os.system('sudo sysctl -w net.ipv4.conf.' + wlan + '.send_redirects=0')

# lo
os.system('sudo sysctl -w net.ipv4.conf.lo.accept_redirects=0')
os.system('sudo sysctl -w net.ipv4.conf.lo.send_redirects=0')

###############################################################################

# variabile globale che mi serve per identificare il libro scelto da cifrare
file_choosen = -1

# mi faccio un array di lettere piu usate da Conan Doyle
letter_more_used = ""

# adesso dell'array_letters ne calcolo le occorrenze
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u','v', 'w', 'x', 'y', 'z']

###############################################################################

print'\033[94m######   ##     ##    ###    ########  ##       #### ########'
print'##    ## ##     ##   ## ##   ##     ## ##        ##  ##       '
print'##       ##     ##  ##   ##  ##     ## ##        ##  ##       '
print'##       ######### ##     ## ########  ##        ##  ######   '
print'##       ##     ## ######### ##   ##   ##        ##  ##       '
print'##    ## ##     ## ##     ## ##    ##  ##        ##  ##       '
print'######   ##     ## ##     ## ##     ## ######## #### ######## \033[0m\n'

int_option3 = None
while int_option3 is None:

    print "0) create dictionary"
    print "1) sniffing packet"
    print "2) bruteforce attack"
    print "3) frequency attack"

    try:
        option3 = raw_input()
    except SyntaxError:
        int_option3 = None

    if option3 == '0':
        # crea dizionari
        print '1) per lettere'
        print '2) per parole'
        print '3) array delle lettere piu usate'

        opt = raw_input()

        #### LETTERE ####
        if opt == '1':

            # per vedere i libri devo fare cd ..
            os.chdir("../")
            # cosi non mi stampa anche STORY_CIPHER e STORY_CLEAR
            books = glob.glob("*_.txt")

            array_books = []
            story = []

            i = 0
            # scorro tutti i libri
            while i < 6:
                file = open(books[i], "r")
                # bisogna togliere la punteggiature [".", ";", ":", "!", "?", "/", "\\", ",", "#", "@", "$", "&", ")", "(", "\""]
                story.append(str(
                    file.read().lower().replace(".", " ").replace("'", " ").replace(";", " ").replace(":",
                                                                                                      " ").replace(
                        "!", " ").replace("?", " ").replace("/", " ").replace("'\'", " ").replace(',', " ").replace(
                        "#",
                        " ").replace(
                        "@", " ").replace("$", " ").replace("&", " ").replace(")", " ").replace('"', " ").replace(
                        "-",
                        " ").replace(
                        "°", " ").replace("(", " ").split()))

                # faccio un merge di tutti i libri
                # print ast.literal_eval(story[i])
                array_books.append(str(ast.literal_eval(story[i])))
                i += 1

            # creo array string con tutte le lettere di tutti i libri
            array_letters = ""

            j = 0
            while j < 6:
                for word in ast.literal_eval(array_books[j]):
                    for c in word:
                        if c.isalpha():
                            array_letters += c + ' '
                j += 1

            print array_letters

            # inizializzo file json
            data = []

            # prima devo tornare nella folder Alice
            os.chdir('Charlie')

            with open('dictionary_letters.txt', 'w') as outfile:
                json_data = json.dumps(data)
                outfile.write(json_data)

            k = 0
            while k < 26:
                # print 'letter: '+alphabet[k]
                # print 'occ: '+str(array_letters.count(alphabet[k]))
                # print 'freq: '+str(round(float(array_letters.count(alphabet[k]))/float(len(array_letters))*100,2))
                # print ''

                # aggiungo al file json il num di lettere, le sue occorrenze e la frequenza all'interno dei libri
                data.append({'letter': alphabet[k], 'occ': array_letters.count(alphabet[k]), 'freq': round(
                    float(array_letters.count(alphabet[k])) / float(len(array_letters)) * 100, 2)})
                k += 1

            ## Save our changes to JSON file
            jsonFile = open("dictionary_letters.txt", "w+")
            jsonFile.write(json.dumps(data))
            jsonFile.close()

            print "\033[92mdictionary_letters created!\n\n\033[0m"

        #### PAROLE #####
        elif opt == '2':

            # per vedere i libri devo fare cd ..
            os.chdir("../")
            # cosi non mi stampa anche STORY_CIPHER e STORY_CLEAR
            books = glob.glob("*_.txt")

            array_without_occurence = ""
            story = []

            i = 0
            # scorro tutti i libri
            while i < 6:
                file = open(books[i], "r")
                # bisogna togliere la punteggiature [".", ";", ":", "!", "?", "/", "\\", ",", "#", "@", "$", "&", ")", "(", "\""]
                story.append(str(
                    file.read().lower().replace(".", " ").replace("'", " ").replace(";", " ").replace(":",
                                                                                                      " ").replace(
                        "!", " ").replace("?", " ").replace("/", " ").replace("'\'", " ").replace(',', " ").replace(
                        "#", " ").replace("@", " ").replace("$", " ").replace("&", " ").replace(")", " ").replace(
                        '"', " ").replace("-", " ").replace("°", " ").replace("(", " ").split()))

                # aggiungo le parole non doppie
                for word in ast.literal_eval(story[i]):
                    if not array_without_occurence.__contains__(word):
                        array_without_occurence += word + '\n'

                # passo al libro sucessivo
                i += 1

            # prima devo tornare nella folder Alice
            os.chdir('Charlie')

            # scrivo e creo dizionario
            file = open("dictionary_words.txt", "w")
            file.write(array_without_occurence)

            print "\033[92mdictionary_words created!\n\n\033[0m"

        # lettere più usate
        elif opt == '3':

            with open('dictionary_letters.txt') as input_file:
                data_loaded = json.load(input_file)

            # per vedere i libri devo fare cd ..
            os.chdir("../")
            # cosi non mi stampa anche STORY_CIPHER e STORY_CLEAR
            books = glob.glob("*_.txt")

            # #mi serve per capire Conan Doyle quali lettere usa maggiormente
            # ordino in ordine decrescente la frequenza delle lettere!
            sorted_list = sorted(data_loaded, key=lambda k: (int(k['freq'])), reverse=True)[:10]
            # sorted_list.take(5) equivalente in python sorted_list[:5]
            # print sorted_list[:10]

            num = 0
            while num < len(sorted_list):
                letter_more_used += (sorted_list[num]['letter']) + ','
                num += 1

            # stampo e elimino il punto e virgola finale con [:-1] equivale ad un remove.last()
            print letter_more_used[:-1]

            os.chdir("Charlie")

            # scrivo e creo file cifrato
            file = open("letters_more_used.txt", "w")
            file.write(letter_more_used[:-1])

            print "\033[92mletters_more_used created!\n\n\033[0m"


    elif option3 == '1':
        os.chdir("../")
        os.system('python sniffer.py')


    #bruteforce
    elif option3 == '2':

        # cosi non mi stampa anche STORY_CIPHER e STORY_CLEAR
        books = glob.glob("*_.txt")

        print "########  ########  ##     ## ######## ######## ########  #######  ########   ######  ######## "
        print "##     ## ##     ## ##     ##    ##    ##       ##       ##     ## ##     ## ##    ## ##       "
        print "##     ## ##     ## ##     ##    ##    ##       ##       ##     ## ##     ## ##       ##       "
        print "########  ########  ##     ##    ##    ######   ######   ##     ## ########  ##       ######   "
        print "##     ## ##   ##   ##     ##    ##    ##       ##       ##     ## ##   ##   ##       ##       "
        print "##     ## ##    ##  ##     ##    ##    ##       ##       ##     ## ##    ##  ##    ## ##       "
        print "########  ##     ##  #######     ##    ######## ##        #######  ##     ##  ######  ######## \n"

        # apro il file cifrato
        file = open('STORY_CIPHER.txt', "r+")
        story_cipher = file.read()
        a = len(story_cipher)

        # (inizio il bruteforce!)
        file1 = open('dictionary_words.txt', "r+")
        dictionary = file1.read()

        # il bruteforce viene fatto due alla volta, ovvero per il numero 3 viene fatto sia (+3) che (-3)
        offset_bruteforce = 1

        while offset_bruteforce < 27:

            t1 = time.time()

            story_bruteforce_positive = ""
            story_bruteforce_negative = ""

            # inizio decifrazione avendo noto l'offset
            for c in story_cipher:
                # restituisce True se e un carattere ABCabc
                if c.isalpha():
                    # ord('a') -> 97
                    # chr(97 + 3) -> chr(100) -> 'd'

                    # numero corrispondente in ASCII
                    character = str(c)
                    # print character
                    old = ord(character)
                    # print int(old)

                    # numero shiftato destra
                    new_positive = int(old) + offset_bruteforce
                    if new_positive > 122:
                        new_positive = new_positive - 26

                    # numero shiftato a sinistra
                    new_negative = int(old) - offset_bruteforce
                    if new_negative < 97:
                        new_negative = new_negative + 26

                    story_bruteforce_positive = story_bruteforce_positive + chr(new_positive)
                    story_bruteforce_negative = story_bruteforce_negative + chr(new_negative)
                    # print chr(new)

                # e un carattere lo lascio cosi
                else:
                    character = str(c)
                    story_bruteforce_positive = story_bruteforce_positive + character
                    story_bruteforce_negative = story_bruteforce_negative + character

            # mi faccio due array di 0 e 1 in base a SI appartiene alla lista o NO non appartiane
            en_pos = []
            en_neg = []

            i = 0
            n = len(story_bruteforce_positive.split())
            # visto che hanno entrambe uguale lunghezza
            # posso usare direttamente la meta della parole tanto sono sufficienti per far match con il dizionario
            # per velocizzarlo di quasi 2s posso anche arrivare a n/3,n/4 perche sarebbero 2000 parole
            # n/10 equivale a 1000 parole e sono abbastanza
            while i < n / 10:

                wordp = story_bruteforce_positive.split()[i]
                if dictionary.__contains__(wordp):
                    en_pos.append(True)
                else:
                    en_pos.append(False)

                wordn = story_bruteforce_negative.split()[i]
                if dictionary.__contains__(wordn):
                    en_neg.append(True)
                else:
                    en_neg.append(False)
                i += 1

            percent_plus = (float(en_pos.count(True)) / float(len(en_pos))) * 100
            percent_minus = (float(en_neg.count(True)) / float(len(en_neg))) * 100

            print 'offset (+' + str(offset_bruteforce) + ') ---> ' + str(round(percent_plus, 1)) + '%'
            print 'offset (-' + str(offset_bruteforce) + ') ---> ' + str(round(percent_minus, 1)) + '%'
            print ''

            if int(percent_plus) > 80:
                print "# FIND! #"
                print 'the offset used is (-' + str(offset_bruteforce) + ')\n'

                os.chdir('Charlie')

                # scrivo e creo file cifrato
                file = open("STORY_BRUTEFORCE.txt", "w")
                file.write(story_bruteforce_positive)

                offset_bruteforce = 28

            elif int(percent_minus) > 80:
                print "# FIND! #"
                print 'the offset used is (+' + str(offset_bruteforce) + ')\n'

                # scrivo e creo file cifrato
                file = open("STORY_BRUTEFORCE.txt", "w")
                file.write(story_bruteforce_negative)

                offset_bruteforce = 28

            # print str(round((time.time() - t1), 1)) + 's'
            # fallito passo all offset successivo
            offset_bruteforce += 1

        print "story_bruteforce created!\n\n"

        # o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o #

    #frequency
    elif option3 == '3':

        # cosi non mi stampa anche STORY_CIPHER e STORY_CLEAR
        books = glob.glob("*_.txt")

        print "######## ########  ########  #######  ##     ## ######## ##    ##  ######  ######## "
        print "##       ##     ## ##       ##     ## ##     ## ##       ###   ## ##    ## ##       "
        print "##       ##     ## ##       ##     ## ##     ## ##       ####  ## ##       ##       "
        print "######   ########  ######   ##     ## ##     ## ######   ## ## ## ##       ######   "
        print "##       ##   ##   ##       ##  ## ## ##     ## ##       ##  #### ##       ##       "
        print "##       ##    ##  ##       ##    ##  ##     ## ##       ##   ### ##    ## ##       "
        print "##       ##     ## ########  ##### ##  #######  ######## ##    ##  ######  ######## \n"

        # apro il file cifrato
        file = open('STORY_CIPHER.txt', "r+")
        story_cipher = file.read()

        # (inizio l attacco per frequenza!)
        # mi calcolo le occorrenze delle lettere del cifrato, scopo ultimo ovviamente risalire all'offset usato

        letter_more_used = open("letters_more_used.txt", "r").read()
        print 'deve fare match con quello di Conan Doyle: [' + letter_more_used + ']'

        offset_bruteforce = 1

        while offset_bruteforce < 27:

            t1 = time.time()

            # riutilizzo il codice di prima tanto sempre bruteforce e
            story_bruteforce_positive = ""
            story_bruteforce_negative = ""

            # inizio decifrazione avendo noto l'offset
            for c in story_cipher:
                # restituisce True se e un carattere ABCabc
                if c.isalpha():
                    # ord('a') -> 97
                    # chr(97 + 3) -> chr(100) -> 'd'

                    # numero corrispondente in ASCII
                    character = str(c)
                    # print character
                    old = ord(character)
                    # print int(old)

                    # numero shiftato destra
                    new_positive = int(old) + offset_bruteforce
                    if new_positive > 122:
                        new_positive = new_positive - 26

                    # numero shiftato a sinistra
                    new_negative = int(old) - offset_bruteforce
                    if new_negative < 97:
                        new_negative = new_negative + 26

                    story_bruteforce_positive = story_bruteforce_positive + chr(new_positive)
                    story_bruteforce_negative = story_bruteforce_negative + chr(new_negative)
                    # print chr(new)

                # e un carattere lo lascio cosi
                else:
                    character = str(c)
                    story_bruteforce_positive = story_bruteforce_positive + character
                    story_bruteforce_negative = story_bruteforce_negative + character

            # qui la cosa cambia adesso che ho applicato l offset faccio l'analisi in frequenza
            # mi calcolo le frequenza delle 10 lettere piu usate di entrambi

            # creo array string con tutte le lettere dei due file applicati l'offset
            array_letters_positive = ""
            array_letters_negative = ""

            # sono necessari per la formattazione di ast.literal_eval
            story_positive = []
            story_negative = []

            story_positive.append(str(
                story_bruteforce_positive.replace(".", " ").replace("'", " ").replace(";", " ").replace(":",
                                                                                                        " ").replace(
                    "!", " ").replace("?", " ").replace("/", " ").replace("'\'", " ").replace(',', " ").replace("#",
                                                                                                                " ").replace(
                    "@", " ").replace("$", " ").replace("&", " ").replace(")", " ").replace('"', " ").replace("-",
                                                                                                              " ").replace(
                    "°", " ").replace("(", " ").split()))

            story_negative.append(str(
                story_bruteforce_negative.replace(".", " ").replace("'", " ").replace(";", " ").replace(":",
                                                                                                        " ").replace(
                    "!", " ").replace("?", " ").replace("/", " ").replace("'\'", " ").replace(',', " ").replace("#",
                                                                                                                " ").replace(
                    "@", " ").replace("$", " ").replace("&", " ").replace(")", " ").replace('"', " ").replace("-",
                                                                                                              " ").replace(
                    "°", " ").replace("(", " ").split()))

            for wordp in ast.literal_eval(str(story_positive)):
                for c in wordp:
                    if c.isalpha():
                        array_letters_positive += c + ' '

            for wordn in ast.literal_eval(str(story_negative)):
                for c in wordn:
                    if c.isalpha():
                        array_letters_negative += c + ' '

            # inizializzo file json
            data_positive = []
            json_data_positive = json.dumps(data_positive)
            data_negative = []
            json_data_negative = json.dumps(data_negative)

            k = 0
            while k < 26:
                # print 'letter: '+alphabet[k]
                # print 'occ: '+str(array_letters.count(alphabet[k]))
                # print 'freq: '+str(round(float(array_letters.count(alphabet[k]))/float(len(array_letters))*100,2))
                # print ''

                # aggiungo al file json il num di lettere, le sue occorrenze e la frequenza all'interno dei libri
                data_positive.append(
                    {'letter': alphabet[k], 'occ': array_letters_positive.count(alphabet[k]), 'freq': round(
                        float(array_letters_positive.count(alphabet[k])) / float(len(array_letters_positive)) * 100,
                        2)})

                data_negative.append(
                    {'letter': alphabet[k], 'occ': array_letters_negative.count(alphabet[k]), 'freq': round(
                        float(array_letters_negative.count(alphabet[k])) / float(len(array_letters_negative)) * 100,
                        2)})

                k += 1

            sorted_list_positive = sorted(data_positive, key=lambda k: (int(k['freq'])), reverse=True)[:10]
            sorted_list_negative = sorted(data_negative, key=lambda k: (int(k['freq'])), reverse=True)[:10]

            letter_more_used_positive = ""
            letter_more_used_negative = ""

            # deve fare match con quello di Conan Doyle:

            num = 0
            while num < len(sorted_list_negative):
                letter_more_used_positive += (sorted_list_positive[num]['letter']) + ','
                letter_more_used_negative += (sorted_list_negative[num]['letter']) + ','
                num += 1

            # stampo e elimino il punto e virgola finale con [:-1] equivale ad un remove.last()
            print 'for (+' + str(offset_bruteforce) + ') --> ' + letter_more_used_positive[:-1]
            print 'for (-' + str(offset_bruteforce) + ') --> ' + letter_more_used_negative[:-1]
            print ''

            i = 0

            if (letter_more_used[0] == letter_more_used_positive[0]):
                if (letter_more_used[1] == letter_more_used_positive[1]):
                    print "# FIND! #"
                    print 'the offset used is (-' + str(offset_bruteforce) + ')\n'
                    offset_bruteforce = 28

                    # scrivo e creo file cifrato
                    file = open("STORY_FREQUENCE.txt", "w")
                    file.write(story_bruteforce_positive)

            elif (letter_more_used[0] == letter_more_used_negative[0]):
                if (letter_more_used[1] == letter_more_used_negative[1]):
                    print "# FIND! #"
                    print 'the offset used is (+' + str(offset_bruteforce) + ')\n'
                    offset_bruteforce = 28

                    # scrivo e creo file cifrato
                    file = open("STORY_FREQUENCE.txt", "w")
                    file.write(story_bruteforce_negative)
            else:
                offset_bruteforce += 1

        print "\033[92mstory_frequence created!\n\n\033[0m"

