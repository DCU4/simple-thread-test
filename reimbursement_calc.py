from datetime import date

def calculate_reimbursement(projects):
    reimbursements = []
    # TODO: multiple projects
    for project in projects: 
        total = 0
        # calculate...
        f_days = get_full_days(project["start_date"], project["end_date"])
        t_days = get_travel_days(project["start_date"], project["end_date"])
        city_rates = get_city_rates(project["city"]) # H or L
        print(f_days, t_days, city_rates)
        # is this the best way? no
        total = (f_days * city_rates["full"]) + (t_days * city_rates["travel"])
        reimbursements.append(total)
    print(sum(reimbursements))
    return sum(reimbursements)


def get_full_days(start_date, end_date):
    m,d,y = start_date.split('/')
    start = date(int(y), int(m), int(d))
    m,d,y = end_date.split('/')
    end = date(int(y), int(m), int(d))
    # print(start, end)
    delta = (end - start)
    # print(delta)
    # delta = difference between days, so subtract 1 for other travel day
    full_days = delta.days - 1
    if full_days >= 1:
        return full_days
    else:
        return 0


def get_travel_days(start_date, end_date):
    m,d,y = start_date.split('/')
    start = date(int(y), int(m), int(d))
    m,d,y = end_date.split('/')
    end = date(int(y), int(m), int(d))
    if start == end:
        return 1
    else: 
        return 2
    

# basic dict for grabbing rates
def get_city_rates(city) :
    city_rates = {
        "H": {
            "travel": 55,
            "full" : 85
        },
        "L": {
            "travel": 45,
            "full" : 75
        }
    }
    return city_rates[city]


projects = [{
    "start_date": "10/1/2024",
    "end_date": "10/4/2024",
    "city": "L"
}]
calculate_reimbursement(projects)



# TODO: 
# Projects that are contiguous or overlap, with no gap between the end of one and the start of the next, 
# are considered a sequence of projects and should be treated similar to a single project.

# hmm so 10/6 is a full day, but which rate? split in half? lets do start date rate
projects = [{
    "start_date": "10/1/2024",
    "end_date": "10/1/2024",
    "city": "L"
},
{
    "start_date": "10/2/2024",
    "end_date": "10/6/2024",
    "city": "H"
},
{
    "start_date": "10/6/2024",
    "end_date": "10/9/2024",
    "city": "L"
}]
calculate_reimbursement(projects)

# 45
# 110 + 3*85 (255) = 365
# 90 + 2*75 = 240
# 650

projects = [{
    "start_date": "9/30/2024",
    "end_date": "10/3/2024",
    "city": "L"
},
{
    "start_date": "10/5/2024",
    "end_date": "10/7/2024",
    "city": "H"
},
{
    "start_date": "10/8/2024",
    "end_date": "10/8/2024",
    "city": "H"
}]
calculate_reimbursement(projects)

# 90 + 150 = 240
# 110 + 85 = 195
# 55
# 490

# TODO: 
# Any given day is only ever reimbursed once, even if multiple projects are on the same day.
projects = [{
    "start_date": "10/1/2024",
    "end_date": "10/1/2024",
    "city": "L"
},
{
    "start_date": "10/1/2024",
    "end_date": "10/1/2024",
    "city": "L"
},
{
    "start_date": "10/2/2024",
    "end_date": "10/6/2024",
    "city": "H"
},
{
    "start_date": "10/6/2024",
    "end_date": "10/9/2024",
    "city": "L"
}]
calculate_reimbursement(projects)
