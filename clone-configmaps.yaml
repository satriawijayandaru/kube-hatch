#!/bin/bash

echo -n "Enter namespace: "
read NAMESPACE

if [ -z "$NAMESPACE" ]; then
    echo "Namespace cannot be empty!"
    exit 1
fi

kubectl get cm -n "$NAMESPACE" -o name | while read cm; do
  kubectl get "$cm" -n "$NAMESPACE" -o yaml > "$(echo $cm | cut -d'/' -f2).yaml"
done

echo "All ConfigMaps have been saved"
