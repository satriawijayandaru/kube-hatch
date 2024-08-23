#!/bin/bash

# Prompt for IP/hostname and password
read -p "Enter the IP or hostname: " HOSTNAME
read -sp "Enter the Rancher admin password: " PASSWORD
echo

echo "installing K3S"
curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=v1.26.9+k3s1 sh -s - server --cluster-init

echo "Waiting for K3s to start..."
sleep 60
until kubectl get nodes &>/dev/null; do
  sleep 2
done

# Copy the K3s config to the .kube directory
cp /etc/rancher/k3s/k3s.yaml /root/.kube/config

echo "installing HELM"
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

echo "adding rancher to helm repo"
helm repo add rancher-stable https://releases.rancher.com/server-charts/stable
helm repo update

echo "installing cert manager"
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.12.0/cert-manager.crds.yaml
helm repo add jetstack https://charts.jetstack.io
helm repo update
helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace --version v1.12.0

# Check if the cattle-system namespace already exists
if kubectl get namespace cattle-system &>/dev/null; then
  echo "Namespace cattle-system already exists. Skipping creation."
else
  echo "Creating cattle-system namespace."
  kubectl create namespace cattle-system
fi

#kubectl create namespace cattle-system
helm install rancher rancher-stable/rancher \
  --namespace cattle-system \
  --set hostname=${HOSTNAME}.sslip.io \
  --set replicas=1 \
  --set bootstrapPassword=${PASSWORD}

watch -n 1 kubectl get all -n cattle-system
