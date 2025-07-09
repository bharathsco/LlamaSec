# LlamaSec
LlamaSec is an open-source tool that uses Large Language Models (LLMs) to automatically triage security vulnerabilities (CVEs) in your open source dependencies.
Instead of drowning in endless vulnerability alerts, LlamaSec helps you answer:

🔍 Is this CVE actually exploitable in my app?

⚠️ How severe is it, given my environment?

🛠️ What patch or mitigation should I apply?

It connects your SBOM or dependency files with real-time CVE feeds and enriches that data using LLMs like GPT-4 or LLaMA, making vulnerability management contextual, fast, and developer-friendly.

✨ Key Features
Parse dependencies from package-lock.json, requirements.txt, pom.xml, etc.

Fetch real-time CVE data via OSV.dev, GitHub advisories

Ask the LLM: severity, exploitability, patch instructions

CLI or API interface for easy integration

Optional: GitHub PR suggestions, Slack notifications

🔧 Example
bash
Copy
Edit
llama-sec scan --file package-lock.json
Output:

css
Copy
Edit
✅ CVE-2025-1234 affects log4j-core@2.14.0
⚠️ Exploitable: Yes (JNDI lookup enabled by default)
🔧 Fix: Upgrade to 2.17.1
🔍 Why This Matters
Security tools often overwhelm teams with alerts. LlamaSec brings intelligence and prioritization into the equation by combining LLM reasoning with real-world project context.

