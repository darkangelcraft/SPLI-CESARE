# coding=utf-8
import os
import glob
import json
import ast
import time

from random import shuffle
from string import maketrans

### CONVERSION LETTERS TO ASCII CODE ##########################################
'''
 ord('a') -> 97
 chr(97 + 3) -> chr(100) -> 'd'
'''

### CONSTANTS #################################################################
BOOKS_COUNT = 6
ASCII_RANGE_VALID_VALUE = 26
ASCII_LOWER_LIMIT_VALUE = 97
ASCII_UPPER_LIMIT_VALUE = 122
MIN_OFFSET_ATTACK = 1
MAX_OFFSET_ATTACK = 26
BRUTEFORCE_SUCCESS_RATE = 80

### GLOBALS ###################################################################

file_choosen = -1
books = glob.glob("*_.txt")

# lettere piu usate da Conan Doyle
letter_more_used = ""

# alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
#  'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
alphabet = "abcdefghijklmnopqrstuvwxyz"

# indica se la cifratura è avvenuta con un offset positivo o negativo
encryptionOffsetSign = ''

# Bruteforce
posMatchPercents = dict()
negMatchPercents = dict()

offset = None


### FUNCTION DEFINITIONS ######################################################

# Description
#    Cifra il testo del messaggio applicando un offset specificato.
#
# Params
#    @story: testo del messaggio in chiaro.
#    @encryptionOffset: offset da applicare ai caratteri del messaggio per la
#    cifratura.
#
# Returns
#    Restituisce il messaggio cifrato.
def DoEncrypt(story, encryptionOffset):
    msg = ""
    if encryptionOffset != 0:
        for c in story:
            if c.isalpha():
                character = str(c)
                oldAscii = ord(character)
                newAscii = int(oldAscii) + encryptionOffset

                if newAscii > ASCII_UPPER_LIMIT_VALUE:
                    newAscii = newAscii - ASCII_RANGE_VALID_VALUE
                elif newAscii < ASCII_LOWER_LIMIT_VALUE:
                    newAscii = newAscii + ASCII_RANGE_VALID_VALUE
                else:
                    pass
                msg += chr(newAscii)
            else:
                character = str(c)
                msg += character
    else:
        msg = story

    return msg


def DoDecrypt(story, decryptionOffset):
    msg = ""
    for c in story:
        if c.isalpha():
            character = str(c)
            oldAscii = ord(character)
            newAscii = int(oldAscii) + decryptionOffset

            if newAscii > ASCII_UPPER_LIMIT_VALUE:
                newAscii = newAscii - ASCII_RANGE_VALID_VALUE
            elif newAscii < ASCII_LOWER_LIMIT_VALUE:
                newAscii = newAscii + ASCII_RANGE_VALID_VALUE
            else:
                pass
            msg += chr(newAscii)
        else:
            character = str(c)
            msg += character

    return msg


# Description
#    Decifra il testo del messaggio utilizzando l'offset nel verso opposto.
#
# Params
#    @story: testo del messaggio cifrato.
#    @decryptionOffset: offset da applicare ai caratteri del messaggio per la
#    decifratura.
#    @encryptionOffsetSign: indica se il messaggio è stato cifrato con offset
#    positivo o negativo.
#
# Returns
#    Restituisce il messaggio in chiaro.
def Decrypt(story, decryptionOffset, encryptionOffsetSign):
    msg = ""
    if decryptionOffset != 0:
        if encryptionOffsetSign == '+':
            # La cifratura è stata applicata con offset positivo
            if decryptionOffset < 0:
                msg = DoDecrypt(story, decryptionOffset)
            else:
                msg = DoDecrypt(story, -decryptionOffset)

        elif encryptionOffsetSign == '-':
            # La cifratura è stata applicata con offset negativo
            if decryptionOffset < 0:
                msg = DoDecrypt(story, -decryptionOffset)
            else:
                msg = DoDecrypt(story, decryptionOffset)
        else:
            pass
    else:
        msg = story

    return msg


