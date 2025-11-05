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

    for _ in range(len(edges)):
        # Найти целевой шлюз
        distances = {virus_pos: 0}
        queue = deque([virus_pos])

        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)

        # Выбрать ближайший шлюз
        candidate_gates = []
        for gate in gates:
            if gate in distances:
                candidate_gates.append((distances[gate], gate))

        if not candidate_gates:
            break

        min_dist = min(dist for dist, _ in candidate_gates)
        target_gate = min(gate for dist, gate in candidate_gates if dist == min_dist)

        # Используем BFS от target_gate назад для построения всех кратчайших путей
        prev = defaultdict(list)
        queue = deque([target_gate])
        prev[target_gate] = []

        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in prev:
                    # Первое посещение
                    prev[neighbor] = [current]
                    queue.append(neighbor)
                elif distances[neighbor] == distances[current] - 1:
                    # Альтернативный путь той же длины
                    prev[neighbor].append(current)

        # Находим всех соседей virus_pos на кратчайших путях
        candidate_next_nodes = []
        for neighbor in graph[virus_pos]:
            if neighbor in prev and distances[neighbor] == 1:
                candidate_next_nodes.append(neighbor)

        if not candidate_next_nodes:
            break

        # Выбираем лексикографически наименьший
        next_node = min(candidate_next_nodes)

        # Находим ближайший шлюз из next_node
        next_distances = {next_node: 0}
        next_queue = deque([next_node])

        while next_queue:
            current = next_queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in next_distances:
                    next_distances[neighbor] = next_distances[current] + 1
                    next_queue.append(neighbor)

        # Находим ближайший шлюз из next_node
        next_gates = []
        for gate in gates:
            if gate in next_distances:
                next_gates.append((next_distances[gate], gate))

        if not next_gates:
            break

        next_min_dist = min(dist for dist, _ in next_gates)
        next_target_gate = min(gate for dist, gate in next_gates if dist == next_min_dist)

        # Находим путь от next_node к next_target_gate
        threat_prev = {next_node: None}
        threat_queue = deque([next_node])

        while threat_queue:
            current = threat_queue.popleft()
            if current == next_target_gate:
                break
            for neighbor in graph[current]:
                if neighbor not in threat_prev:
                    threat_prev[neighbor] = current
                    threat_queue.append(neighbor)

        # Находим узел, непосредственно соединенный с next_target_gate на этом пути
        if next_target_gate in threat_prev:
            current = next_target_gate
            while threat_prev[current] != next_node:
                current = threat_prev[current]
            node_to_block = current
            link_to_cut = f"{next_target_gate}-{node_to_block}"
        else:
            # Если путь не найден, блокируем любую связь next_target_gate
            available_links = [f"{next_target_gate}-{node}" for node in graph[next_target_gate]]
            if not available_links:
                break
            link_to_cut = min(available_links)

        result.append(link_to_cut)

        # Удаляем связь из графа
        gate, node = link_to_cut.split('-')
        if node in graph[gate]:
            graph[gate].remove(node)
        if gate in graph[node]:
            graph[node].remove(gate)

        # Вирус перемещается
        virus_pos = next_node

        # Проверяем завершение
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