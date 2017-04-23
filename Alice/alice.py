# coding=utf-8
import os
import glob
import json
import ast

# variabile globale che mi serve per identificare il libro scelto da cifrare
file_choosen = -1

# mi faccio un array di lettere piu usate da Conan Doyle
letter_more_used = ""

# adesso dell'array_letters ne calcolo le occorrenze
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u','v', 'w', 'x', 'y', 'z']

###############################################################################

print'\033[94m\t\t\t  #########  ##       ####  ######    ########'
print'              ##     ##  ##        ##   ##        ##'
print'              ##     ##  ##        ##   ##        ##'
print'              ##     ##  ##        ##   ##        ######'
print'              #########  ##        ##   ##        ##'
print'              ##     ##  ##        ##   ##        ##'
print'              ##     ##  ######## ####  ########  ########\033[0m\n'

int_option1 = None
while int_option1 is None:

    print '0) create dictionary'
    print '1) select file'
    print '2) crypt'
    print '3) send'

    try:
        option1 = raw_input()
    except SyntaxError:
        int_option1 = None

    #crea dizionari
    if option1 == '0':
        print '1) per lettere'
        print '2) per parole'
        print '3) array delle lettere piu usate'

        opt = raw_input()

        #### LETTERE ####
        if opt == '1':

            # per vedere i libri devo fare cd ..
            os.chdir('/Users/alanguerzi/Documents/SPLI-CESARE')
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

            #prima devo tornare nella folder Alice
            os.chdir('/Users/alanguerzi/Documents/SPLI-CESARE/Alice')

            ## Save our changes to JSON file
            jsonFile = open("dictionary_letters.txt", "w+")
            jsonFile.write(json.dumps(data))
            jsonFile.close()

            print "dictionary_letters created!\n\n"

        #### PAROLE #####
        elif opt == '2':

            # per vedere i libri devo fare cd ..
            os.chdir('/Users/alanguerzi/Documents/SPLI-CESARE')
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
            os.chdir('/Users/alanguerzi/Documents/SPLI-CESARE/Alice')

            # scrivo e creo dizionario
            file = open("dictionary_words.txt", "w")
            file.write(array_without_occurence)

            print "dictionary_words created!\n\n"

        #lettere più usate
        elif opt == '3':

            with open('dictionary_letters.txt') as input_file:
                data_loaded = json.load(input_file)

            # per vedere i libri devo fare cd ..
            os.chdir('/Users/alanguerzi/Documents/SPLI-CESARE')
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

            # scrivo e creo file cifrato
            file = open("letters_more_used.txt", "w")
            file.write(letter_more_used[:-1])

            print "letters_more_used created!\n\n"

    # o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o #

    #seleziono i file
    elif option1 == '1':

        # per vedere i libri devo fare cd ..
        os.chdir('/Users/alanguerzi/Documents/SPLI-CESARE')
        # cosi non mi stampa anche STORY_CIPHER e STORY_CLEAR
        books = glob.glob("*_.txt")

        # stampo i file da selezionare1
        i = 0
        for num in books:
            print '\t' + str(i) + ') ' + books[i]
            i = i + 1

        try:
            file_choosen = raw_input()
        except SyntaxError:
            option = None

    # CIFRATURA
    elif option1 == '2':

        # per vedere i libri devo fare cd ..
        os.chdir('/Users/alanguerzi/Documents/SPLI-CESARE')
        # cosi non mi stampa anche STORY_CIPHER e STORY_CLEAR
        books = glob.glob("*_.txt")

        print 'the book choosen is: ' + books[int(file_choosen)]

        # aggiusto prima il file eliminando maiuscole al suo interno
        file = open(books[int(file_choosen)], "r+")
        story = file.read().lower()

        print 'insert OFFSET: (+2) (-2)'
        offset = raw_input()

        story_cipher = ""

        # ora scorro carattere per carattere e applico l offset alle lettere
        for c in story:
            # restituisce True se e un carattere ABCabc
            if c.isalpha():
                # ord('a') -> 97
                # chr(97 + 3) -> chr(100) -> 'd'

                # numero corrispondente in ASCII
                character = str(c)
                # print character
                old = ord(character)
                # print int(old)
                # numero shiftato destra o sinistra
                if offset.__contains__('+'):
                    new = int(old) + int(offset[1:])
                    if new > 122:
                        new = new - 26
                else:
                    new = int(old) - int(offset[1:])
                    if new < 97:
                        new = new + 26

                story_cipher = story_cipher + chr(new)
                # print chr(new)
            else:
                character = str(c)
                story_cipher = story_cipher + character

        # print story_cipher
        encrypted_file = story_cipher

        # prima devo tornare nella folder Alice
        os.chdir('/Users/alanguerzi/Documents/SPLI-CESARE/Alice')

        # scrivo e creo file cifrato
        file = open("STORY_CIPHER.txt", "w")
        file.write(story_cipher)

        print "story_cipher created!\n\n"

    # o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o #

    # invio file cifrato con netcat
    elif option1 == '3':
        print 'sending with netcat'
        print "insert ip target:"
        ip = raw_input()
        os.system('pv STORY_CIPHER.txt | nc -w 1 ' + ip + ' 3333')