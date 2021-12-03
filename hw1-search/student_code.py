from expand import expand

# 1) A*, will use the distances between places as the heuristic (how far you're from the destination).
# 2) A*, the distance from the start to your current location will be time-based, but the distance from your current
# location to the destination will be distance-based.
''' STEPS
*** Avoid expanding paths that are already expensive
1) USE the FN function for each node
    - Estimate of goodness
    - Expand best unexpanded node
    **********f(n) = g(n) + h(n)**********
    ->  g(n) = cost so far to reach n
    ->  h(n) = estimated cost from n to goal
    ->  f(n) = estimated total cost of path through n to goal
    ->  f(n) is the evaluation of the desirability of n.

2) A* uses straight-line distance (aka Euclidean distance) as a heuristic.
'''


def heuristic(dis_map, start, end):
    # Go to the distance map and get the distance between the two points (straight line)
    return dis_map[start][end]


def traveling_time_calc(time_map, start, end):
    # Go to the time map and get the time it takes to travel between the two points
    return time_map[start][end]


def a_star_search(dis_map, time_map, start, end):
    # Heuristic --> use the dis_map with euclidean distance
    # Graph --> time_map, use the times
    # Initializations
    traveling_times = {}
    # The traveling time from the start node to to itself is going to be 0
    traveling_times[start] = 0
    # This contains the priorities with which to visit the nodes, calculated using the heuristic.
    distances = {}
    # start node has a priority equal to straight line distance to goal. It will be the first to be expanded.
    distances[start] = heuristic(dis_map, start, end)
    # Create a list to save the heuristic values for each node:
    heuristic_value_per_node = {}
    heuristic_value_per_node[start] = heuristic(dis_map, start, end)
    # This contains whether a node was already previous_node
    previous_node = {}
    # Closed Vertices -> their children have been studied too
    closed_vertices = [[]]
    # Open Vertices
    open_vertices = [start]

    while len(open_vertices) > 0:
        # First step is to get the node from the open vertices with the shortest distance according to the heuristic
        current_vertex = None
        node_distance_score = None
        for vertex in open_vertices:
            if current_vertex is None or distances[vertex] < node_distance_score:
                # gets the smallest f(n) value, initializes values if it is the first node in the loop
                node_distance_score = distances[vertex]
                current_vertex = vertex
            # if two nodes have the same f(n) value then
            elif distances[vertex] == node_distance_score:
                # we expand the one with the smallest h(n) which is vertex
                if heuristic_value_per_node[vertex] < heuristic_value_per_node[current_vertex]:
                    # expand vertex as it has smaller h(n) value
                    print("f(n) of new vertex < old vertex")
                    # print("old vertex --> " , current_vertex)
                    # print("new vertex --> " , vertex)
                    node_distance_score = distances[vertex]
                    current_vertex = vertex
                elif heuristic_value_per_node[vertex] == heuristic_value_per_node[current_vertex]:
                    # expand current_vertex as it has smaller h(n) value, remove vertex from the list
                    # the two nodes have equal h(n) values, so we expand the current one and not the vertex
                    print("f(n) of new vertex == old vertex")
                    # print("old vertex --> ", current_vertex)
                    # print("new vertex --> ", vertex)
                    continue

        if goal_reached(current_vertex, end):
            # we have to find our way back to the beggining from the current_vertex
            followed_path = [current_vertex]
            while current_vertex in previous_node:
                current_vertex = previous_node[current_vertex]
                followed_path.append(current_vertex)
            # Now we have to reverse the list as we are tracing backwards
            followed_path.reverse()

            return followed_path

        # Remove from the open_vertices the current node and add it to the closed as we completed the path for this one
        open_vertices.remove(current_vertex)
        closed_vertices.append(current_vertex)

        # Now we have to get all the neighbours of the current node from the time map
        for child in expand(current_vertex, time_map):
            # Check if children is already in closed_vertices to avoid loops
            if child in closed_vertices:
                continue
            # Now calculate the time cost to move between the current vertex and the neighbor
            # it's goign to be the time we travleed so far + their difference
            current_traveling_time = traveling_times[current_vertex]
            # check if traveling time != None which means that no road connects these two vertices so we just skip
            estimated_traveling_time = traveling_time_calc(time_map, current_vertex, child)
            traveling_time = current_traveling_time + estimated_traveling_time

            # Check if neighbor is already in open_vertices, if not add
            if child not in open_vertices:
                open_vertices.append(child)
            elif traveling_time >= traveling_times[child]:
                # we dont want to get a higher traveling time..
                continue

            # update the previous_node list
            previous_node[child] = current_vertex
            traveling_times[child] = traveling_time
            # Get the heuristic calculation from the neighbor to the end node
            heur = heuristic(dis_map, child, end)
            heuristic_value_per_node[child] = heur
            print(child, " h(n) -> ", heuristic_value_per_node[child])
            # Calculate the f(n) function for the neighbor
            distances[child] = traveling_times[child] + heur
            print(child, " f(n) -> ", distances[child])


def breadth_first_search(time_map, start, end):
    explored = []
    # Queue for traversing the
    # graph in the BFS
    queue = [[start]]
    # If the desired node is
    # reached
    if goal_reached(start, end):
        return [start]

    # Loop to traverse the graph
    # with the help of the queue
    while queue:

        path = queue.pop(0)
        node = path[-1]
        # Condition to check if the
        # current node is not visited
        if goal_reached(node, end):
            print("\n"), print("The explored list is --> ", explored), print("The path is --> ", path)
            return path
        if node not in explored:
            # Condition to check if the
            # child node is the goal
            explored.append(node)
            children = expand(node, time_map)
            print("The children of the node ", node, ", are --> ", children)
            if len(children) > 0:
                # Loop to iterate over the
                # children of the node
                for child in children:
                    temp_path = list(path)
                    temp_path.append(child)
                    queue.append(temp_path)


def depth_first_search(time_map, start, end):
    node = list(start)
    # call the function to check if we reached the end
    if goal_reached(start,end):
        return node
    children = expand(start, time_map)
    # making sure to reverse the list
    children = children[::-1]

    for child in children:
        # recursively call to get the path
        path = depth_first_search(time_map, child, end)
        # check if path exists
        if path:
            # call the function to check if we reached the end , get the node at the end of the path
            if goal_reached(path[-1], end):
                node.extend(path)
                return node


def goal_reached(current, end):
    # custom function which checks whether the provided current node is the goal (end node), returns true if it is
    return current == end
