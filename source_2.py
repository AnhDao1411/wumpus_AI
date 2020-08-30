#global list
Breeze = []
Stench = []
Gold = []
Pit = []
Wumpus = []
Oke = []
Visited = []

clauses = []

def load_level(path):
    file = path
    with open(file) as f:
        size = int(f.readline())
        cave = [[room for room in row.strip().split('.')]
                for row in f.readlines()]
    if len(cave) != size:
        raise Exception('Not enough Row')
    for r in cave:
        if len(r) != size:
            raise Exception('Not enough Col')

    return size, cave


def init(size):
    for i in range(size):
        Breeze.append([False]*size)
        Stench.append([False]*size)
        Gold.append([False]*size)
        Pit.append([0]*size)
        Wumpus.append([0]*size)
        Oke.append([False]*size)
        Visited.append([False]*size)


def Agent_init_pos(size, cave):
    for i in range(size):
        for j in range(size):
            if 'A' in cave[i][j]:
                return (i, j)


def No_Wumpus_Around(pos, size, cave):
    x = pos[0]
    y = pos[1]
    if x-1 >= 0:
        if 'W' in cave[x-1][y]:
            return False
    if x+1 <= size-1:
        if 'W' in cave[x+1][y]:
            return False
    if y-1 >= 0:
        if 'W' in cave[x][y-1]:
            return False
    if y+1 <= size-1:
        if 'W' in cave[x][y+1]:
            return False
    return True


def Is_Wumpus_dead(pos, size, cave):
    x = pos[0]
    y = pos[1]
    if 'W' not in cave[x][y]:
        return False
    else:
        print('Shot wumpus successfully at ',x,y)
        cave[x][y] = cave[x][y].replace('W', '')
        if x-1 >= 0:
            if No_Wumpus_Around((x-1, y), size, cave):
                cave[x-1][y] = cave[x-1][y].replace('S', '')
        if x+1 <= size-1:
            if No_Wumpus_Around((x+1, y), size, cave):
                cave[x+1][y] = cave[x+1][y].replace('S', '')
        if y-1 >= 0:
            if No_Wumpus_Around((x, y-1), size, cave):
                cave[x][y-1] = cave[x][y-1].replace('S', '')
        if y+1 <= size-1:
            if No_Wumpus_Around((x, y+1), size, cave):
                cave[x][y+1] = cave[x][y+1].replace('S', '')
        return True


def found_Breeze(Breeze_pos, size):
    x = Breeze_pos[0]
    y = Breeze_pos[1]
    # x-1,y
    if (x-1 >= 0) and (not Visited[x-1][y]):
        if Wumpus[x-1][y]:
            Wumpus[x-1][y] -= 1
            if not Wumpus[x-1][y] and not Pit[x-1][y]:
                Oke[x-1][y] = True
        else:
            Pit[x-1][y] += 1
    # x+1,y
    if (x+1 <= size-1) and (not Visited[x+1][y]):
        if Wumpus[x+1][y]:
            Wumpus[x+1][y] -= 1
            if not Wumpus[x+1][y] and not Pit[x+1][y]:
                Oke[x+1][y] = True
        else:
            Pit[x+1][y] += 1
    # x,y-1
    if (y-1 >= 0) and (not Visited[x][y-1]):
        if Wumpus[x][y-1]:
            Wumpus[x][y-1] -= 1
            if not Wumpus[x][y-1] and not Pit[x][y-1]:
                Oke[x][y-1] = True
        else:
            Pit[x][y-1] += 1
    # x,y+1
    if (y+1 <= size-1) and (not Visited[x][y+1]):
        if Wumpus[x][y+1]:
            Wumpus[x][y+1] -= 1
            if not Wumpus[x][y+1] and not Pit[x][y+1]:
                Oke[x][y+1] = True
        else:
            Pit[x][y+1] += 1


