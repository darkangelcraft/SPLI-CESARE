# coding=utf-8
import os
import glob

# variabile globale che mi serve per identificare il libro scelto da cifrare
file_choosen = -1

###############################################################################

print'\033[94m\t\t\t   #######   ######### ######## '
print'               ##     ## ##     ## ##     ##'
print'               ##     ## ##     ## ##     ##'
print'               ########  ##     ## ######## '
print'               ##     ## ##     ## ##     ##'
print'               ##     ## ##     ## ##     ##'
print'               ########   #######  ########\033[0m\n'


int_option2 = None
while int_option2 is None:

    print '1) receiv'
    print '2) decrypt'
    print '3) show received_file'

    try:
        option2 = raw_input()
    except SyntaxError:
        int_option2 = None

    # RECEIVER
    if option2 == '1':
        print 'waiting...'
        os.chdir('Bob')
        os.system('nc -l -p 3333 | pv -rb > STORY_CIPHER.txt')

    # o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o #

    # DECIFRATURA
    elif option2 == '2':

        # cosi non mi stampa anche STORY_CIPHER e STORY_CLEAR
        books = glob.glob("*_.txt")

        # aggiusto prima il file eliminando maiuscole al suo interno
        file = open("STORY_CIPHER.txt", "r+")
        story = file.read()

        print 'insert OFFSET known:'
        offset = raw_input()

        story_clear = ""

        # inizio decifrazione avendo noto l'offset
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

                story_clear = story_clear + chr(new)
                # print chr(new)
            else:
                character = str(c)
                story_clear = story_clear + character

        # scrivo e creo file cifrato
        file = open("STORY_CLEAR.txt", "w")
        file.write(story_clear)

        print "story_clear created!\n\n"

    # o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o #

    elif option2 == '3':
        print os.system('cat STORY_CIPHER.txt')
