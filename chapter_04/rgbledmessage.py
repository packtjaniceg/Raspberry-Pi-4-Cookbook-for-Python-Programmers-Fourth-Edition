#!/usr/bin/python3
'''rgbledmessage.py'''
import os
import rgbled as RGBLED
import tilt as TILT

DEBUG = True

def read_message_file(filename):
    ''' Read letter formats from file '''
    assert os.path.exists(filename), \
           'Cannot find the message file: %s' % (filename)
    try:
        with open(filename, 'r') as the_file:
            file_content = the_file.readlines()
    except IOError:
        print("Unable to open %s" % (filename))
    if DEBUG: print("File Content START:")
    if DEBUG: print(file_content)
    if DEBUG: print("File Content END")
    dictionary = processfile_content(file_content)
    return dictionary

def processfile_content(content):
    ''' Gather letter formats together '''
    letter_format = [] #Will contain the format of each letter
    first_letter = True
    next_letter = False
    LETTERDIC = {}
    #Process each line that was in the file
    for line in content:
        # Ignore the # as comments
        if '#' in line:
            if DEBUG: print("Comment: %s"%line)
        #Check for " in the line = index name
        elif '"' in line:
            next_letter = True
            line = line.replace('"', '') #Remove " characters
            LETTER = line.rstrip()
            if DEBUG: print("Index: %s"%line)
        #Remaining lines are formatting codes
        else:
            #Skip first_letter until complete
            if first_letter:
                first_letter = False
                next_letter = False
                last_letter = LETTER
            #Move to next letter if needed
            if next_letter:
                next_letter = False
                LETTERDIC[last_letter] = letter_format[:]
                letter_format[:] = []
                last_letter = LETTER
            #Save the format data
            values = line.rstrip().split(' ')
            row = []
            for val in values:
                row.append(int(val))
            letter_format.append(row)
    LETTERDIC[last_letter] = letter_format[:]
    #Show letter patterns for debugging
    if DEBUG: print("LETTERDIC: %s" %LETTERDIC)
    if DEBUG: print("C: %s"%LETTERDIC['C'])
    if DEBUG: print("O: %s"%LETTERDIC['O'])
    return LETTERDIC

def create_buffer(message, dictionary):
    ''' Join letter patterns together '''
    buffer = []
    for letter in message:
        try:
            letter_pattern = dictionary[letter]
        except KeyError:
            if DEBUG: print("Unknown letter %s: use _"%letter)
            letter_pattern = dictionary['_']
        buffer = add_letter(letter_pattern, buffer)
    if DEBUG: print("Buffer: %s"%buffer)
    return buffer

def add_letter(letter, buffer):
    ''' Add letter pattern '''
    for row in letter:
        buffer.append(row)
    buffer.append([0, 0, 0, 0, 0])
    buffer.append([0, 0, 0, 0, 0])
    return buffer

def display_buffer(buffer):
    ''' Cycle through the buffer and display each line '''
    position = 0
    while True:
        if not TILT.tilt_moving():
            position = 0
        elif (position + 1) < len(buffer):
            position += 1
            if DEBUG: print("Pos:%s ROW:%s"%(position, buffer[position]))
        #RGBLED.rgbled_pov(buffer[position], RGBLED.RGB_GREEN, 0.002)
        RGBLED.rgbled_pov(buffer[position], RGBLED.RGB_BLUE, 0.002)
        #RGBLED.rgbled_pov(buffer[position], RGBLED.RGB_RED, 0.002)

def main():
    RGBLED.led_setup()
    TILT.tilt_setup()
    letter_dict = read_message_file('letters.txt')
    buffer = create_buffer('_COOKBOOK!', letter_dict)
    display_buffer(buffer)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Done")
    finally:
        RGBLED.led_cleanup()
        print("Closed Everything. END")
#End
