from datetime import datetime

def calculate_reimbursement(projects):
    reimbursements = []
    projects = check_overlapping_projects(projects)
    projects = set_travel_sequence(projects)

    print(projects)
    for project in projects: 
        total = 0
        f_days = get_full_days(project)
        t_days = get_travel_days(project)
        city_rates = get_city_rates(project["city"]) # H or L
        print(f_days, city_rates["full"], t_days, city_rates["travel"])
        total = (f_days * city_rates["full"]) + (t_days * city_rates["travel"])
        reimbursements.append(total)
    # print(reimbursements)
    print('total',sum(reimbursements))
    # return sum(reimbursements)

    

def check_overlapping_projects(projects): 
    i = 0
    # if only one project
    if len(projects) <= 1:
        projects[0]["is_sequence"] = False
        projects[0]["is_travel_sequence"] = False
        return projects
    
    for project in projects:
        if i == 0:
            project["is_sequence"] = False
            project["is_overlapping"] = False
            project["overlapping_days"] = 0
            project["is_travel_sequence"] = False
            i += 1
            continue
        previous_project = projects[i-1] if i > 0 else None
        # check_contigious = 0
        # if previous_project is not None:
        check_contigious = parse_date(project["start_date"]) - parse_date(previous_project["end_date"])
        print('check_contigious.days', check_contigious.days)
        if(check_contigious.days < 0) :
            previous_project["is_sequence"] = True
            previous_project["is_overlapping"] = True
            project["is_sequence"] = True
            project["is_overlapping"] = True
            overlapping_days = parse_date(previous_project["end_date"]) - parse_date(previous_project["start_date"])
            project["overlapping_days"] = overlapping_days.days + 1
            previous_project["overlapping_days"] = 0

        elif (check_contigious.days == 1 or check_contigious.days == 0):
            previous_project["is_sequence"] = True
            project["is_sequence"] = True
            project["is_overlapping"] = False
        else:
            project["is_sequence"] = False
            project["is_overlapping"] = False
        i += 1
    return projects
            

    


def get_full_days(project):
    start = parse_date(project["start_date"])
    end = parse_date(project["end_date"])
    delta = (end - start)

    # delta = difference between days, so subtract 1 for other travel day
    # if sequence then include that day except end sequence
    full_days = delta.days - 1

    
    if project["is_sequence"] == True:
        
        # if sequence day AND overlapping, return all days from previous
        if project["is_overlapping"] == True:
            if project["overlapping_days"] > 0: 
                return delta.days - project["overlapping_days"]
            else :
                return delta.days + 1 if delta.days == 1 else delta.days

        # if sequence but not overlapping, then return all days except last day
        if project["is_travel_sequence"] == False:
            return delta.days
        elif project["is_travel_sequence"] == True:
            if delta.days == 0:
                return 0
            else :
              return delta.days
    
    # if not sequence, then just return full days
    if full_days >= 1:
        return full_days
    else:
        return 0


def get_travel_days(project):
    if project["is_sequence"] == True and project["is_travel_sequence"] == False:
        return 0
    if project["is_sequence"] == True and project["is_travel_sequence"] == True:
        return 1
    
    start = parse_date(project["start_date"])
    end = parse_date(project["end_date"])
    if start == end:
        return 1
    else: 
        return 2
    
def set_travel_sequence(projects):
    def set_default_travel_sequence(p):
        p["is_travel_sequence"] = False
        return p

    projects = list(map(set_default_travel_sequence, projects))

    find_first = lambda p: p["is_sequence"] == True
    first_seq = next(filter(find_first, projects), False) # first is_sequence
    if first_seq is not False:
        first_seq["is_travel_sequence"] = True

    reversed_set = reversed(projects)
    last_seq = next(filter(find_first, reversed_set), False) # last is_sequence
    if last_seq is not False:
        last_seq["is_travel_sequence"] = True

    return projects


def parse_date(date_str):
    return datetime.strptime(date_str, "%m/%d/%y").date()

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
    "start_date": "10/1/24",
    "end_date": "10/4/24",
    "city": "L"
},
{
    "start_date": "10/1/24",
    "end_date": "10/10/24",
    "city": "L"
}]
calculate_reimbursement(projects)



# Projects that are contiguous or overlap, with no gap between the end of one and the start of the next, 
# are considered a sequence of projects and should be treated similar to a single project.


projects = [{
    "start_date": "10/1/24",
    "end_date": "10/1/24",
    "city": "L"
},
{
    "start_date": "10/2/24",
    "end_date": "10/6/24",
    "city": "H"
},
{
    "start_date": "10/6/24",
    "end_date": "10/9/24",
    "city": "L"
}]
calculate_reimbursement(projects)


projects = [{
    "start_date": "9/30/24",
    "end_date": "10/3/24",
    "city": "L"
},
{
    "start_date": "10/5/24",
    "end_date": "10/7/24",
    "city": "H"
},
{
    "start_date": "10/8/24",
    "end_date": "10/8/24",
    "city": "H"
}]
calculate_reimbursement(projects)



# Any given day is only ever reimbursed once, even if multiple projects are on the same day.
projects = [{
    "start_date": "10/1/24",
    "end_date": "10/1/24",
    "city": "L"
},
{
    "start_date": "10/1/24",
    "end_date": "10/1/24",
    "city": "L"
},
{
    "start_date": "10/2/24",
    "end_date": "10/3/24",
    "city": "H"
},
{
    "start_date": "10/2/24",
    "end_date": "10/6/24",
    "city": "H"
}]
calculate_reimbursement(projects)
