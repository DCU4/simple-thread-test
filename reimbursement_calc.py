from datetime import date

def calculate_reimbursement(project):
    total = 0
    # TODO: multiple projects
    # for project in projects: 
    #     calculate...
    
    f_days = get_full_days(project["start_date"], project["end_date"])
    t_days = get_travel_days(project["start_date"], project["end_date"])
    city_rates = get_city_rates(project["city"]) # H or L
    print(f_days, t_days, city_rates)
    # is this the best way?
    total = (f_days * city_rates["full"]) + (t_days * city_rates["travel"])
    print(total)
    return total


def get_full_days(start_date, end_date):
    m,d,y = start_date.split('/')
    start = date(int(y), int(m), int(d))
    m,d,y = end_date.split('/')
    end = date(int(y), int(m), int(d))
    print(start, end)
    delta = (end - start)
    print(delta)
    # delta = difference between days, so subtract 1 for other travel day
    full_days = delta.days - 1
    if full_days >= 1:
        return full_days
    else:
        return 0


def get_travel_days(start_date, end_date):
    m,d,y = start_date.split('/')
    m,d,y = end_date.split('/')
    start = date(int(y), int(m), int(d))
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