# Bruteforce attack
def DoMatchCheck(hackedMsg, wordsCollection):
    i = 0
    matches = []
    hackedMsgLen = len(hackedMsg.split())

    # posso usare direttamente la meta delle parole tanto sono sufficienti per
    # far match con il dizionario
    # per velocizzarlo di quasi 2s posso anche arrivare a n/3, n/4 perche
    # sarebbero 2000 parole
    # n/10 equivale a 1000 parole e sono abbastanza
    while i < hackedMsgLen / 10:
        word = hackedMsg.split()[i]
        if wordsCollection.__contains__(word):
            matches.append(True)
        else:
            matches.append(False)
        i += 1

    return matches


# Bruteforce attack (Ver. 1)
def TryBruteforceAttack(encryptedMsg, wordsCollection):
    msg = None
    posMatches = []
    negMatches = []

    bruteforceOfst = MIN_OFFSET_ATTACK
    while bruteforceOfst < MAX_OFFSET_ATTACK + 1:

        posHackedMsg = DoDecrypt(encryptedMsg, bruteforceOfst)
        negHackedMsg = DoDecrypt(encryptedMsg, -bruteforceOfst)
        posMatches = DoMatchCheck(posHackedMsg, wordsCollection)
        negMatches = DoMatchCheck(negHackedMsg, wordsCollection)

        # Calcolo percentuali dei match per offset positivo e negativo
        posPercent = (float(posMatches.count(True)) / float(len(posMatches))) * 100
        negPercent = (float(negMatches.count(True)) / float(len(negMatches))) * 100

        posMatchPercents[str(bruteforceOfst)] = str(round(posPercent, 1))
        negMatchPercents[str(-bruteforceOfst)] = str(round(negPercent, 1))

        # Percentuale di successo fissata a +80%.
        if int(posPercent) > BRUTEFORCE_SUCCESS_RATE:
            bruteforceOfstFound = bruteforceOfst
            file = open("STORY_BRUTEFORCE.txt", "w")
            file.write(posHackedMsg)
            msg = posHackedMsg
            bruteforceOfst = MAX_OFFSET_ATTACK

        elif int(negPercent) > BRUTEFORCE_SUCCESS_RATE:
            bruteforceOfstFound = -bruteforceOfst
            file = open("STORY_BRUTEFORCE.txt", "w")
            file.write(negHackedMsg)
            msg = negHackedMsg
            bruteforceOfst = MAX_OFFSET_ATTACK
        else:
            bruteforceOfstFound = None

        bruteforceOfst += 1

    return msg, bruteforceOfstFound


# Bruteforce attack (Ver. 2)
def TryBruteforcingAttack(cipherText, wordsCollection):
    msg = None
    posMatches = []
    negMatches = []

    bruteforceOfst = MIN_OFFSET_ATTACK
    while bruteforceOfst < MAX_OFFSET_ATTACK + 1:

        posHackedMsg = CaesarDecode(cipherText, bruteforceOfst, alphabet)
        negHackedMsg = CaesarDecode(cipherText, -bruteforceOfst, alphabet)

        posMatches = DoMatchCheck(posHackedMsg, wordsCollection)
        negMatches = DoMatchCheck(negHackedMsg, wordsCollection)

        # Calcolo percentuali dei match per offset positivo e negativo
        posPercent = (float(posMatches.count(True)) / float(len(posMatches))) * 100
        negPercent = (float(negMatches.count(True)) / float(len(negMatches))) * 100

        posMatchPercents[str(bruteforceOfst)] = str(round(posPercent, 1))
        negMatchPercents[str(-bruteforceOfst)] = str(round(negPercent, 1))

        # Percentuale di successo fissata a +80%.
        if int(posPercent) > BRUTEFORCE_SUCCESS_RATE:
            bruteforceOfstFound = bruteforceOfst
            file = open("STORY_BRUTEFORCE.txt", "w")
            file.write(posHackedMsg)
            msg = posHackedMsg
            bruteforceOfst = MAX_OFFSET_ATTACK

        elif int(negPercent) > BRUTEFORCE_SUCCESS_RATE:
            bruteforceOfstFound = -bruteforceOfst
            file = open("STORY_BRUTEFORCE.txt", "w")
            file.write(negHackedMsg)
            msg = negHackedMsg
            bruteforceOfst = MAX_OFFSET_ATTACK
        else:
            bruteforceOfstFound = None

        bruteforceOfst += 1

    return msg, bruteforceOfstFound


