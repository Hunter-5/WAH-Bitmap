'''Creator: William Purviance   william.purviance@wsu.edu   3/2/19
    Description: Creates a bitmap of an animals.txt file, a bitmap
    of a sorted animals.txt file, and a 32 and 64 bit word compression
    for both bitmaps.'''

def make_bitmap(animals_file, bitmap):
    '''Creates bitmap index for assignment 4 data.
    Requires file to index, and a file for writing
    to the index.'''
    file = open(animals_file, "r")
    new_file = open(bitmap, "w")

    # Bit mapping of animal attribute.
    animals = {
        "cat": "1000",
        "dog": "0100",
        "turtle": "0010",
        "bird": "0001"
    }

    for line in file:
        age_bin = "0000000000" # Binary columns for age, set to zero.
        animal, age, adopted = line.split(',')
        new_file.write(animals[animal]) # Write animal bites to file.

        age_index = -(-int(age)//10) # Determine location of bite index for age.
        age_bin = age_bin[:age_index-1] + "1" + age_bin[age_index:] # Set bite to '1' for calculated index.
        new_file.write(age_bin)

        # Writes the adopted bit info
        if adopted == "True\n":
            new_file.write("10\n")
        elif adopted == "False\n":
            new_file.write("01\n")
    
    file.close()
    new_file.close()

def order_animals(animals_file):
    '''Creates an ordered list of animal data.
    Requires txt file of animal data'''
    file = open(animals_file, "r")
    new_file = open("animals_sorted.txt", "w")
    
    sorting = file.readlines()
    sorting.sort()

    for line in sorting:
        new_file.write(line)

    file.close()
    new_file.close()

def isLiteral(bitstring):
    '''Determines if a string of bits is literal.
    Requires a string of bits.'''
    for b in bitstring: # If a dirty bit is found, we do not have a literal.
        if b != bitstring[0]:
            return True
    return False

# Compress bitmap index using 32-bit WAH.
def WAH(bitmap, compressed_file, bit):
    file = open(bitmap, "r")
    new_file = open(compressed_file, "w")

    bitmap_tuples = file.readlines()
    
    fill = 0 #
    literal = 0 #
    count = 0 # Number of runs
    column = []
    run_type = 0
    for column_number in range(16):
        # Capturing column as a string.
        for line in bitmap_tuples:
            column.append(line.rstrip()[column_number])
        column = ''.join(column)
        for index in range(0, len(column), bit-1):
            word = column[index:index + bit-1]
            if len(word) < bit-1: # End of bitmap reach and < bit-1.
                if count != 0:
                    new_file.write(run_type + "{:0{}b}".format(count, bit-2))
                    count = 0
                    run_type = 0
                literal += 1 #
                new_file.write("0" + word)
                continue
            elif isLiteral(word): # If it's a literal, just write it.
                if count != 0:
                    new_file.write(run_type + "{:0{}b}".format(count, bit-2))
                    count = 0
                    run_type = 0
                literal += 1 #
                new_file.write("0" + word)
                continue
            elif run_type != 0 and run_type != "1"+word[0]:
                # If a new run type is encountered, write old run
                # and begin new run.
                new_file.write(run_type + "{:0{}b}".format(count, bit-2))
                count = 0
            fill += 1 #
            run_type = "1" + word[0]
            count+=1
        new_file.write('\n')
        column = []

    print("fill = " + str(fill))
    print("literal = " + str(literal))

    file.close()
    new_file.close()
     
def main():
    make_bitmap("animals.txt", "animals_bitmap.txt") # Unsorted bitmap.
    order_animals("animals.txt") # Order animals file.
    make_bitmap("animals_sorted.txt", "animals_bitmap_sorted.txt") # Sorted bitmap.
    print("32 - Unsorted:")
    WAH("animals_bitmap.txt", "animals_compressed32.txt", 32) # Unsorted compressed. 32 bit.
    print("32 - Sorted:")
    WAH("animals_bitmap_sorted.txt", "animals_sorted_compressed32.txt", 32) # Sorted compressed. 32 bit.
    print("64 - Unsorted:")
    WAH("animals_bitmap.txt", "animals_compressed64.txt", 64) # Unsorted compressed. 64 bit.
    print("64 - Sorted:")
    WAH("animals_bitmap_sorted.txt", "animals_sorted_compressed64.txt", 64) # Unsorted compressed. 64 bit.

if __name__ == '__main__':
    main()
