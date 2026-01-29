import os
import yaml

INPUT_DIR = "./"
OUTPUT_DIR = "transformed_files"

REMOVE_METADATA_FIELDS = {
    "creationTimestamp",
    "managedFields",
    "resourceVersion",
    "uid",
    "ownerReferences",
}

REMOVE_ANNOTATIONS = {
    "field.cattle.io/targetWorkloadIds",
    "management.cattle.io/ui-managed",
}

REMOVE_SPEC_FIELDS = {
    "clusterIP",
    "clusterIPs",
    "ipFamilies",
    "ipFamilyPolicy",
    "internalTrafficPolicy",
}

# Ask user for namespace
NEW_NAMESPACE = input("Enter target namespace: ").strip()
if not NEW_NAMESPACE:
    raise ValueError("Namespace cannot be empty")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_service(doc):
    if not isinstance(doc, dict):
        return None
    if doc.get("kind") != "Service":
        return None

    # --- metadata cleanup ---
    metadata = doc.get("metadata", {})

    for field in REMOVE_METADATA_FIELDS:
        metadata.pop(field, None)

    annotations = metadata.get("annotations", {})
    for ann in REMOVE_ANNOTATIONS:
        annotations.pop(ann, None)

    if not annotations:
        metadata.pop("annotations", None)

    metadata["namespace"] = NEW_NAMESPACE
    doc["metadata"] = metadata

    # --- spec cleanup ---
    spec = doc.get("spec", {})

    for field in REMOVE_SPEC_FIELDS:
        spec.pop(field, None)

    # NodePort: let Rancher/K8s auto-allocate
    if spec.get("type") == "NodePort":
        for port in spec.get("ports", []):
            port.pop("nodePort", None)

    doc["spec"] = spec

    # --- status cleanup ---
    doc.pop("status", None)

    return doc


for filename in os.listdir(INPUT_DIR):
    if not filename.endswith((".yaml", ".yml")):
        continue

    input_path = os.path.join(INPUT_DIR, filename)
    output_path = os.path.join(OUTPUT_DIR, filename)

    with open(input_path, "r") as f:
        docs = list(yaml.safe_load_all(f))

    cleaned_docs = []
    for doc in docs:
        cleaned = clean_service(doc)
        if cleaned:
            cleaned_docs.append(cleaned)

    if not cleaned_docs:
        print(f"⚠️  Skipped {filename} (no Service found)")
        continue

    with open(output_path, "w") as f:
        yaml.safe_dump_all(cleaned_docs, f, sort_keys=False)

    print(f"✅ Cleaned: {filename} → {output_path}")

print("🎉 All done. Cleaned files are in ./transformed_files/")
