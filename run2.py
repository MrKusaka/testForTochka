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
            found_target = False

            while n_queue and not found_target:
                current_node = n_queue.popleft()
                if current_node == target_gate:
                    found_target = True
                    break
                for nbr in graph[current_node]:
                    if nbr not in neighbor_dist:
                        neighbor_dist[nbr] = neighbor_dist[current_node] + 1
                        n_queue.append(nbr)

            # Проверяем, ведет ли neighbor к target_gate за (min_dist - 1) шагов
            if found_target and neighbor_dist[target_gate] == min_dist - 1:
                candidate_next_nodes.append(neighbor)

        if not candidate_next_nodes:
            break

        # Выбираем лексикографически наименьший
        next_node = min(candidate_next_nodes)

        # Находим ВСЕ доступные для отключения связи со шлюзами
        all_possible_links = []

        # Сначала проверяем связи next_node со шлюзами (непосредственные угрозы)
        for neighbor in graph[next_node]:
            if neighbor in gates:
                all_possible_links.append(f"{neighbor}-{next_node}")

        # Если нет непосредственных угроз, берем ВСЕ связи шлюзов
        if not all_possible_links:
            for gate in sorted(gates):  # Сортируем шлюзы
                for node in sorted(graph[gate]):  # Сортируем узлы
                    all_possible_links.append(f"{gate}-{node}")

        if not all_possible_links:
            break

        # Выбираем лексикографически наименьшую связь
        link_to_cut = min(all_possible_links)
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