def found_Stench(Stench_pos, size, shot, cave):
    x = Stench_pos[0]
    y = Stench_pos[1]
    # x-1,y
    if (x-1 >= 0) and (not Visited[x-1][y]):
        if Pit[x-1][y]:
            Pit[x-1][y] -= 1
            if not Pit[x-1][y] and not Wumpus[x-1][y]:
                Oke[x-1][y] = True
        else:
            Wumpus[x-1][y] += 1
            if Wumpus[x-1][y] > 1:
                shot.append(((x, y), (x-1, y)))
                if Is_Wumpus_dead((x-1, y), size, cave):
                    Oke[x - 1][y] = True
    # x+1,y
    if (x+1 <= size-1) and (not Visited[x+1][y]):
        if Pit[x+1][y]:
            Pit[x+1][y] -= 1
            if not Pit[x+1][y] and not Wumpus[x+1][y]:
                Oke[x+1][y] = True
        else:
            Wumpus[x+1][y] += 1
            if Wumpus[x+1][y] > 1:
                shot.append(((x, y), (x+1, y)))
                if Is_Wumpus_dead((x+1, y), size, cave):
                    Oke[x + 1][y] = True
    # x,y-1
    if (y-1 >= 0) and (not Visited[x][y-1]):
        if Pit[x][y-1]:
            Pit[x][y-1] -= 1
            if not Pit[x][y-1] and not Wumpus[x][y-1]:
                Oke[x][y-1] = True
        else:
            Wumpus[x][y-1] += 1
            if Wumpus[x][y-1] > 1:
                shot.append(((x, y), (x, y-1)))
                if Is_Wumpus_dead((x, y-1), size, cave):
                    Oke[x][y - 1] = True
    # x,y+1
    if (y+1 <= size-1) and (not Visited[x][y+1]):
        if Pit[x][y+1]:
            Pit[x][y+1] -= 1
            if not Pit[x][y+1] and not Wumpus[x][y+1]:
                Oke[x][y+1] = True
        else:
            Wumpus[x][y+1] += 1
            if Wumpus[x][y+1] > 1:
                shot.append(((x, y), (x, y+1)))
                if Is_Wumpus_dead((x, y+1), size, cave):
                    Oke[x][y + 1] = True


def found_BriSten(pos, size, shot, cave):
    x = pos[0]
    y = pos[1]
    # x-1,y
    if (x-1 >= 0) and (not Visited[x-1][y]):
        Wumpus[x-1][y] += 1
        if Wumpus[x-1][y] > 1:
            shot.append(((x, y), (x-1, y)))
            if Is_Wumpus_dead((x-1, y), size, cave):
                Oke[x - 1][y] = True
        Pit[x-1][y] += 1
    # x+1,y
    if (x+1 <= size-1) and (not Visited[x+1][y]):
        Wumpus[x+1][y] += 1
        if Wumpus[x+1][y] > 1:
            shot.append(((x, y), (x+1, y)))
            if Is_Wumpus_dead((x+1, y), size, cave):
                Oke[x + 1][y] = True
        Pit[x+1][y] += 1
    # x,y-1
    if (y-1 >= 0) and (not Visited[x][y-1]):
        Wumpus[x][y-1] += 1
        if Wumpus[x][y-1] > 1:
            shot.append(((x, y), (x, y-1)))
            if Is_Wumpus_dead((x, y-1), size, cave):
                Oke[x][y - 1] = True
        Pit[x][y-1] += 1
    # x,y+1
    if (y+1 <= size-1) and (not Visited[x][y+1]):
        Wumpus[x][y+1] += 1
        if Wumpus[x][y+1] > 1:
            shot.append(((x, y), (x, y+1)))
            if Is_Wumpus_dead((x, y+1), size, cave):
                Oke[x][y + 1] = True
        Pit[x][y+1] += 1

