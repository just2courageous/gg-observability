# 🧭 Runbook — gg-observability (kube-prometheus-stack)

## ✅ Notes (current reality)
This repo is being polished for **GitHub (code hosting)** + portfolio.
If your **EKS (Elastic Kubernetes Service)** cluster is currently deleted, you can still keep this runbook as “how to reproduce later”.

## ✅ Prerequisites (when you rebuild later)
- An existing **EKS (Elastic Kubernetes Service)** cluster
- `kubectl` configured
- `helm` installed
- Namespace planned: `monitoring`

## 1) Create namespace
```bash
kubectl get ns monitoring || kubectl create ns monitoring
