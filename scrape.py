## Scrape from Excel data tables finding intervals where string appears, in order to lookup postcode and data

import openpyxl as op

#Find Strings in Cells
def findStrInCell(stri,ws):
    for row in ws.iter_rows():
        for cell in row:
            if stri in str(cell.value):
               yield (cell.value, cell.row, cell.column)


#Input an array of integers and return ranges
def ranges(a):
    b = sorted(a)
    i = 0
    for j in xrange(1,len(b)):
        if b[j] > b[j-1]+1:
            yield (b[i],b[j-1])
            i = j
    yield (b[i], b[-1])

workb = op.load_workbook('Pers_Mortage_PCS_2016-q3.xlsx', read_only = True, data_only = True)
#wb.get_sheet_names()

worksheet = workb.worksheets[-1]

#print( list(findStrInCell("London",worksheet)), sep='\n' ) Python

foundList=list(findStrInCell("London",worksheet) )
rows=[]
for elem in foundList: rows.append(elem[1])

rangesList=list(ranges(rows))

print rangesList

print "finished"
