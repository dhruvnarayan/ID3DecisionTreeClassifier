import csv


def parse(filename):
    """
     takes a filename and returns attribute information and all the data in array of dictionaries
    """
    out = []
    
    csvfile = open(filename, 'r')
    fileRead = csv.reader(csvfile)
    headers = next(fileRead)
    # iterate through rows of actual data
    for row in fileRead:
        out.append(dict(zip(headers, row)))

    return out
