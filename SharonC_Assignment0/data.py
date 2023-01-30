import random

def RandomRow():
    row = ''
    for i in range(6):
        rowInt = random.randint(0,100)
        row += str(rowInt)
        if i != 5:
            row += ','
    return row

def WriteFile(outFile = 'data.csv', header = 'A,B,C,D,E,F'):
    file = open(outFile, 'w')

    for i in range(401):
        if i == 0:
            file.write(header)
        else:
            file.write(RandomRow())

        if i != 400:
            file.write('\n')

    file.close()

WriteFile()
