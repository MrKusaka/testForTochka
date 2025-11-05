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

        reachable_gates = [(distances[gate], gate) for gate in gates if gate in distances]
        if not reachable_gates:
            break

        min_dist = min(dist for dist, _ in reachable_gates)
        target_gate = min(gate for dist, gate in reachable_gates if dist == min_dist)

        # BFS от target_gate назад для построения дерева кратчайших путей
        prev = defaultdict(list)
        dist_to_gate = {target_gate: 0}
        queue = deque([target_gate])

        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in dist_to_gate:
                    dist_to_gate[neighbor] = dist_to_gate[current] + 1
                    prev[neighbor] = [current]
                    queue.append(neighbor)
                elif dist_to_gate[neighbor] == dist_to_gate[current] + 1:
                    # Альтернативный путь той же длины
                    prev[neighbor].append(current)

        # Найти следующий узел (лексикографически наименьший сосед на кратчайшем пути)
        next_node = None
        for neighbor in sorted(graph[virus_pos]):  # Сортируем для детерминированности
            if neighbor in prev and dist_to_gate[neighbor] == min_dist - 1:
                next_node = neighbor
                break

        if next_node is None:
            break

        # Правило: отключаем шлюз, который будет угрожать после перемещения вируса

        # Найти ближайший шлюз ИЗ next_node
        next_distances = {next_node: 0}
        next_queue = deque([next_node])

        while next_queue:
            current = next_queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in next_distances:
                    next_distances[neighbor] = next_distances[current] + 1
                    next_queue.append(neighbor)

        # Найти все шлюзы, достижимые из next_node
        next_gates = [(next_distances[gate], gate) for gate in gates if gate in next_distances]
        if not next_gates:
            break

        next_min_dist = min(dist for dist, _ in next_gates)
        threat_gate = min(gate for dist, gate in next_gates if dist == next_min_dist)

        # Найти следующий узел
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

        # Упрощенная и надежная логика блокировки
        all_possible_links = []

        # Сначала проверяем связи next_node со шлюзами (непосредственные угрозы)
        for neighbor in graph[next_node]:
            if neighbor in gates:
                all_possible_links.append(f"{neighbor}-{next_node}")

        # Если нет непосредственных угроз, проверяем связи virus_pos со шлюзами
        if not all_possible_links:
            for neighbor in graph[virus_pos]:
                if neighbor in gates:
                    all_possible_links.append(f"{neighbor}-{virus_pos}")

        # Если все еще нет, берем ВСЕ связи шлюзов в лексикографическом порядке
        if not all_possible_links:
            for gate in sorted(gates):
                for node in sorted(graph[gate]):
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