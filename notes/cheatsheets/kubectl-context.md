# kubectl Context & Namespace Cheatsheet

## Show current context

```bash
kubectl config current-context
```

## List contexts

```bash
kubectl config get-contexts
```

## Switch context

```bash
kubectl config use-context <context-name>
```

## Set default namespace for current context

```bash
kubectl config set-context --current --namespace=<namespace>
```

## Verify effective namespace in current context

```bash
kubectl config view --minify -o jsonpath='{..namespace}'
```