def create_clauses(breeze,stench,pos,size):
    Prove_Oke(pos)
    print('New_percept_at: ',pos[0],',',pos[1])
    x=pos[0]
    y=pos[1]
    if not breeze:
        if (x-1>=0) and (not Visited[x-1][y]):
            clauses.append(['-P',x-1,y])
            print('-P[ ',x-1,' ][ ',y,' ]')
        if (x+1 <= size-1) and (not Visited[x+1][y]):
            clauses.append(['-P',x+1,y])
            print('-P[ ',x+1,' ][ ',y,' ]')
        if (y-1>=0) and (not Visited[x][y-1]):
            clauses.append(['-P',x,y-1])
            print('-P[ ',x,' ][ ',y-1,' ]')
        if (y+1 <= size-1) and (not Visited[x][y+1]):
            clauses.append(['-P',x,y+1])
            print('-P[ ',x,' ][ ',y+1,' ]')
    else:
        temp = []
        if (x-1>=0) and (not Visited[x-1][y]):
            temp.append(['P',x-1,y])
        if (x+1 <= size-1) and (not Visited[x+1][y]):
            temp.append(['P',x+1,y])
        if (y-1>=0) and (not Visited[x][y-1]):
            temp.append(['P',x,y-1])
        if (y+1 <= size-1) and (not Visited[x][y+1]):
            temp.append(['P',x,y+1])
        clauses.append(temp)
        for i,ele in enumerate(temp):
            if i < len(temp)-1:
                print('P[ ',ele[1],' ][ ',ele[2],' ] OR',end =" ")
            else:
                print('P[ ',ele[1],' ][ ',ele[2],' ]')

    if not stench:
        if (x-1>=0) and (not Visited[x-1][y]):
            clauses.append(['-W',x-1,y])
            print('-W[ ',x-1,' ][ ',y,' ]')
        if (x+1 <= size-1) and (not Visited[x+1][y]):
            clauses.append(['-W',x+1,y])
            print('-W[ ',x+1,' ][ ',y,' ]')
        if (y-1>=0) and (not Visited[x][y-1]):
            clauses.append(['-W',x,y-1])
            print('-W[ ',x,' ][ ',y-1,' ]')
        if (y+1 <= size-1) and (not Visited[x][y+1]):
            clauses.append(['-W',x,y+1])
            print('-W[ ',x,' ][ ',y+1,' ]')
    else:
        temp = []
        if (x-1>=0) and (not Visited[x-1][y]):
            temp.append(['W',x-1,y])
        if (x+1 <= size-1) and (not Visited[x+1][y]):
            temp.append(['W',x+1,y])
        if (y-1>=0) and (not Visited[x][y-1]):
            temp.append(['W',x,y-1])
        if (y+1 <= size-1) and (not Visited[x][y+1]):
            temp.append(['W',x,y+1])
        clauses.append(temp)
        for i,ele in enumerate(temp):
            if i < len(temp)-1:
                print('W[ ',ele[1],' ][ ',ele[2],' ] OR',end =" ")
            else:
                print('W[ ',ele[1],' ][ ',ele[2],' ]')
                
    print('-----------------------------------')
    
def Prove_Oke(pos):
    if (['-P',pos[0],pos[1]] in clauses) and (['-W',pos[0],pos[1]] in clauses):
        print('-P[ ',pos[0],' ][ ',pos[1],' ] AND -W[ ',pos[0],' ][ ',pos[1],' ] -> OKE[ ',pos[0],' ][ ',pos[1],' ]')
        
def take_percept(pos, size, shot, cave):
    x = pos[0]
    y = pos[1]
    Oke[x][y] = True
    check_BS = False
    if 'B' in cave[x][y] and 'S' in cave[x][y]:
        Breeze[x][y] = True
        Stench[x][y] = True
        found_BriSten(pos, size, shot, cave)
        check_BS = True
        create_clauses(True,True,pos,size)
    elif 'B' in cave[x][y]:
        Breeze[x][y] = True
        found_Breeze(pos, size)
        check_BS = True
        create_clauses(True,False,pos,size)
    elif 'S' in cave[x][y]:
        Stench[x][y] = True
        found_Stench(pos, size, shot, cave)
        check_BS = True
        create_clauses(False,True,pos,size)
    if check_BS:
        return
    create_clauses(False,False,pos,size)
    # 4 cells around is OK
    # x-1,y
    if x-1 >= 0:
        Oke[x-1][y] = True
    # x+1,y
    if x+1 <= size-1:
        Oke[x+1][y] = True
    # x,y-1
    if y-1 >= 0:
        Oke[x][y-1] = True
    # x,y+1
    if y+1 <= size-1:
        Oke[x][y+1] = True


def find_Oke_pos(size):
    oke_pos = []
    for i in range(size):
        for j in range(size):
            if (Oke[i][j]) and (not Visited[i][j]):
                oke_pos.append((i, j))
    return oke_pos


def distance(pos1, pos2):
    return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])


def solution(trace, v, start):
    path_list = []
    while(trace[v[0]][v[1]] != -1):
        path_list.append(v)
        v = trace[v[0]][v[1]]
    path_list.append(start)
    path_list.reverse()
    return path_list


