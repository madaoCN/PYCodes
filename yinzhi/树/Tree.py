#coding=utf8
#!/usr/bin/python
# -*- coding: utf-8 -*-

tree = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F', 'G'],
        'D': ['H', 'I'],
        'E': [],
        'F': [],
        'G': [],
        'H': [],
        'I': []
    }
    leaf = []
    to_crawl = deque(['A'])
    while to_crawl:
        current = to_crawl.popleft()
        print current, to_crawl
        children = tree[current]
        if len(children)> 0:
            # width first
            # to_crawl.extend(children)
            # depth first
            to_crawl.extendleft(children[::-1])
            print to_crawl
        else:
            leaf.append(current)
    print leaf