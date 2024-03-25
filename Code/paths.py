import math

points = [(2,5,0),(2,2.5,2.5),(2,0.5,4.5),(4,0.5,6.5)] # X Y G

def equalSpacingPath(points):
    spacing = 0.1
    current_distance = 0.0
    current_idx = 0

    new_points = []

    while current_distance < points[-1][2]:
        if(current_idx < len(points)):
            if(current_distance > points[current_idx+1][2]):
                current_idx += 1
        progress = 1-(points[current_idx+1][2]-current_distance)/(points[current_idx+1][2]-points[current_idx][2])
        x=points[current_idx][0]+(points[current_idx+1][0]-points[current_idx][0])*progress
        y=points[current_idx][1]+(points[current_idx+1][1]-points[current_idx][1])*progress
        new_points.append((x,y))
        # print(str(new_points[-1][0])+","+str(new_points[-1][1]))
        current_distance += spacing

    return new_points

def smoothPath(path):
    new_points = []
    strength = 4
    for i in range(strength-1):
        path.insert(0,path[0])

    for pointIdx in range(len(path)):
        sumX = 0
        sumY = 0
        count = 0
        for next in path[pointIdx:pointIdx+strength]:
            sumX += next[0]
            sumY += next[1]
            count += 1

        new_points.append((sumX/count,sumY/count))
    return new_points

def getPathDistance(path):
    curr_distance = 0.0
    last_point = path[0]
    for pnt in path:
        dx = math.dist(last_point,pnt)
        if(dx>0.0):
            curr_distance += math.dist(pnt,last_point)
    return curr_distance

def timedPath(path,max_vel,accel):
    curr_speed = 0.0
    last_point = path[0]
    curr_distance = 0.0
    max_distance = getPathDistance(path)
    accel_distance = max_vel/accel
    curr_time = 0.0
    new_path = []
    for pnt in path:
        dx = math.dist(last_point,pnt)
        if(dx>0.0):
            dt = dx/curr_speed
            curr_distance += math.dist(pnt,last_point)
            curr_time += dt
            new_path.append((pnt,curr_time))

        if(curr_distance < max_vel):
            curr_speed += accel
            
        last_point = pnt

    return new_path

def distanceToTime(timedpath):
    new_points = []
    distance = 0.0
    for i in range(1,len(timedpath[1:])):
        lpnt = timedpath[i-1]
        pnt = timedpath[i]
        dx = math.dist(pnt[0],lpnt[0])
        distance += dx
        new_points.append((pnt[1],distance))

    return new_points

def format_desmos(points):
    for point in points:
        print(str(point[0])+","+str(point[1]))

# format_desmos(smoothPath(equalSpacingPath(points)))
smoothPath(equalSpacingPath(points))