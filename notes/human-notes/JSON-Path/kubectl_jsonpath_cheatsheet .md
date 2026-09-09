# kubectl JSONPath & Output Formatting Cheatsheet

> **kubectl = Kubernetes CLI** → talks to the Kube API Server (speaks JSON)

---

## Why JSONPath?

`kubectl get nodes -o wide` hides most of the JSON output for readability.
For full output use:

```yaml
kubectl get nodes -o json
kubectl get pods -o json
```

Then filter & format with JSONPath queries.

---

## JSONPath Syntax Basics

| Syntax | Meaning |
|---|---|
| `.items[0]` | First element of array |
| `.items[*]` | All elements |
| `.items[0].metadata.name` | Nested field access |
| `'{range .items[*]}{...}{end}'` | Loop over all items |
| `{"\n"}` | Newline helper |
| `{"\t"}` | Tab helper |

---

## Basic Examples

### Get name of first node
```bash
kubectl get nodes -o=jsonpath='{.items[0].metadata.name}'
```

### Get image of first container in first pod
```bash
kubectl get nodes -o=jsonpath='{.items[0].spec.containers[0].image}'
```

### Get all node names
```bash
kubectl get nodes -o=jsonpath='{.items[*].metadata.name}'
```

### Get OS architecture of all nodes
```bash
kubectl get nodes -o=jsonpath='{.items[*].status.nodeInfo.architecture}'
```

### Get CPU capacity of all nodes
```bash
kubectl get nodes -o=jsonpath='{.items[*].status.capacity.cpu}'
```

### Get memory capacity of all nodes
```bash
kubectl get nodes -o=jsonpath='{.items[*].status.capacity.memory}'
```

---

## Combining Multiple Queries

Queue multiple `{}`-blocks in one command:

```bash
# Names and CPU side by side (no separator)
kubectl get nodes -o=jsonpath='{.items[*].metadata.name}{.items[*].status.capacity.cpu}'

# With newline between
kubectl get nodes -o=jsonpath='{.items[*].metadata.name}{"\n"}{.items[*].status.capacity.cpu}'
```

---

## LOOP → FOR/EACH (range)

Iterate over all items and print fields per line:

```bash
kubectl get nodes -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.capacity.cpu}{"\n"}{end}'
```

### More range examples

#### Node name + OS image
```bash
kubectl get nodes -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.nodeInfo.osImage}{"\n"}{end}'
```

#### Pod name + namespace + status
```bash
kubectl get pods -A -o=jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.status.phase}{"\n"}{end}'
```

#### Pod name + container image(s)
```bash
kubectl get pods -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{range .spec.containers[*]}{.image}{" "}{end}{"\n"}{end}'
```

#### All service ClusterIPs
```bash
kubectl get svc -A -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.clusterIP}{"\n"}{end}'
```

---

## Filtering with Conditions

### Only nodes with a specific label (e.g. role=worker)
```bash
kubectl get nodes -l node-role.kubernetes.io/worker -o=jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}'
```

### Pods NOT in Running state
```bash
kubectl get pods -A -o=jsonpath='{range .items[?(@.status.phase!="Running")]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.status.phase}{"\n"}{end}'
```
> `?(@.field=="value")` = JSONPath filter expression

### Nodes where memory > threshold (advanced)
```bash
kubectl get nodes -o=jsonpath='{range .items[?(@.status.capacity.memory>"8Gi")]}{.metadata.name}{"\n"}{end}'
```

---

## Custom Columns

Cleaner table output without full JSON:

```bash
# Node name + CPU
kubectl get nodes -o=custom-columns=NODE:.metadata.name,CPU:.status.capacity.cpu

# Node name + memory + OS
kubectl get nodes -o=custom-columns=NODE:.metadata.name,MEMORY:.status.capacity.memory,OS:.status.nodeInfo.osImage

# Pod name + status + node it runs on
kubectl get pods -o=custom-columns=POD:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName

# All pods with restart count
kubectl get pods -A -o=custom-columns=NAMESPACE:.metadata.namespace,POD:.metadata.name,RESTARTS:.status.containerStatuses[0].restartCount
```

---

## Sort-by

```bash
# Sort nodes by name
kubectl get nodes --sort-by=.metadata.name

# Sort pods by creation time (oldest first)
kubectl get pods --sort-by=.metadata.creationTimestamp

# Sort pods by restart count (most restarts first — pipe to tac to reverse)
kubectl get pods --sort-by=.status.containerStatuses[0].restartCount

# Sort PVCs by capacity
kubectl get pvc --sort-by=.spec.resources.requests.storage
```

---

## Helpers (embed in any query)

| Helper | Code |
|---|---|
| New line | `{"\n"}` |
| Tab | `{"\t"}` |
| Space | `{" "}` |
| Literal string | `{"---"}` |

### Example with separator
```bash
kubectl get nodes -o=jsonpath='{range .items[*]}{.metadata.name}{" | "}{.status.capacity.cpu}{" CPU | "}{.status.capacity.memory}{"\n"}{end}'
```

---

## List first item (non-kubectl)

```bash
cat xx.yaml | jpath '$[0]'
```

---

## Context & Kubeconfig Queries

The kubeconfig file holds clusters, users, and contexts. JSONPath works on it just like on any other resource — but you use `kubectl config view` instead of `kubectl get`.

