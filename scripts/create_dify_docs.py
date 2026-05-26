"""One-time script to create text-type documents in Dify Knowledge Base."""
import os, sys, requests

sys.path.insert(0, ".")

api_key = os.environ.get("DIFY_API_KEY", "")
if not api_key:
    print("ERROR: DIFY_API_KEY not set")
    sys.exit(1)

api_base = "https://api.dify.ai/v1"
dataset_id = "3c950956-51f3-4fed-a6dd-b2f01f70bd8b"
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

for fname in ["docs/combined-confluence.md", "docs/combined-jpcoar.md"]:
    text = open(fname, encoding="utf-8").read()
    payload = {
        "name": fname.split("/")[-1],
        "text": text,
        "indexing_technique": "high_quality",
        "process_rule": {
            "mode": "custom",
            "rules": {
                "pre_processing_rules": [
                    {"id": "remove_extra_spaces", "enabled": True},
                    {"id": "remove_urls_emails", "enabled": False},
                ],
                "segmentation": {"separator": "\n\n", "max_tokens": 500},
            },
        },
    }
    # Try both hyphen and underscore variants
    for endpoint in [
        f"{api_base}/datasets/{dataset_id}/documents/create-by-text",
        f"{api_base}/datasets/{dataset_id}/documents/create_by_text",
        f"{api_base}/datasets/{dataset_id}/document/create_by_text",
    ]:
        r = requests.post(endpoint, headers=headers, json=payload)
        print(f"  {endpoint.split('/v1/')[1]} -> {r.status_code}")
        if r.ok:
            print(f"  document_id: {r.json()['document']['id']}")
            break
        elif r.status_code != 404:
            print(f"  ERROR: {r.text[:300]}")
            break
    else:
        print("  All endpoints returned 404. app- key may not have Knowledge Base access.")
