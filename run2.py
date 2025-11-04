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

    graph = defaultdict(list)

    # строим граф
    for node1, node2 in edges:
        graph[node1].append(node2)
        graph[node2].append(node1)

    # находим узлы
    gates = {node for node in graph if node.isupper()}

    # текущая точка вируса
    virus_pos = 'a'

    result = []

    for _ in range(len(edges)):
        # BFS для поиска расстояний до всех шлюзов
        queue = deque([virus_pos])
        distances = {virus_pos: 0}
        queue = deque([virus_pos])

        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)

        # Находим целевой шлюз
        candidate_gates = [(distances[gate], gate) for gate in gates if gate in distances]
        if not candidate_gates:
            break

        min_dist = min(dist for dist, i in candidate_gates)
        target_gate = min(gate for dist, gate in candidate_gates if dist == min_dist)

        # Ищем следующий шаг вируса, снова BFS
        prev = {target_gate: None}
        queue = deque([target_gate])

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

        # Если next_node напрямую соединен с target_gate
        if target_gate in graph[next_node]:
            link_to_cut = f"{target_gate}-{next_node}"
        else:
            # Ищем, какой шлюз будет угрожать из next_node
            # Запускаем BFS из next_node
            next_distances = {next_node: 0}
            next_queue = deque([next_node])

            while next_queue:
                current = next_queue.popleft()
                for neighbor in graph[current]:
                    if neighbor not in next_distances:
                        next_distances[neighbor] = next_distances[current] + 1
                        next_queue.append(neighbor)

            # Находим ближайший шлюз из next_node
            threat_gates = [(next_distances[gate], gate) for gate in gates if gate in next_distances]
            if not threat_gates:
                break

            threat_min_dist = min(dist for dist, _ in threat_gates)
            threat_gate = min(gate for dist, gate in threat_gates if dist == threat_min_dist)

            # Блокируем связь threat_gate с next_node (если существует)
            if threat_gate in graph[next_node]:
                link_to_cut = f"{threat_gate}-{next_node}"
            else:
                # Ищем любую связь threat_gate
                gate_links = [f"{threat_gate}-{n}" for n in graph[threat_gate]]
                if not gate_links:
                    break
                link_to_cut = min(gate_links)

        # Отключаем коридор
        result.append(link_to_cut)

        # Удаляем связь из графа
        parts = link_to_cut.split('-')
        if len(parts) == 2:
            gate, node = parts
            if node in graph[gate]:
                graph[gate].remove(node)
            if gate in graph[node]:
                graph[node].remove(gate)

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