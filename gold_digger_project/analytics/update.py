users = {}
mines = {}
games = 0

class Mine:
    gold = []
    move_optimal = []
    move_user = []
    number_of_mines = 0
    average_gold = 0
    average_optimal = 0
    average_user = 0

class User:
    gold = []
    move_optimal = []
    move_user = []
    number_of_mines = 0
    average_gold = 0
    average_optimal = 0
    average_user = 0

with open('../logs/log') as f:
    c = f.readlines()

for line in c:
    games += 1
    groups = str(line).split(' ')

    # Parse mines

    if groups[5] in mines.keys():
        mines[groups[5]].gold.append(groups[7])
        mines[groups[5]].move_optimal.append(groups[9])
        mines[groups[5]].move_user.append(groups[11])
        mines[groups[5]].number_of_mines += 1
    else:
        x = Mine()
        x.gold.append(groups[7])
        x.move_optimal.append(groups[9])
        x.move_user.append(groups[11])
        x.number_of_mines += 1
        mines[groups[5]] = x

    # Parse users

    if groups[3] in users.keys():
        users[groups[3]].gold.append(groups[7])
        users[groups[3]].move_optimal.append(groups[9])
        users[groups[3]].move_user.append(groups[11])
        users[groups[3]].number_of_mines += 1
    else:
        x = User()
        x.gold.append(groups[7])
        x.move_optimal.append(groups[9])
        x.move_user.append(groups[11])
        x.number_of_mines += 1
        users[groups[3]] = x

# Analyze data
print ''
print '============================== Mine statistics ============================== '
print ''
for key in mines.keys():
    # Average gold
    mines[key].total_gold = reduce(lambda x, y: int(x) + int(y), mines[key].gold)
    mines[key].average_gold =float( mines[key].total_gold) / mines[key].number_of_mines

    # Average optimal stopping point
    mines[key].total_optimal = reduce(lambda x, y: int(x) + int(y), mines[key].move_optimal)
    mines[key].average_optimal = float(mines[key].total_optimal) / mines[key].number_of_mines

    # Average user stopping point
    mines[key].total_user = reduce(lambda x, y: int(x) + int(y), mines[key].move_user)
    mines[key].average_user = float(mines[key].total_user) / mines[key].number_of_mines

    print 'Mine: ' + str(key)
    print 'Total gold: ' + str(mines[key].total_gold)
    print 'Average gold: ' + str(mines[key].average_gold)
    print 'Average optimal stopping point: ' + str(mines[key].average_optimal)
    print 'Average user stopping point: ' + str(mines[key].average_user)

print ''
print '============================== User statistics ============================== '
print ''

for key in users.keys():
    # Average gold
    users[key].total_gold = reduce(lambda x, y: int(x) + int(y), users[key].gold)
    users[key].average_gold = float(users[key].total_gold) / users[key].number_of_mines

    # Average optimal stopping point
    users[key].total_optimal = reduce(lambda x, y: int(x) + int(y), users[key].move_optimal)
    users[key].average_optimal = float(users[key].total_optimal) / users[key].number_of_mines

    # Average user stopping point
    users[key].total_user = reduce(lambda x, y: int(x) + int(y), users[key].move_user)
    users[key].average_user = float(users[key].total_user) / users[key].number_of_mines

    print 'Username: ' + str(key)
    print 'Total gold: ' + str(users[key].total_gold)
    print 'Average gold: ' + str(users[key].average_gold)
    print 'Average optimal stopping point: ' + str(users[key].average_optimal)
    print 'Average user stopping point: ' + str(users[key].average_user)














