import csv

#Read a csv file from a given path
def readCSV(filepath):
    
    result = []
    
    with open(filepath,'r') as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        for row in reader:
            result.append({'username':row[0],'birthdate':row[1],'gender':row[2],'voted':row[3]})
            
    return result
    