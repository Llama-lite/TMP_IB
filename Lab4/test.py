import re

with open("test_commands.txt", "r") as file:
    for line in file:
        range_match = re.match(r'(supplyDate|name|amount|special) (=|!=) (.+)', line.strip()[4:])
        if range_match:
            print("==========================", line.strip())
            for group in range_match.groups():
                print(group)