def BFS(agent_pos, goal_pos, size, cave):
    NotFree = [agent_pos]
    queue = [agent_pos]
    trace = []
    for i in range(size):
        trace.append([-1]*size)
    while queue:
        s = queue.pop(0)
        if s == goal_pos:
            return solution(trace, goal_pos, agent_pos)
        temp = (s[0]-1, s[1])
        if (temp[0] >= 0) and (temp not in NotFree) and (Visited[temp[0]][temp[1]]):
            queue.append(temp)
            NotFree.append(temp)
            trace[temp[0]][temp[1]] = s
        temp = (s[0]+1, s[1])
        if (temp[0] <= size-1) and (temp not in NotFree) and (Visited[temp[0]][temp[1]]):
            queue.append(temp)
            NotFree.append(temp)
            trace[temp[0]][temp[1]] = s
        temp = (s[0], s[1]-1)
        if (temp[1] >= 0) and (temp not in NotFree) and (Visited[temp[0]][temp[1]]):
            queue.append(temp)
            NotFree.append(temp)
            trace[temp[0]][temp[1]] = s
        temp = (s[0], s[1]+1)
        if (temp[1] <= size-1) and (temp not in NotFree) and (Visited[temp[0]][temp[1]]):
            queue.append(temp)
            NotFree.append(temp)
            trace[temp[0]][temp[1]] = s
    return


def Game(path):
    size, cave = load_level(path)
    init(size)
    init_pos = Agent_init_pos(size, cave)
    clauses.append(['-P',init_pos[0],init_pos[1]])
    clauses.append(['-W',init_pos[0],init_pos[1]])
    Pick_Gold = []
    Shot_Wumpus = []
    Score = []
    Agent_path, Stop = Wumpus_Agent(
        init_pos, size, cave, Pick_Gold, Shot_Wumpus, Score)
    if Stop == 'no_room':
        if len(Agent_path) == 0:
            Agent_path = [init_pos]
            Score = [10]
        else:
            path = BFS(Agent_path[-1], init_pos, size, cave)
            count = 0
            for i in range(1, len(path)):
                Agent_path.append(path[i])
                count += 1
            for i in range(count-1):
                Score.append(-10)
            Score.append(10)
    return Agent_path, Score, Pick_Gold, Shot_Wumpus


def Wumpus_Agent(init_pos, size, cave, Pick_Gold, Shot_Wumpus, Score):
    Agent_path = []
    Agent_pos = init_pos
    Visited[init_pos[0]][init_pos[1]] = True
    while True:
        score_room = 0
        take_percept(Agent_pos, size, Shot_Wumpus, cave)
        x = Agent_pos[0]
        y = Agent_pos[1]
        if 'G' in cave[x][y]:
            Gold[x][y] = True
            Pick_Gold.append(new_pos)
            score_room += 100
            cave[x][y] = cave[x][y].replace('G', '')
        if x-1 >= 0:
            if Wumpus[x-1][y] > 1:
                score_room -= 100
                Shot_Wumpus.append(((x, y), (x-1, y)))
                Is_Wumpus_dead((x-1, y), size, cave)
        if x+1 <= size-1:
            if Wumpus[x+1][y] > 1:
                score_room -= 100
                Shot_Wumpus.append(((x, y), (x+1, y)))
                Is_Wumpus_dead((x+1, y), size, cave)
        if y-1 >= 0:
            if Wumpus[x][y-1] > 1:
                score_room -= 100
                Shot_Wumpus.append(((x, y), (x, y-1)))
                Is_Wumpus_dead((x, y-1), size, cave)
        if y+1 <= size-1:
            if Wumpus[x][y+1] > 1:
                score_room -= 100
                Shot_Wumpus.append(((x, y), (x, y+1)))
                Is_Wumpus_dead((x, y+1), size, cave)

        Oke_pos = find_Oke_pos(size)
        if not Oke_pos:
            return Agent_path, 'no_room'
        Oke_pos = sorted(Oke_pos, key=lambda x: distance(x, Agent_pos))
        new_pos = Oke_pos.pop(0)
        score_room -= 10
        Visited[new_pos[0]][new_pos[1]] = True
        path = BFS(Agent_pos, new_pos, size, cave)
        for i in range(1, len(path)):
            Agent_path.append(path[i])
        Agent_pos = new_pos
        Score.append(score_room)


Game('./Data/map5.txt')
