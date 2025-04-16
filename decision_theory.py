# Name: Ben Croyle
# Topic: Decision Theory

graph = [[0.25, 0.35, 0.4], [0.35, 0.15, 0.5], [0.4, 0.5, 0.1]]
if graph[0][0] >= 5:
    print("Discounts are available")
if graph[0][1] >= 5:
    print("Prices remain the same")
if graph[0][2] >= 5:
    print("Prices are higher than usual")
if graph[1][0] >= 5:
    print("We can work with less workers than usual")
if graph[1][1] >= 5:
    print("Usual number of workers required")
if graph[1][2] >= 5:
    print("We need more workers than usual")
if graph[2][0] >= 5:
    print("We have more than enough equipment")
if graph[2][1] >= 5:
    print("We have just the right amount of equipment")
if graph[2][2] >= 5:
    print("We need more equipment")