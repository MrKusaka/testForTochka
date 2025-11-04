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

    max_steps = len(edges)  # Защита от бесконечного цикла

    for step in range(max_steps):
        # Найти куда пойдет вирус ИЗ ТЕКУЩЕЙ позиции
        distances_from_virus = {virus_pos: 0}
        queue = deque([virus_pos])

        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in distances_from_virus:
                    distances_from_virus[neighbor] = distances_from_virus[current] + 1
                    queue.append(neighbor)

        # Найти ближайший шлюз для вируса
        reachable_gates = []
        for gate in gates:
            if gate in distances_from_virus:
                reachable_gates.append((distances_from_virus[gate], gate))

        if not reachable_gates:
            break  # Вирус изолирован

        # Выбираем целевой шлюз
        min_dist = min(dist for dist, _ in reachable_gates)
        target_gate = min(gate for dist, gate in reachable_gates if dist == min_dist)

        # Найти следующий узел на пути к target_gate
        # BFS от target_gate назад
        prev = {}
        queue = deque([target_gate])
        prev[target_gate] = None

        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in prev:
                    prev[neighbor] = current
                    queue.append(neighbor)

        # Восстанавливаем путь
        path = []
        current = virus_pos
        while current != target_gate:
            path.append(current)
            current = prev[current]
        next_node = path[1] if len(path) > 1 else target_gate

        # Находим все шлюзы, достижимые ИЗ next_node
        distances_from_next = {next_node: 0}
        queue = deque([next_node])

        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in distances_from_next:
                    distances_from_next[neighbor] = distances_from_next[current] + 1
                    queue.append(neighbor)

        # Находим ближайший шлюз ИЗ next_node
        threat_gates = []
        for gate in gates:
            if gate in distances_from_next:
                threat_gates.append((distances_from_next[gate], gate))

        if not threat_gates:
            break

        threat_min_dist = min(dist for dist, _ in threat_gates)
        threat_gate = min(gate for dist, gate in threat_gates if dist == threat_min_dist)

        # Находим путь от next_node к threat_gate
        prev_to_threat = {}
        queue = deque([threat_gate])
        prev_to_threat[threat_gate] = None

        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in prev_to_threat:
                    prev_to_threat[neighbor] = current
                    queue.append(neighbor)

        # Находим первый узел от next_node на пути к threat_gate
        current = next_node
        while current != threat_gate:
            next_on_path = prev_to_threat[current]
            current = next_on_path

        # Блокируем связь между threat_gate и узлом, который к нему ведет
        available_links = [f"{threat_gate}-{node}" for node in graph[threat_gate]]
        if not available_links:
            break

        link_to_cut = min(available_links)

        result.append(link_to_cut)

        # Удаляем связь из графа
        gate_part, node_part = link_to_cut.split('-')
        graph[gate_part].remove(node_part)
        graph[node_part].remove(gate_part)

        # Вирус делает ход
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