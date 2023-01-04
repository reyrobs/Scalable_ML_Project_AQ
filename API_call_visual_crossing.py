import csv
import urllib.request
import sys
import codecs
import json

def csv_reader(it):
  for line in it:
    yield line.strip().split(',')

if __name__ == '__main__':
  try:
    ResultBytes = urllib.request.urlopen(
      "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Paris?unitGroup=us&include=days&key=SC6YQNXSJZYPRJHRAGWK63GDC&contentType=csv")
    # Parse the results as CSV
    CSVText = csv.reader(codecs.iterdecode(ResultBytes, 'utf-8'))
  except urllib.error.HTTPError as e:
    ErrorInfo = e.read().decode()
    print('Error code: ', e.code, ErrorInfo)
    sys.exit()
  except  urllib.error.URLError as e:
    ErrorInfo = e.read().decode()
    print('Error code: ', e.code, ErrorInfo)
    sys.exit()

  list_of_lists = []
  for row in CSVText:
    list_of_lists.append(row)
  with open('temp_file.csv', 'w', newline='', encoding='utf-8') as file_object:
    writer_object = csv.writer(file_object)
    for row in list_of_lists:
      writer_object.writerow(row)