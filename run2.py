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

    while True:
        # Находим целевой шлюз для вируса
        distances = {virus_pos: 0}
        queue = deque([virus_pos])

        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)

        # Найти все достижимые шлюзы и выбрать ближайший
        reachable_gates = [(distances[gate], gate) for gate in gates if gate in distances]
        if not reachable_gates:
            break

        min_dist = min(dist for dist, _ in reachable_gates)
        target_gate = min(gate for dist, gate in reachable_gates if dist == min_dist)

        #  Найти следующий узел вируса
        # BFS от целевого шлюза назад для построения дерева путей
        prev = {target_gate: None}
        queue = deque([target_gate])

        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in prev:
                    prev[neighbor] = current
                    queue.append(neighbor)

        # Теперь находим всех соседей virus_pos, которые ведут к target_gate
        candidate_next_nodes = []
        for neighbor in graph[virus_pos]:
            # Проверяем, есть ли путь от neighbor к target_gate через prev
            current = neighbor
            while current is not None and current != target_gate:
                current = prev.get(current)
            if current == target_gate:
                candidate_next_nodes.append(neighbor)

        if not candidate_next_nodes:
            break

        # Выбираем лексикографически наименьший следующий узел
        next_node = min(candidate_next_nodes)

        # Определить какой шлюз отключать
        # Если есть непосредственные угрозы из next_node
        immediate_threats = []
        for neighbor in graph[next_node]:
            if neighbor in gates:
                immediate_threats.append(f"{neighbor}-{next_node}")

        if immediate_threats:
            link_to_cut = min(immediate_threats)
        else:
            # Найти ближайший шлюз из next_node
            next_distances = {next_node: 0}
            next_queue = deque([next_node])

            while next_queue:
                current = next_queue.popleft()
                for neighbor in graph[current]:
                    if neighbor not in next_distances:
                        next_distances[neighbor] = next_distances[current] + 1
                        next_queue.append(neighbor)

            # Найти все достижимые шлюзы из next_node
            next_gates = [(next_distances[gate], gate) for gate in gates if gate in next_distances]
            if not next_gates:
                break

            next_min_dist = min(dist for dist, _ in next_gates)
            next_target_gate = min(gate for dist, gate in next_gates if dist == next_min_dist)

            # Найти все связи next_target_gate
            gate_links = [f"{next_target_gate}-{node}" for node in graph[next_target_gate]]
            if not gate_links:
                break
            link_to_cut = min(gate_links)

        result.append(link_to_cut)

        # Удалить связь из графа
        gate, node = link_to_cut.split('-')
        graph[gate].remove(node)
        graph[node].remove(gate)

        # Вирус перемещается
        virus_pos = next_node

        # Проверка завершения
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