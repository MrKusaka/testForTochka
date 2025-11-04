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
        # Выбор целевого шлюза
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

        # Находим ВСЕ соседи virus_pos, которые ведут к target_gate по кратчайшему пути
        candidate_next_nodes = []

        for neighbor in graph[virus_pos]:
            # Запускаем BFS из neighbor чтобы проверить, ведет ли он к target_gate
            neighbor_distances = {neighbor: 0}
            n_queue = deque([neighbor])
            found = False

            while n_queue:
                current_node = n_queue.popleft()
                if current_node == target_gate:
                    found = True
                    break
                for nbr in graph[current_node]:
                    if nbr not in neighbor_distances:
                        neighbor_distances[nbr] = neighbor_distances[current_node] + 1
                        n_queue.append(nbr)

            # Если через neighbor можно дойти до target_gate за (min_dist - 1) шагов
            if found and neighbor_distances.get(target_gate, float('inf')) == min_dist - 1:
                candidate_next_nodes.append(neighbor)

        if not candidate_next_nodes:
            break

        # Выбираем лексикографически наименьший узел
        next_node = min(candidate_next_nodes)

        # Находим все шлюзы, соединенные с next_node (непосредственные угрозы)
        immediate_threats = []
        for neighbor in graph[next_node]:
            if neighbor in gates:
                immediate_threats.append(f"{neighbor}-{next_node}")

        if immediate_threats:
            # Блокируем лексикографически наименьшую непосредственную угрозу
            link_to_cut = min(immediate_threats)
        else:
            # Если нет непосредственных угроз, находим ближайший шлюз из next_node
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
            threat_gate_candidates = [gate for dist, gate in threat_gates if dist == threat_min_dist]
            threat_gate = min(threat_gate_candidates)

            # Блокируем лексикографически наименьшую связь threat_gate
            available_links = [f"{threat_gate}-{node}" for node in graph[threat_gate]]
            if not available_links:
                break
            link_to_cut = min(available_links)

        result.append(link_to_cut)

        # Удаляем связь из графа
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