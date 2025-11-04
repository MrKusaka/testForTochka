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
        # BFS для поиска расстояний до всех узлов
        distances = {virus_pos: 0}
        queue = deque([virus_pos])

        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)

        # Находим ближайший шлюз
        candidate_gates = []
        for gate in gates:
            if gate in distances:
                candidate_gates.append((distances[gate], gate))

        if not candidate_gates:
            break

        min_dist = min(dist for dist, _ in candidate_gates)
        target_gate = min(gate for dist, gate in candidate_gates if dist == min_dist)

        # Находим следующий узел на пути к target_gate
        # BFS от target_gate назад
        prev = {target_gate: None}
        queue = deque([target_gate])

        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in prev:
                    prev[neighbor] = current
                    queue.append(neighbor)

        # Восстанавливаем путь от вируса к шлюзу
        path = []
        current = virus_pos
        while current != target_gate:
            path.append(current)
            current = prev[current]
        path.append(target_gate)

        next_node = path[1]  # Следующий узел

        # Блокируем связь next_node с тем шлюзом, который будет ближайшим ИЗ next_node
        next_distances = {next_node: 0}
        next_queue = deque([next_node])

        while next_queue:
            current = next_queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in next_distances:
                    next_distances[neighbor] = next_distances[current] + 1
                    next_queue.append(neighbor)

        # Находим ближайший шлюз из next_node
        threat_gates = []
        for gate in gates:
            if gate in next_distances:
                threat_gates.append((next_distances[gate], gate))

        if not threat_gates:
            break

        threat_min_dist = min(dist for dist, _ in threat_gates)
        threat_gate = min(gate for dist, gate in threat_gates if dist == threat_min_dist)

        # ВАЖНО: Проверяем, существует ли связь между threat_gate и next_node
        # Если нет, ищем другую связь threat_gate
        if next_node in graph[threat_gate]:
            link_to_cut = f"{threat_gate}-{next_node}"
        else:
            # Ищем любую существующую связь threat_gate
            available_links = [f"{threat_gate}-{node}" for node in graph[threat_gate]]
            if not available_links:
                break
            link_to_cut = min(available_links)

        result.append(link_to_cut)

        # Удаляем связь из графа (теперь безопасно)
        gate_part, node_part = link_to_cut.split('-')
        if node_part in graph[gate_part]:
            graph[gate_part].remove(node_part)
        if gate_part in graph[node_part]:
            graph[node_part].remove(gate_part)

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