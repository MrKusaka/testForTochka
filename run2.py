import sys
from collections import defaultdict, deque


def solve(edges: list[tuple[str, str]]) -> list[str]:
    """
    Решение задачи об изоляции вируса

    Args:
        edges: список коридоров в формате (узел1, узел2)

    Returns:
        список отключаемых коридоров в формате "Шлюз-узел"

    """
    graph = defaultdict(list)
    for node1, node2 in edges:
        graph[node1].append(node2)
        graph[node2].append(node1)

    gates = {node for node in graph if node.isupper()}
    virus_pos = 'a'
    result = []

    # Максимальное количество шагов
    for _ in range(len(edges)):
        # ШАГ 1: Найти все шлюзы, до которых может дойти вирус
        distances = {}
        queue = deque([virus_pos])
        distances[virus_pos] = 0

        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)

        # Найти ближайший шлюз
        closest_gates = []
        for gate in gates:
            if gate in distances:
                closest_gates.append((distances[gate], gate))

        if not closest_gates:
            break  # Вирус изолирован

        min_distance = min(dist for dist, _ in closest_gates)
        target_gate = min(gate for dist, gate in closest_gates if dist == min_distance)

        # ШАГ 2: Найти следующий узел на пути к целевому шлюзу
        # BFS от шлюза назад для построения путей
        prev = {target_gate: None}
        queue = deque([target_gate])

        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in prev:
                    prev[neighbor] = current
                    queue.append(neighbor)

        # Восстановить путь от вируса к шлюзу
        path = []
        current = virus_pos
        while current != target_gate:
            path.append(current)
            current = prev[current]
        next_node = path[1] if len(path) > 1 else target_gate

        # ШАГ 3: Блокировать угрозу ИЗ следующей позиции
        # Найти все шлюзы, соединенные с next_node
        immediate_threats = []
        for neighbor in graph[next_node]:
            if neighbor in gates:
                immediate_threats.append(f"{neighbor}-{next_node}")

        if immediate_threats:
            # Блокируем лексикографически наименьшую непосредственную угрозу
            link_to_cut = min(immediate_threats)
        else:
            # Если нет непосредственных угроз, блокируем любой шлюз на пути
            # Найти шлюзы, достижимые из next_node
            next_distances = {next_node: 0}
            next_queue = deque([next_node])

            while next_queue:
                current = next_queue.popleft()
                for neighbor in graph[current]:
                    if neighbor not in next_distances:
                        next_distances[neighbor] = next_distances[current] + 1
                        next_queue.append(neighbor)

            # Найти ближайший шлюз из next_node
            threat_gates = []
            for gate in gates:
                if gate in next_distances:
                    threat_gates.append((next_distances[gate], gate))

            if not threat_gates:
                break

            threat_min_dist = min(dist for dist, _ in threat_gates)
            threat_gate = min(gate for dist, gate in threat_gates if dist == threat_min_dist)

            # Блокируем любую связь этого шлюза
            available_links = [f"{threat_gate}-{node}" for node in graph[threat_gate]]
            if not available_links:
                break
            link_to_cut = min(available_links)

        # Отключаем коридор
        result.append(link_to_cut)

        # Удаляем связь из графа
        gate, node = link_to_cut.split('-')
        if node in graph[gate]:
            graph[gate].remove(node)
        if gate in graph[node]:
            graph[node].remove(gate)

        # Вирус перемещается
        virus_pos = next_node

        # Проверяем, не достиг ли вирус шлюза
        if virus_pos in gates:
            break

    return result


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                edges.append((node1, node2))

    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()