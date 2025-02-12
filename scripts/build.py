import sys
from collections import defaultdict, deque

from common import ensure
from dependencies import platform_projects, dag


def sort_projects(projects: list[str]) -> list[str]:
    in_degree = {project: len([dep for dep in dag.get(project, []) if dep in projects]) for project in projects}
    adjacency_list = defaultdict(list)

    for project, deps in dag.items():
        if project not in projects:
            continue
        for dep in deps:
            # openssl is not needed for curl on iOS.
            if dep not in projects:
                continue
            adjacency_list[dep].append(project)

    zero_in_degree = deque(sorted([p for p in projects if in_degree[p] == 0]))

    sorted_projects = []
    while zero_in_degree:
        project = zero_in_degree.popleft()
        sorted_projects.append(project)

        for neighbor in sorted(adjacency_list[project]):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                zero_in_degree.append(neighbor)

    if len(sorted_projects) != len(projects):
        raise ValueError("Dependency graph has a cycle")

    return sorted_projects


for project in sort_projects(platform_projects[sys.argv[1]]):
    ensure('python', [f'scripts/{project}.py'] + sys.argv[1:])