### Kubeconfig structure (mental model)
```
kubeconfig
├── clusters[]     → cluster name + API server URL
├── users[]        → user name + credentials
└── contexts[]     → name + { cluster, user, namespace }
                        ↑ a context = cluster + user paired together
```

### View full kubeconfig (incl. secrets)
```bash
kubectl config view --raw
# or a specific file:
kubectl config view --kubeconfig=my-kube-config
```

### Get all context names
```bash
kubectl config view -o=jsonpath='{.contexts[*].name}'
```

### Get all context names — one per line (range)
```bash
kubectl config view -o=jsonpath='{range .contexts[*]}{.name}{"\n"}{end}'
```

### Get context name by filtering on user (filter expression)
```bash
kubectl config view --kubeconfig=my-kube-config \
  -o jsonpath="{.contexts[?(@.context.user=='aws-user')].name}"
```
> Same `?(@.field=='value')` filter syntax as everywhere else — works on any array field.

### Get context name by filtering on cluster
```bash
kubectl config view -o jsonpath="{.contexts[?(@.context.cluster=='my-cluster')].name}"
```

### Get the current active context
```bash
kubectl config current-context
# or via jsonpath:
kubectl config view -o=jsonpath='{.current-context}'
```

### Get the cluster URL for a specific context
```bash
# Step 1: find the cluster name for the context
kubectl config view -o jsonpath="{.contexts[?(@.name=='my-context')].context.cluster}"

# Step 2: find the server URL for that cluster
kubectl config view -o jsonpath="{.clusters[?(@.name=='my-cluster')].cluster.server}"
```

### List all users
```bash
kubectl config view -o=jsonpath='{.users[*].name}'
```

### Get credentials for a specific user
```bash
kubectl config view --raw -o jsonpath="{.users[?(@.name=='aws-user')].user}"
```

### Context name + cluster + user — full table
```bash
kubectl config view -o=jsonpath='{range .contexts[*]}{.name}{"\t"}{.context.cluster}{"\t"}{.context.user}{"\n"}{end}'
```

### Switch context
```bash
kubectl config use-context <context-name>
```

### Set a context's default namespace
```bash
kubectl config set-context --current --namespace=my-namespace
```

### Output context name to a file (scripting pattern)
```bash
kubectl config view --kubeconfig=my-kube-config \
  -o jsonpath="{.contexts[?(@.context.user=='aws-user')].name}" \
  > /opt/outputs/aws-context-name
```

---

## Best Practices

**1. Always explore with `-o json` first**
Before writing a JSONPath query, dump the full JSON to understand the structure:
```bash
kubectl get node <nodename> -o json | less
```

**2. Test queries incrementally**
Start broad, then narrow:
```bash
# Step 1: confirm items exist
kubectl get pods -o=jsonpath='{.items[0]}'
# Step 2: drill into field
kubectl get pods -o=jsonpath='{.items[0].status}'
# Step 3: get exact value
kubectl get pods -o=jsonpath='{.items[0].status.phase}'
```

**3. Use `custom-columns` for human-readable output, JSONPath for scripting**
- `custom-columns` → reading in terminal
- `jsonpath` → piping into scripts or `grep`

**4. Combine with standard Unix tools**
```bash
# Count running pods
kubectl get pods -A -o=jsonpath='{range .items[?(@.status.phase=="Running")]}{.metadata.name}{"\n"}{end}' | wc -l

# Find pods with high restarts
kubectl get pods -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.containerStatuses[0].restartCount}{"\n"}{end}' | sort -t$'\t' -k2 -rn | head -10
```

**5. Quote carefully in different shells**
```bash
# Bash: single quotes around jsonpath
kubectl get pods -o=jsonpath='{.items[0].metadata.name}'

# PowerShell: escape differently
kubectl get pods -o=jsonpath="{``.items[0].metadata.name``}"
```

**6. Use `-A` (--all-namespaces) when unsure which namespace**
```bash
kubectl get pods -A -o=jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\n"}{end}'
```

---

## Quick Reference Card

```bash
# All node names
kubectl get nodes -o=jsonpath='{.items[*].metadata.name}'

# All pod names across namespaces
kubectl get pods -A -o=jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}'

# Node name + CPU + Memory table
kubectl get nodes -o=custom-columns=NODE:.metadata.name,CPU:.status.capacity.cpu,MEM:.status.capacity.memory

# Pods sorted by age
kubectl get pods --sort-by=.metadata.creationTimestamp

# Images running in cluster
kubectl get pods -A -o=jsonpath='{range .items[*]}{range .spec.containers[*]}{.image}{"\n"}{end}{end}' | sort -u

# Pod IPs
kubectl get pods -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.podIP}{"\n"}{end}'

# Service ClusterIPs + Ports
kubectl get svc -o=custom-columns=NAME:.metadata.name,CLUSTERIP:.spec.clusterIP,PORT:.spec.ports[0].port

# All context names
kubectl config view -o=jsonpath='{range .contexts[*]}{.name}{"\n"}{end}'

# Current active context
kubectl config current-context

# Context name filtered by user
kubectl config view -o jsonpath="{.contexts[?(@.context.user=='aws-user')].name}"

# Context → cluster → server URL
kubectl config view -o=jsonpath='{range .contexts[*]}{.name}{"\t"}{.context.cluster}{"\t"}{.context.user}{"\n"}{end}'
```
