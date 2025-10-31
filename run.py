import sys
import heapq
from collections import defaultdict


def solve(lines: list[str]) -> int:
    # Читаем входные данные, убираем пробелы
    clean_lines = []
    for line in lines:
        if line.strip():  # Пропускаем пустые строки
            clean_lines.append(line.rstrip())
    print(clean_lines)
    depth = len(clean_lines) - 3
    corridor = ['.'] * 11

    rooms = []
    for i in range(4):
        room = []
        for j in range(depth):
            # Безопасно берем символы
            row = clean_lines[2 + j]
            pos = 3 + 2 * i
            if pos < len(row):
                room.append(row[pos])
            else:
                room.append('.')  # Если вышли за границу - пусто
        rooms.append(room)

    start = (tuple(corridor), tuple(tuple(r) for r in rooms))

    # Настройки
    room_pos = [2, 4, 6, 8]
    targets = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    stops = [0, 1, 3, 5, 7, 9, 10]

    # Поиск
    heap = [(0, start)]
    best = defaultdict(lambda: 10 ** 9)
    best[start] = 0

    while heap:
        cost, state = heapq.heappop(heap)
        if cost > best[state]:
            continue

        cor, rms = state

        # Проверка победы
        win = True
        for i, t in enumerate(['A', 'B', 'C', 'D']):
            for x in rms[i]:
                if x != t:
                    win = False
                    break
        if win:
            return cost

        # Ходы из комнат в коридор
        for ri in range(4):
            room = rms[ri]
            # Ищем верхнюю фишку
            dep, amp = -1, ''
            for d in range(len(room)):
                if room[d] != '.':
                    dep, amp = d, room[d]
                    break
            if dep == -1:
                continue

            # Проверяем надо ли двигать
            move_need = True
            if ri == targets[amp]:
                ok = True
                for dd in range(dep, len(room)):
                    if rms[ri][dd] != amp:
                        ok = False
                        break
                if ok:
                    move_need = False
            if not move_need:
                continue

            # Пробуем позиции в коридоре
            for pos in stops:
                if cor[pos] != '.':
                    continue

                # Проверяем путь
                door = room_pos[ri]
                clear = True
                step = 1 if pos > door else -1
                for p in range(door + step, pos + step, step):
                    if cor[p] != '.':
                        clear = False
                        break
                if not clear:
                    continue

                # Делаем ход
                new_cor = list(cor)
                new_cor[pos] = amp
                new_rms = [list(room) for room in rms]
                new_rms[ri][dep] = '.'
                new_state = (tuple(new_cor), tuple(tuple(r) for r in new_rms))

                # Считаем стоимость
                steps = (dep + 1) + abs(pos - door)
                new_cost = cost + steps * costs[amp]

                if new_cost < best[new_state]:
                    best[new_state] = new_cost
                    heapq.heappush(heap, (new_cost, new_state))

        # Ходы из коридора в комнаты
        for pos in range(11):
            amp = cor[pos]
            if amp == '.':
                continue

            target_ri = targets[amp]
            target_room = rms[target_ri]

            # Проверяем можно ли зайти в комнату
            can_enter = True
            target_dep = -1
            for d in range(len(target_room) - 1, -1, -1):
                if target_room[d] == '.':
                    target_dep = d
                    break
                elif target_room[d] != amp:
                    can_enter = False
                    break

            if not can_enter or target_dep == -1:
                continue

            # Проверяем путь
            door = room_pos[target_ri]
            clear = True
            step = 1 if door > pos else -1
            for p in range(pos + step, door + step, step):
                if cor[p] != '.':
                    clear = False
                    break
            if not clear:
                continue

            # Делаем ход
            new_cor = list(cor)
            new_cor[pos] = '.'
            new_rms = [list(room) for room in rms]
            new_rms[target_ri][target_dep] = amp
            new_state = (tuple(new_cor), tuple(tuple(r) for r in new_rms))

            # Считаем стоимость
            steps = abs(pos - door) + (target_dep + 1)
            new_cost = cost + steps * costs[amp]

            if new_cost < best[new_state]:
                best[new_state] = new_cost
                heapq.heappush(heap, (new_cost, new_state))

    return -1


def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))

    result = solve(lines)
    print(result)


if __name__ == "__main__":
    main()