Set-StrictMode -Version Latest

function Get-EndpointComplianceAudit {
    <#
    .SYNOPSIS
    Classify supplied endpoint records without modifying any device or directory.
    .EXAMPLE
    @([pscustomobject]@{ deviceName='LAB-01'; complianceState='compliant' }) |
      Get-EndpointComplianceAudit
    #>
    [CmdletBinding()]
    param(
        [Parameter(ValueFromPipeline = $true, Mandatory = $true)]
        [psobject]$Device,
        [ValidateRange(1, 3650)]
        [int]$StaleDays = 30
    )
    process {
        $props = $Device.PSObject.Properties
        $name = if ($props['deviceName']) { [string]$Device.deviceName } elseif ($props['Name']) { [string]$Device.Name } else { 'Unnamed' }
        $state = if ($props['complianceState']) { [string]$Device.complianceState } else { 'unknown' }
        $state = $state.ToLowerInvariant()
        if ($state -notin @('compliant', 'noncompliant')) { $state = 'unknown' }
        $freshness = 'unknown'
        if ($props['lastSyncDateTime'] -and $Device.lastSyncDateTime) {
            $parsed = [datetimeoffset]::MinValue
            if ([datetimeoffset]::TryParse([string]$Device.lastSyncDateTime, [ref]$parsed)) {
                $freshness = if (([datetimeoffset]::UtcNow - $parsed.ToUniversalTime()).TotalDays -gt $StaleDays) { 'stale' } else { 'recent' }
            }
        }
        $risk = if ($state -eq 'noncompliant') { 'high' } elseif ($freshness -eq 'stale') { 'medium' } elseif ($state -eq 'unknown' -or $freshness -eq 'unknown') { 'unknown' } else { 'low' }
        [pscustomobject]@{
            Name = $name
            Compliance = $state
            Freshness = $freshness
            Risk = $risk
        }
    }
}
Export-ModuleMember -Function Get-EndpointComplianceAudit
