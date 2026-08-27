<!-- AGENTTEAMS:BEGIN content v=1 -->
# networkx Reference — LearnPythonStatsEcon

> Quick-reference for **networkx ** (library) in LearnPythonStatsEcon.
> This is a lightweight reference file, not an agent. For operational procedures, consult the tool's reference/skill document, or escalate to `@orchestrator`.

---

## Version

`networkx` ``

## Configuration

**Config files:** `N/A`

## Official Documentation

https://networkx.org/documentation/stable/reference/

## Key API Surface

Graph creation: nx.Graph(), nx.DiGraph(), nx.MultiGraph(); graph manipulation: G.add_node(), G.add_edge(), G.add_nodes_from(), G.add_edges_from(); algorithms: nx.shortest_path(), nx.degree_centrality(), nx.betweenness_centrality(), nx.pagerank(), nx.connected_components(), nx.is_connected(); drawing: nx.draw(), nx.draw_networkx(), nx.spring_layout()

<!-- Document the primary classes, functions, or APIs that project code depends on from networkx. -->

## Common Patterns & Pitfalls

Create graphs with G = nx.Graph(); G.add_edges_from(edge_list). Store node attributes: G.nodes[n]['weight'] = val. Visualise with nx.draw(G, pos=nx.spring_layout(G), with_labels=True). For weighted shortest paths pass weight='weight' to the algorithm. Pitfall: NetworkX stores graphs in memory — for >100k nodes use GraphTool or igraph.

<!-- Document common usage patterns, best practices, and known issues for networkx . -->

## Key Conventions

- Follow project style rules when using networkx
- Refer to authority sources for API contract accuracy
- Validate changes against existing tests before committing

## Related Agents

- `@technical-validator` — verify technical accuracy of networkx usage
- `@primary-producer` — implements code that depends on networkx
<!-- AGENTTEAMS:END content -->
