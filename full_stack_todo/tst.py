people = [
    {"name": "Alice", "age": 25, "profession": "Engineer"},
    {"name": "Bob", "age": 35, "profession": "Writer"},
    {"name": "Charlie", "age": 45, "profession": "Chef"},
    {"name": "Diana", "age": 20, "profession": "Artist"},
    {"name": "Edward", "age": 50, "profession": "Doctor"}
]

new_dict = {
    (person["name"].upper() if person["age"] > 30 else person["name"]): 
    (person["age"], person["profession"].upper())
    for person in people if person["age"] > 20
}


for person in people:
    print(person['name'])
