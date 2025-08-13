from datetime import date

def calculate_reimbursement(projects):
    reimbursements = []
    projects = check_overlapping_projects(projects)
    print(projects)
    for project in projects: 
        total = 0
        f_days = get_full_days(project["start_date"], project["end_date"], project["is_sequence"], project["is_end_sequence"])
        t_days = get_travel_days(project["start_date"], project["end_date"], project["is_sequence"])
        city_rates = get_city_rates(project["city"]) # H or L
        print(f_days, city_rates["full"], t_days, city_rates["travel"])
        total = (f_days * city_rates["full"]) + (t_days * city_rates["travel"])
        reimbursements.append(total)
    print(reimbursements)
    print(sum(reimbursements))
    return sum(reimbursements)


def check_overlapping_projects(projects): 
    end_date_check = ""
    i = 0
    for project in projects:
        t_days = get_travel_days(project["start_date"], project["end_date"], "false")
        previous_project = projects[i-1]
        project["is_end_sequence"] = "false"

        if t_days == 2: # not single days of travel
            if project["start_date"] == end_date_check:
                overlapping_project = project
                previous_project["is_sequence"] = "true"
                overlapping_project["is_sequence"] = "true"
                overlapping_project["is_end_sequence"] = "true"
                end_date_check = ""
            else:
                previous_project = projects[i-1]
                previous_project["is_sequence"] = "false"
        else :
            previous_project["is_sequence"] = "false"
    
        end_date_check = project['end_date']
        i += 1
    return projects

    

def get_full_days(start_date, end_date, is_sequence, is_end_sequence):
    m,d,y = start_date.split("/")
    start = date(int(y), int(m), int(d))
    m,d,y = end_date.split("/")
    end = date(int(y), int(m), int(d))
    delta = (end - start)

    # delta = difference between days, so subtract 1 for other travel day
    # if sequence then include that day except end sequence
    full_days = delta.days if is_sequence == "true" and is_end_sequence == "true" else delta.days - 1
  
    if full_days >= 1:
        return full_days
    else:
        return 0


def get_travel_days(start_date, end_date, is_sequence):
    m,d,y = start_date.split("/")
    start = date(int(y), int(m), int(d))
    m,d,y = end_date.split("/")
    end = date(int(y), int(m), int(d))
    if is_sequence == "true":
        return 1
    elif start == end:
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
# calculate_reimbursement(projects)



# Projects that are contiguous or overlap, with no gap between the end of one and the start of the next, 
# are considered a sequence of projects and should be treated similar to a single project.

# remove last day from previous project in sequence
# use all days as full except last for ending project 

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
# 55 + 45 + (3*75) + (3*85)
# 625

# wrong
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
