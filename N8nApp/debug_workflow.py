#!/usr/bin/env python3

import os
import json
import sys

# Get a workflow file
workflow_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workflows")
if not os.path.exists(workflow_dir):
    print("Workflow directory not found.")
    sys.exit(1)

workflow_files = [f for f in os.listdir(workflow_dir) if f.endswith('.json')]
if not workflow_files:
    print("No workflow files found.")
    sys.exit(1)

sample_file = os.path.join(workflow_dir, workflow_files[0])

try:
    with open(sample_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create a filtered version with only allowed properties
    filtered = {
        "name": data.get("name", ""),
        "nodes": data.get("nodes", []),
        "connections": data.get("connections", {}),
        "settings": {
            "executionOrder": "v1"
        },
        "staticData": {}
    }
    
    # Print original and filtered sizes
    print(f"Original properties: {list(data.keys())}")
    print(f"Filtered properties: {list(filtered.keys())}")
    
    # JSON Schema validation issue could be with nodes structure
    if "nodes" in data:
        sample_node = data["nodes"][0] if data["nodes"] else {}
        print(f"\nSample node original properties: {list(sample_node.keys())}")
        
        filtered_node = {
            "id": sample_node.get("id", ""),
            "name": sample_node.get("name", ""),
            "type": sample_node.get("type", ""),
            "typeVersion": sample_node.get("typeVersion", 1),
            "position": sample_node.get("position", [0, 0]),
            "parameters": sample_node.get("parameters", {})
        }
        print(f"Sample node filtered properties: {list(filtered_node.keys())}")
        
except Exception as e:
    print(f"Error: {str(e)}")