# Frequency attack
def GetMsgChars(encryptedMsg):
    msg = []
    recurChars = ""

    msg.append(str(
        encryptedMsg.replace(".", " ").replace("'", " ").replace(";", " ").replace(":", " ").replace("!", " ").replace(
            "?", " ").replace("/", " ").replace("'\'", " ").replace(',', " ").replace("#", " ").replace("@",
                                                                                                        " ").replace(
            "$", " ").replace("&", " ").replace(")", " ").replace('"', " ").replace("-", " ").replace("°", " ").replace(
            "(", " ").split()))

    for word in ast.literal_eval(str(msg)):
        for c in word:
            if c.isalpha():
                recurChars += c + ' '

    return recurChars


# Frequency attack
def GetRecurrentChars(ofstChars):
    ofstCharsLen = float(len(ofstChars))
    charsList = []

    # Crea lista dei caratteri, occorrenze e frequenza presenti nel brano.
    if ofstCharsLen == 0:
        return None
    else:
        i = 0
        while i < len(alphabet):
            charsList.append({'letter': alphabet[i],
                              'occ': ofstChars.count(alphabet[i]),
                              'freq': round(float(ofstChars.count(alphabet[i])) / ofstCharsLen * 100, 2)})
            i += 1

    # Crea lista ordinata per frequenza in ordine decrescente.
    sortedListByFreq = sorted(charsList, key=lambda k: (int(k['freq'])), reverse=True)[:10]
    mostUsedChars = ""

    # Crea la stringa con i caratteri maggiormente utilizzati
    i = 0
    while i < len(sortedListByFreq):
        mostUsedChars += sortedListByFreq[i]['letter'] + ','
        i += 1

    return mostUsedChars


# Frequency attack
def TryFrequencyAttack(encryptedMsg, charsCollection):
    msg = None
    resultChars = ""
    posCharsCollection = []
    negCharsCollection = []
    frequencyOfst = MIN_OFFSET_ATTACK

    while frequencyOfst < MAX_OFFSET_ATTACK + 1:
        posHackedMsg = DoDecrypt(encryptedMsg, frequencyOfst)
        negHackedMsg = DoDecrypt(encryptedMsg, -frequencyOfst)

        posChars = GetMsgChars(posHackedMsg)
        negChars = GetMsgChars(negHackedMsg)

        # Inizializza file json
        jsonPosCollection = json.dumps(posCharsCollection)
        jsonNegCollection = json.dumps(negCharsCollection)

        mostUsedPosChars = GetRecurrentChars(posChars)
        mostUsedNegChars = GetRecurrentChars(negChars)

        if mostUsedPosChars is not None and mostUsedNegChars is not None:
            # Verifica il match delle due stringhe decifrate con quelle di Conan Doyle
            #
            # Tecnica di confronto usando le operazioni sui set (operazioni insiemistiche)
            # Tecnica alternativa: uso di Counter (vedi primo link)
            #
            # Sources:
            # https://stackoverflow.com/questions/21903842/how-do-i-compare-two-strings-in-python
            # https://www.programiz.com/python-programming/set
            # https://stackoverflow.com/questions/21191259/returning-boolean-if-set-is-empty
            #
            if set(mostUsedPosChars).difference(set(charsCollection)) == set():
                msg = posHackedMsg
                resultChars = mostUsedPosChars
                break

            elif set(mostUsedNegChars).difference(set(charsCollection)) == set():
                msg = negHackedMsg
                resultChars = mostUsedNegChars
                frequencyOfst = -frequencyOfst
                break

            else:
                frequencyOfst += 1

    file = open("STORY_FREQUENCE.txt", "w")
    file.write(msg)

    return frequencyOfst, resultChars


