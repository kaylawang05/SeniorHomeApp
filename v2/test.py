from backend import *

vm = VisitorManager(ApartmentDatabase("./data/apts.json"), "./visitor-logs")
vm.sign_in("david", 102).unwrap()
vm.sign_out("david", 102).unwrap()
vm.sign_in("bob", 102).unwrap()
vm.sign_in("clara", 102).unwrap()
vm.sign_out("bob", 102).unwrap()
vm.sign_out("clara", 102).unwrap()
