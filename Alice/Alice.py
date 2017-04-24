# coding=utf-8
import os
import glob
import json
import ast


wlan = "eth0"
#devo configurarlo come host A
os.system('ifconfig ' + wlan + ' 172.30.1.2/24')
os.system('route add default gw 172.30.1.1')

###############################################################################

# variabile globale che mi serve per identificare il libro scelto da cifrare
file_choosen = -1

# mi faccio un array di lettere piu usate da Conan Doyle
letter_more_used = ""

# adesso dell'array_letters ne calcolo le occorrenze
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u','v', 'w', 'x', 'y', 'z']

###############################################################################

print'\033[94m#########  ##       ####  ######    ########'
print'##     ##  ##        ##   ##        ##'
print'##     ##  ##        ##   ##        ##'
print'##     ##  ##        ##   ##        ######'
print'#########  ##        ##   ##        ##'
print'##     ##  ##        ##   ##        ##'
print'##     ##  ######## ####  ########  ########\033[0m\n'

int_option1 = None
while int_option1 is None:

    print '1) select file'
    print '2) crypt'
    print '3) send'

    try:
        option1 = raw_input()
    except SyntaxError:
        int_option1 = None


    #seleziono i file
    if option1 == '1':

        # per vedere i libri devo fare cd ..
        os.chdir("../")
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

        # prima devo tornare nella folder Alice
        os.chdir('Alice')

        # scrivo e creo file cifrato
        file = open("STORY_CIPHER.txt", "w")
        file.write(story_cipher)

        print "\033[92mstory_cipher created!\n\n\033[0m"

    # o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o #

    # invio file cifrato con netcat
    elif option1 == '3':
        print 'sending with netcat'
        print "insert ip target:"
        ip = raw_input()
        os.system('pv STORY_CIPHER.txt | nc -w 1 ' + ip + ' 4000')