def CreateFrequencyDictonary():
    storyBooks = []
    frqChars = []
    bookLetters = ""

    i = 0
    while i < BOOKS_COUNT:
        file = open(books[i], "r")

        # Create the list of all parsed books
        storyBooks.append(str(file.read().lower().replace(".", " ").replace(
            "'", " ").replace(";", " ").replace(":", " ").replace("!", " ").replace(
            "?", " ").replace("/", " ").replace("'\'", " ").replace(',', " ").replace(
            "#", " ").replace("@", " ").replace("$", " ").replace("&", " ").replace(
            ")", " ").replace('"', " ").replace("-", " ").replace("°", " ").replace("(", " ").split()))

        # Create array with all book's characters
        for word in ast.literal_eval(storyBooks[i]):
            for c in word:
                if c.isalpha():
                    bookLetters += c + ' '
        i += 1

    # Create the list of dictionaries with all frequencies
    bookLettersLen = float(len(bookLetters))
    if bookLettersLen != 0:
        i = 0
        while i < ASCII_RANGE_VALID_VALUE:
            frqChars.append({'letter': alphabet[i],
                             'occ': bookLetters.count(alphabet[i]),
                             'freq': round(float(bookLetters.count(alphabet[i])) / bookLettersLen * 100, 2)})
            i += 1

    # Open and format the file to JSON standard
    with open('dictionary_letters.txt', 'w') as outfile:
        jsonDict = json.dumps(frqChars)
        outfile.write(jsonDict)

    # Save our changes to JSON file
    jsonFile = open("dictionary_letters.txt", "w+")
    jsonFile.write(json.dumps(frqChars))
    jsonFile.close()


def CreateWordsDictionary():
    storyBooks = []
    wordsList = ""

    i = 0
    while i < BOOKS_COUNT:
        file = open(books[i], "r")

        # Create the list of all parsed books
        storyBooks.append(str(file.read().lower().replace(".", " ").replace(
            "'", " ").replace(";", " ").replace(":", " ").replace("!", " ").replace(
            "?", " ").replace("/", " ").replace("'\'", " ").replace(',', " ").replace(
            "#", " ").replace("@", " ").replace("$", " ").replace("&", " ").replace(
            ")", " ").replace('"', " ").replace("-", " ").replace("°", " ").replace("(", " ").split()))

        # Create array with all book's words
        for word in ast.literal_eval(storyBooks[i]):
            if not wordsList.__contains__(word):
                wordsList += word + '\n'
        i += 1

    file = open("dictionary_words.txt", "w")
    file.write(wordsList)


##
## CRYPTOGRAPH USING MAKETRANS FOR SUBSTITUTION AND CAESAR CIPHERS
## Source: http://www.stealthcopter.com/blog/2009/12/python-cryptograph-using-maketrans-for-substitution-and-caesar-ciphers/
##
# Return the crypted/decoded text
def Translator(text, alphabet, key):
    trantab = maketrans(alphabet, key)
    return text.translate(trantab)


# Cipher the text
def CaesarEncode(plainText, shift, alphabet):
    return Translator(plainText, alphabet, alphabet[shift:] + alphabet[:shift])


# Decode the text
def CaesarDecode(cipherText, shift, alphabet):
    return Translator(cipherText, alphabet, alphabet[-shift:] + alphabet[:-shift])


