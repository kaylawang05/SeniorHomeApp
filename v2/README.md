# Senior Home App

## Pre-requisites
- You need to be on Python 3.10 or above
- Install fuzzywuzzy module by running `pip3 install fuzzywuzzy`

## How to run
Run `pip install -r requirements.txt` and then to run the code, run `python3 main.py`

## Some Notes
`apartment.py` contains the `Apartment` class which represents an apartment in the `ApartmentDatabase`. This database is saved and loaded from `apt.json`. You can add or set apartments to `ApartmentDatabase` and you can add or remove tenants or visitors. Something that could possibly return an error has the return type of `Result[type, Error]` where type represents the value returned by the function and Error represents a possible error that could be returned instead. `Error` as well as its subtypes are in `errors.py`. When using these functions, you can either call `.unwrap()` on them to unwrap the value from the `Result` container or crash if it is an `Error` instead. You can also use the `match` statement to handle the errors yourself. 

Here is an example of using `Result`
```python
# here is an example of error handling
def safe_div(a, b):
    if b == 0:
        return Failure(ZeroDivisionError())
    return Success(a/b)

x = safe_div(10,2).unwrap()
print(x) # 5

print(safe_div(10,2)) # Success(5)

print(safe_div(1,0)) # Failure(ZeroDivisionError)

print(safe_div(1,0).unwrap()) # *crashes*

# using a match statement
match safe_div(12,6):
    case Success(x): # Notice, you can pattern match on parts of the Success and Failure containers
        print(f"Successfully executed, the answer is {x}")
    case Failure(m):
        print(f"Ran into an erro: {m}")
```

`visit.py` has the `VisitorManager` class which manages current visitors and logs their visits in CSV files in `./visitor-logs`. When a new visitor comes, which means it is not in the database, their name is added to `apt.json`. If they are already a known visitor, i.e. they are in `apt.json` for that apartment, they are just kept track by the `VisitorManager`. If two people visit the same room with the same name (unlikely but still possible) the sign-in code just adds them to the currently tracked visitors in `VisitorManager` but does not add them to `apt.json` because we do not want duplicate names in there.

Here is an example of using the API
```python
from returns.result import Result, Failure, Success # Failure and Success are different variants for Result

from apartment import Apartment, ApartmentDatabase
from visit import VisitorManager

apt = Apartment(number=1234, tenants=["alice"], vistors=["bob", "cindy"]) # create a new apartment

apts = ApartmentDatabase("./data/apt.json") # create a new apartment database

match apts.remove_tenant(69, "david"):
    case Success(_): # If the operation is a Success, we do not care what is inside Success
        print("successfully removed david from room 69")
    case Failure(x): # If the operation is a Failure, print the failure
        print(x)

# If we want to crash on a failure, we can do this instead
apts.remove_tenant(69, "david").unwrap()

apts.save() # save database to file

# Visitor manager example
vm = VisitorManager(apts, "./visitor-logs")
vm.sign_in(69, "ethan").unwrap()  # sign in visitor ethan from room 69
vm.sign_out(69, "ethan").unwrap() # sign out visitor ethan from room 69
```
