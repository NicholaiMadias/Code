# Architecture and roadmap

## Current capabilities

`CLI -> read-only API/local fixtures -> normalize -> risk classification -> JSON/CSV/HTML`

- **Python**: standard-library connectors, deterministic risk logic, CLI, safe offline HTML.
- **PowerShell**: independently testable audit function and a Windows Chrome sensor example.
- **Tests**: mock API reads (no credentials or network), data-classification and HTML-escaping assertions, Pester examples.
- **CI**: Python unit tests and PowerShell Pester tests.

## Auth and data boundaries

- The application never requests passwords and never provisions an identity.
- **Microsoft Graph**: supply a short-lived token scoped to `DeviceManagementManagedDevices.Read.All`; endpoint: `GET /v1.0/deviceManagement/managedDevices`. Pagination errors fail closed to avoid producing an apparently complete partial report. No destructive permissions.
- **Workspace ONE UEM**: supply your tenant's API origin and an OAuth token with device inventory read permissions. The `/api/mdm/devices/search` response and paging vary by UEM release. This starter validates the first response but *does not claim exhaustive device counts*. Extend against the precise `/api/help` / OpenAPI release and add paging fixtures before production reporting.
- Run live commands in a private controlled environment. Reports can contain device names or identifiers, so do not publish them.
- AI integrations are **examples of redacted prompts only**. No external inference endpoint is called.

## Portfolio roadmap (not yet implemented)

1. Add Microsoft Graph authentication using a supported identity library with workload identity/federation; add transient-error backoff.
2. Implement release-pinned Workspace ONE adapters for required tenant response schemas and verified paging.
3. Add authenticated local dashboard/API with role separation, CSRF defense and audit logs.
4. Add signed, opt-in remediation with dry-run, approval, least privilege, rollback, and integration tests.
5. Add ServiceNow/Jira tickets, scoring history, and optional private AI summaries after redaction review.

## API references

- https://learn.microsoft.com/en-us/graph/api/intune-devices-manageddevice-list?view=graph-rest-1.0
- https://developer.omnissa.com/workspace-one-uem-apis/
