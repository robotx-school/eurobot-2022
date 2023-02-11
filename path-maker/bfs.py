from collections import deque
import json
import time

def get_next_nodes(x, y, grid, cols, rows): 
    check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows and not grid[y][x] else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
    return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]



def bfs(start, goal, graph):
    queue = deque([start])
    visited = {start: None}

    while queue:
        cur_node = queue.popleft()
        if cur_node == goal:
            break

        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            if next_node not in visited:
                queue.append(next_node)
                visited[next_node] = cur_node
    
    return queue, visited

def main(grid, start, finish, x_delt, y_delt):
    # grid
    cols, rows = len(grid[0]), len(grid)
    print(f"Size: {cols, rows}")

    # dict of adjacency lists
    graph = {}
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if not col:
                graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y, grid, cols, rows)

    # BFS settings
    
    goal = start[0] - 1, start[1] - 1
    queue = deque([start])
    visited = {start: None}
    final_way = []

    mouse_pos = finish[0] - 1, finish[1] - 1
    queue, visited = bfs(start, mouse_pos, graph)
    goal = mouse_pos


    # draw path
    path_head, path_segment = goal, goal

    while path_segment and path_segment in visited:
        path_segment = visited[path_segment]
        if path_segment != None:
            final_way.append((path_segment[0] + x_delt, path_segment[1] + y_delt))
        else:
            break
    corercted_way_pnts = []
    curr_ind = 0
    final_way_ind = 0
    final_way = final_way[::-1]
    scaled_x, scaled_y = 0, 0
    while final_way_ind < len(final_way):
        if curr_ind != 0:
            #tmp_0 = corercted_way_pnts[-1][0]
            #tmp_1 = corercted_way_pnts[-1][1]
            tmp_0 = final_way[final_way_ind - 1][0]
            tmp_1 = final_way[final_way_ind - 1][1]
            #if skipped != (-1, -1):
            #    tmp_0, tmp_1 = skipped
            local_scale_x = int(final_way[final_way_ind][0] - tmp_0)
            local_scale_y = int(final_way[final_way_ind][1] - tmp_1)
            if corercted_way_pnts[curr_ind - 1][1] == final_way[final_way_ind][1]:
                print("Skip")
            elif local_scale_x == scaled_x and local_scale_y == scaled_y:
                print("Skip scaled")
            else:
                corercted_way_pnts.append((int(final_way[final_way_ind][0]), int(final_way[final_way_ind][1])))
                curr_ind += 1
            scaled_x, scaled_y = local_scale_x, local_scale_y


        else:
            corercted_way_pnts.append((int(final_way[0][0]), int(final_way[0][1])))
            curr_ind = 1
        final_way_ind += 1
    corercted_way_pnts.append((int(final_way[-1][0]), int(final_way[-1][1])))
    return corercted_way_pnts


if __name__ == "__main__":
    grid = [[0] * 500 for i in range(100)]
    strt_t = time.time()
    print(main(grid, (0, 0), (10, 10), 10, 10))
    print(time.time() - strt_t)