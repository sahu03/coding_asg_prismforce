import json
from datetime import datetime
from dateutil import rrule

data = json.load(open('1-input.json', 'r'))
 
bal_dict = {}  #Dictionary for calculating balance sheet data



for i in data["revenueData"]:                
    date_time= datetime.strptime(i["startDate"], '%Y-%m-%dT%H:%M:%S.000Z')
    key=date_time
    value=i["amount"]
    if date_time in list(bal_dict.keys()):
        bal_dict[key]=bal_dict[key]+value
    else:
         bal_dict[key]=value

for i in data["expenseData"]:
    date_time= datetime.strptime(i["startDate"], '%Y-%m-%dT%H:%M:%S.000Z')
    key=date_time
    value=i["amount"]
    if date_time in list(bal_dict.keys()):
        bal_dict[key]=bal_dict[key]-value
    else:
         bal_dict[key]=-value

datelist=bal_dict.keys()
end_date = max(datelist)
start_date = min(datelist)

bal_sheet={"balance":[]} # Balance sheet
for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
    temp={"amount":0,"startDate":dt.strftime('%Y-%m-%dT%H:%M:%S.000Z')}
    if dt in datelist:
        temp["amount"]=bal_dict[dt]
    else:
        temp["amount"]=0
    bal_sheet["balance"].append(temp)

json_object = json.dumps(bal_sheet, indent = 2)
  
with open("output.json", "w") as outfile:
    outfile.write(json_object)

print(bal_sheet)