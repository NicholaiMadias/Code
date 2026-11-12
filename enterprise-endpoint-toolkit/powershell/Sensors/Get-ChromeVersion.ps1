# Workspace ONE UEM example sensor: read-only Windows Google Chrome version.
# Return a version string if installed; otherwise return 'Not Installed'.
# Validate response type in your UEM tenant before assignment.
$ErrorActionPreference = 'Stop'
$locations = @(
    'HKLM:\SOFTWARE\Google\Chrome\BLBeacon',
    'HKLM:\SOFTWARE\WOW6432Node\Google\Chrome\BLBeacon'
)
foreach ($location in $locations) {
    if (Test-Path $location) {
        $version = (Get-ItemProperty -LiteralPath $location -Name 'version' -ErrorAction SilentlyContinue).version
        if ($version) { Write-Output ([string]$version); exit 0 }
    }
}
Write-Output 'Not Installed'
