import csv

def to_csv (data):
    '''
    data: (symbol: string, statement_type: string, matrix: 2d-list)

    return: None

    side effect: write "Symbol_statement_type.csv" to file system
    '''

    symbol, statement_type, matrix = data
    filename = symbol + '_' + statement_type.replace(' ', '_') + '.csv' 

    # Insert symbol and statement type
    matrix.insert(0, [symbol + " - " + statement_type + " Statement"])
    matrix.insert(2, [''])

    with open(filename, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', 
                quoting=csv.QUOTE_MINIMAL)

        for row in matrix:
            if len(row) > 1:
                spamwriter.writerow(row)
            elif len(row) == 1:
                # A section header/footer
                spamwriter.writerow([])
                spamwriter.writerow(row)
