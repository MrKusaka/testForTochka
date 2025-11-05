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

        # Нужно найти всех соседей virus_pos, которые находятся на кратчайшем пути к target_gate
        candidate_next_nodes = []

        for neighbor in graph[virus_pos]:
            # Запускаем BFS из neighbor чтобы найти расстояние до target_gate
            neighbor_dist = {neighbor: 0}
            n_queue = deque([neighbor])

            while n_queue:
                current_node = n_queue.popleft()
                if current_node == target_gate:
                    # Проверяем что путь через neighbor действительно короче
                    if neighbor_dist[target_gate] == min_dist - 1:
                        candidate_next_nodes.append(neighbor)
                    break
                for nbr in graph[current_node]:
                    if nbr not in neighbor_dist:
                        neighbor_dist[nbr] = neighbor_dist[current_node] + 1
                        n_queue.append(nbr)

        if not candidate_next_nodes:
            break

        # Выбираем лексикографически наименьший
        next_node = min(candidate_next_nodes)

        # Блокируем связь next_node с target_gate, если она существует
        if target_gate in graph[next_node]:
            link_to_cut = f"{target_gate}-{next_node}"
        else:
            # Ищем ближайший шлюз из next_node
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

            # Находим путь от next_node к threat_gate
            prev_path = {next_node: None}
            path_queue = deque([next_node])

            while path_queue:
                current = path_queue.popleft()
                if current == threat_gate:
                    break
                for neighbor in graph[current]:
                    if neighbor not in prev_path:
                        prev_path[neighbor] = current
                        path_queue.append(neighbor)

            # Находим узел, соединенный с threat_gate на этом пути
            if threat_gate in prev_path:
                # Идем назад от threat_gate к next_node
                current = threat_gate
                while prev_path[current] != next_node:
                    current = prev_path[current]
                node_on_path = current
                link_to_cut = f"{threat_gate}-{node_on_path}"
            else:
                # Если путь не найден, берем любую связь threat_gate
                available_links = [f"{threat_gate}-{node}" for node in graph[threat_gate]]
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

        # Проверяем, не остались ли мы на месте
        if virus_pos in gates or virus_pos == next_node and not graph[virus_pos]:
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