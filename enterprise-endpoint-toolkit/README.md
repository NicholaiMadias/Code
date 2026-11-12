# Enterprise Endpoint Automation Toolkit

A **read-only, demo-first** portfolio toolkit for Endpoint Engineering, Workspace ONE UEM, Microsoft Intune, and infrastructure operations. This is separate from the repository's Nexus Arcade/Toolbox teaching examples.

## Implemented

- Standardize sample, Microsoft Graph Intune, and Workspace ONE UEM device records.
- Flag non-compliance and stale check-ins, preserving **unknown** values rather than treating them as compliant.
- Generate a JSON report, CSV inventory, and self-contained HTML dashboard from the same data.
- Use a documented, permission-scoped Graph managed-devices endpoint with safe pagination.
- Use a configurable Workspace ONE UEM REST host and read-only device search (response shape depends on tenant/release).
- PowerShell audit function and Windows Chrome-version Workspace ONE sensor example.
- Unit tests, Pester tests, GitHub Actions and redacted AI prompt examples.

## Quick start (Python 3.11+)

```sh
cd enterprise-endpoint-toolkit
python -m pip install -e .
endpoint-toolkit demo --out reports
python -m unittest discover -s tests -v
```

Open `reports/dashboard.html`. It is static, contains **sample data only** in demo mode, and has no tracking or external assets.

To analyze a JSON array or a JSON object with `value` or `Devices`:

```sh
endpoint-toolkit analyze --input examples/devices.json --out reports
```

### Optional live, read-only inventory

Microsoft Intune requires an existing OAuth access token with **DeviceManagementManagedDevices.Read.All** and an Intune license:

```sh
export GRAPH_ACCESS_TOKEN="<short-lived access token>"
endpoint-toolkit graph --out reports
```

Workspace ONE UEM requires your SaaS/tenant API host and an existing OAuth token with device-read access:

```sh
export WS1_API_URL="https://as0000.awmdm.com"
export WS1_ACCESS_TOKEN="<short-lived access token>"
# If your tenant requires an API tenant code:
export WS1_TENANT_CODE="<tenant code>"
endpoint-toolkit workspace-one --out reports
```

Tokens are read from environment variables and are not stored or displayed by this program. **Never commit tokens**, production exports, or personal device identifiers. Do not upload production reports to a public repository. Review tenant API/help and role permissions before enabling this integration.

## PowerShell

```powershell
Import-Module ./powershell/EndpointToolkit.psm1 -Force
Get-EndpointComplianceAudit -Device @(
  [pscustomobject]@{ deviceName='LAB-01'; complianceState='noncompliant'; lastSyncDateTime='2025-01-01T00:00:00Z' }
)
# Example local Workspace ONE sensor (Windows only):
./powershell/Sensors/Get-ChromeVersion.ps1
```

For Pester 5+: `Invoke-Pester ./tests/EndpointToolkit.Tests.ps1 -CI`.

## Security and scope

No tenant administration or device commands. No automatic remediation. No interactive sign-in or long-lived tokens. Graph paging is pinned to `graph.microsoft.com`; Workspace ONE calls stay on the configured HTTPS tenant host. Local input is untrusted, and the HTML reporter escapes all fields. Use `docs/ARCHITECTURE.md` for the roadmap and platform-specific limitations.

**API documentation:** [Microsoft Graph managedDevices](https://learn.microsoft.com/en-us/graph/api/intune-devices-manageddevice-list?view=graph-rest-1.0) · [Omnissa Workspace ONE UEM API releases](https://developer.omnissa.com/workspace-one-uem-apis/).
