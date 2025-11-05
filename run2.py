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

        # 2. Найти следующий узел вируса
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

        # 3. ОПРЕДЕЛИТЬ КАКОЙ ШЛЮЗ ОТКЛЮЧАТЬ
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

        # 4. НАЙТИ КОНКРЕТНУЮ СВЯЗЬ ДЛЯ БЛОКИРОВКИ
        # Найти узел, через который next_node идет к threat_gate
        threat_prev = {threat_gate: None}
        threat_queue = deque([threat_gate])

        while threat_queue:
            current = threat_queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in threat_prev:
                    threat_prev[neighbor] = current
                    threat_queue.append(neighbor)

        # Найти узел, непосредственно соединенный с threat_gate на пути из next_node
        node_to_block = None
        if threat_gate in graph[next_node]:
            node_to_block = next_node
        else:
            # Ищем узел на пути от next_node к threat_gate
            path = []
            current = next_node
            while current != threat_gate:
                if current not in threat_prev:
                    break
                path.append(current)
                current = threat_prev[current]
            if path:
                node_to_block = path[-1]  # Последний узел перед threat_gate

        if node_to_block and threat_gate in graph[node_to_block]:
            link_to_cut = f"{threat_gate}-{node_to_block}"
        else:
            # Если не нашли конкретный узел, берем лексикографически наименьшую связь threat_gate
            available_links = [f"{threat_gate}-{node}" for node in sorted(graph[threat_gate])]
            if not available_links:
                break
            link_to_cut = available_links[0]

        result.append(link_to_cut)

        # Удалить связь из графа
        gate, node = link_to_cut.split('-')
        graph[gate].remove(node)
        graph[node].remove(gate)

        # Переместить вирус
        virus_pos = next_node

        # Проверить завершение
        if virus_pos in gates:
            break

        if len(result) >= len(edges):  # Защита от бесконечного цикла
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