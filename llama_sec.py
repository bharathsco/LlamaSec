# llama_sec.py

import argparse
import json
import os
import requests
import openai

# --- Configuration ---
openai.api_key = os.getenv("OPENAI_API_KEY")
OSV_API_URL = "https://api.osv.dev/v1/query"

# --- Functions ---
def get_dependencies_from_package_lock(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    dependencies = list(data.get("dependencies", {}).keys())
    return dependencies

def query_osv(package_name):
    payload = {
        "package": {
            "name": package_name,
            "ecosystem": "npm"
        }
    }
    response = requests.post(OSV_API_URL, json=payload)
    if response.status_code == 200:
        return response.json().get("vulns", [])
    return []

def ask_llm_about_cve(cve_id, summary, config):
    prompt = f"""
You are a security expert.
Given the CVE information below, and the following project context, determine:
1. Whether the CVE is likely exploitable.
2. How severe it is in this context.
3. Recommended patch or workaround.

CVE: {cve_id}
Summary: {summary}
Project Context: {config}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You triage vulnerabilities in open source projects."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def scan(file_path, context_info):
    print(f"🔍 Scanning {file_path} for open source CVEs...")
    packages = get_dependencies_from_package_lock(file_path)
    for pkg in packages:
        vulns = query_osv(pkg)
        for vuln in vulns:
            cve_id = vuln.get("id")
            summary = vuln.get("summary", "No summary available.")
            print(f"\n🚨 {cve_id} affects {pkg}")
            analysis = ask_llm_about_cve(cve_id, summary, context_info)
            print(analysis)

# --- CLI Setup ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LlamaSec - CVE Triage with LLMs")
    parser.add_argument("--file", required=True, help="Path to package-lock.json")
    parser.add_argument("--context", default="Node.js web app using default config.", help="Brief context about your project")
    args = parser.parse_args()

    scan(args.file, args.context)
