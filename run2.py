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

        # BFS от target_gate назад
        prev = {target_gate: None}
        queue = deque([target_gate])

        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in prev:
                    prev[neighbor] = current
                    queue.append(neighbor)

        # Находим следующий узел на пути к target_gate
        path = []
        current = virus_pos
        while current != target_gate:
            path.append(current)
            current = prev[current]

        if len(path) < 2:  # Вирус уже у шлюза
            break

        next_node = path[1]

        # Находим ВСЕ связи шлюзов, доступные для отключения
        all_gate_links = []
        for gate in gates:
            for node in graph[gate]:
                all_gate_links.append(f"{gate}-{node}")

        if not all_gate_links:
            break

        # Связи next_node со шлюзами (непосредственные угрозы)
        immediate_threats = []
        for neighbor in graph[next_node]:
            if neighbor in gates:
                immediate_threats.append(f"{neighbor}-{next_node}")

        if immediate_threats:
            link_to_cut = min(immediate_threats)

        else:
            #  Связи target_gate (текущий целевой шлюз)
            target_links = [f"{target_gate}-{node}" for node in graph[target_gate]]
            if target_links:
                link_to_cut = min(target_links)

            else:
                # Находим шлюзы, достижимые из next_node
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
                next_target = min(gate for dist, gate in next_gates if dist == next_min_dist)

                # Блокируем связь next_target
                next_target_links = [f"{next_target}-{node}" for node in graph[next_target]]
                if not next_target_links:
                    break
                link_to_cut = min(next_target_links)

        if link_to_cut in result:
            # Ищем альтернативную связь
            alternative_links = [link for link in all_gate_links if link not in result]
            if not alternative_links:
                break
            link_to_cut = min(alternative_links)

        result.append(link_to_cut)

        # Удаляем связь из графа
        gate, node = link_to_cut.split('-')
        graph[gate].remove(node)
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