def SubstitutionEncode(plainText, alphabet):
    randarray = range(0, len(alphabet))
    shuffle(randarray)

    key = ""
    for i in range(0, len(alphabet)):
        key += alphabet[randarray[i]]

    return Translator(plainText, alphabet, key), key


def SubstitutionDecode(cipherText, key, alphabet):
    return Translator(cipherText, key, alphabet)


print '\nchoose:'

int_option = None
while int_option is None:

    print '0) dizionario'
    print '1) scegli file'
    print '2) cifra'
    print '3) decifra'
    print '4) ricevi'
    print '5) invia'
    print '6) attacco bruteforce'
    print '7) attacco per frequenza'

    try:
        option1 = raw_input()
    except SyntaxError:
        option = None

    if option1 == '0':
        print '1) per lettere'
        print '2) per parole'
        print '3) array delle lettere piu usate'

        opt = raw_input()

        #### LETTERE ####
        if opt == '1':
            print "Creating dictionary of letters..."
            CreateFrequencyDictonary()
            print "dictionary_letters created!\n\n"

        #### PAROLE #####
        elif opt == '2':
            print 'Creating dictionary of words...'
            CreateWordsDictionary()
            print "dictionary_words created!\n\n"

        ### LETTERE PIU' USATE ###
        elif opt == '3':
            with open('dictionary_letters.txt') as input_file:
                data_loaded = json.load(input_file)

            # mi serve per capire Conan Doyle quali lettere usa maggiormente
            # ordino in ordine decrescente la frequenza delle lettere!
            sorted_list = sorted(data_loaded, key=lambda k: (int(k['freq'])), reverse=True)[:10]
            # sorted_list.take(5) equivalente in python sorted_list[:5]
            # print sorted_list[:10]

            num = 0
            while num < len(sorted_list):
                letter_more_used += (sorted_list[num]['letter']) + ','
                num += 1

            # stampo e elimino il punto e virgola finale con [:-1] equivale ad
            # un remove.last()
            print letter_more_used[:-1]

            file = open("letters_more_used.txt", "w")
            file.write(letter_more_used[:-1])

            print "letters_more_used created!\n\n"

    # o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o

    # SHOW BOOKS LIST
    # stampo i file da selezionare
    elif option1 == '1':
        i = 0
        for num in books:
            print '\t' + str(i) + ') ' + books[i]
            i = i + 1

        try:
            file_choosen = raw_input()
        except SyntaxError:
            option = None

    # o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o

    # ENCRYPTION
    elif option1 == '2':
        print 'the book choosen is: ' + books[int(file_choosen)]

        file = open(books[int(file_choosen)], "r+")
        story = file.read().lower()

        print 'insert OFFSET: (+2) (-2)'
        offset = raw_input()

        # encryptedStory = DoEncrypt(story, int(offset))
        # if int(offset) >= 0:
        #    encryptionOffsetSign = '+'
        # else:
        #    encryptionOffsetSign = '-'
        # file = open("STORY_CIPHER.txt", "w")
        # file.write(encryptedStory)
        # print "story_cipher created!\n\n"

        cipherText = ""
        if offset != "":
            cipherText = CaesarEncode(story, int(offset), alphabet)
        else:
            print 'Input Error! Valid range: [0 - +/-26]'

        file = open("STORY_CIPHER.txt", "w")

        if cipherText != "":
            file.write(cipherText)
            print "story_cipher created!\n"
        else:
            print "story_cipher not created!\n\n"
        print

    # o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o

    # DECRYPTION
    elif option1 == '3':
        print 'the book to decipher is: ' + books[int(file_choosen)]

        file = open("STORY_CIPHER.txt", "r+")
        story = file.read()

        print 'insert OFFSET known:'
        offset = raw_input()

        # decryptedStory = Decrypt(story, int(offset), encryptionOffsetSign)
        # file = open("STORY_CLEAR.txt", "w")
        # file.write(decryptedStory)
        # print "story_clear created!\n\n"

        plainText = ""
        if offset != "":
            plainText = CaesarDecode(story, int(offset), alphabet)
        else:
            print 'Input Error! Valid range: [0 - +/-26]'

        file = open("STORY_CLEAR.txt", "w")

        if plainText != "":
            file.write(plainText)
            print "story_clear created!\n"
        else:
            print "story_clear not created!\n\n"
        print

    # o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o

    # RECEIVE FILE WITH NETCAT
    elif option1 == '4':
        print 'waiting...'
        os.system('sudo nc -l -p 3333 | pv -rb > ' + books[int(file_choosen)])

    # o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o

    # SEND FILE WITH NETCAT
    elif option1 == '5':
        print 'sending with netcat'
        print "insert ip target:"
        ip = raw_input()
        os.system('sudo pv ' + books[int(file_choosen)] + ' | nc -w 1 ' + ip + ' 3333')

    # o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o

    # BRUTEFORCE ATTACK
    # (Usa tutte le combinazioni possibili per decifrare il messaggio)
    elif option1 == '6':
        print 'the book to hacking is: ' + books[int(file_choosen)] + '\n'

        print books[int(file_choosen)]

        # apro il file cifrato
        file = open('STORY_CIPHER.txt', "r+")
        cipherText = file.read()

        # apro il dizionario delle parole
        file1 = open('dictionary_words.txt', "r+")
        dictionary = file1.read()

        t_start = time.time()
        print "Brute forcing hack..."
        # hackedText, offset = TryBruteforceAttack(encryptedStory, dictionary)
        hackedText, offset = TryBruteforcingAttack(cipherText, dictionary)
        t_end = time.time()

        if hackedText is not None and offset is not None:
            if offset > 0:
                print 'Positive offset found!'
                print 'Offset: +' + str(offset) + ' '
                print 'Match percent: ' + posMatchPercents.get(str(offset)) + '%'
                print 'Time passed: ' + str(round((t_end - t_start), 1)) + 'sec\n'
                print "story_bruteforce created!\n\n"
            elif offset < 0:
                print 'Negative offset found!'
                print 'Offset: ' + str(offset) + ' '
                print 'Match percent: ' + negMatchPercents.get(str(offset)) + '%'
                print 'Time passed: ' + str(round((t_end - t_start), 1)) + 'sec\n'
                print "story_bruteforce created!\n\n"
            else:
                pass
        else:
            print "ERROR: story_bruteforce not created!\n\n"

    # o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o

    # FREQUENCE ATTACK
    elif option1 == '7':
        print 'the book to hacking is: ' + books[int(file_choosen)] + '\n'

        print books[int(file_choosen)]

        # apro il file cifrato
        file = open('STORY_CIPHER.txt', "r+")
        story_cipher = file.read()

        # (inizio l'attacco per frequenza!)
        # mi calcolo le occorrenze delle lettere del cifrato, scopo ultimo
        # ovviamente risalire all'offset usato

        letter_more_used = open("letters_more_used.txt", "r").read()
        print 'deve fare match con quello di Conan Doyle: [' + letter_more_used + ']'

        t_start = time.time()
        print "Frequency analysis hack..."
        result = TryFrequencyAttack(story_cipher, letter_more_used)
        t_end = time.time()

        if result is not None:
            if result[0] > 0:
                print 'Positive offset found!'
                print 'Offset: +%d' % result[0]
                print 'Match characters found: [' + result[1] + ']'
                print 'Time passed: ' + str(round((t_end - t_start), 1)) + 'sec\n'
            elif result[0] < 0:
                print 'Negative offset found!'
                print 'Offset: %d' % result[0]
                print 'Match characters found: [' + result[1] + ']'
                # print 'Offset: %d' % frequencyOfstFound
                print 'Time passed: ' + str(round((t_end - t_start), 1)) + 'sec\n'
            else:
                pass

        print 'story_frequence.txt created!\n\n'

    # o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o o

    else:
        print "ERROR"
