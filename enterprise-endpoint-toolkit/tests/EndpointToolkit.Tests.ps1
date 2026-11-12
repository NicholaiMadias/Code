BeforeAll {
    Import-Module "$PSScriptRoot/../powershell/EndpointToolkit.psm1" -Force
}
Describe 'Get-EndpointComplianceAudit' {
    It 'flags missing status and check-in as unknown' {
        $result = [pscustomobject]@{ deviceName = 'LAB-01' } | Get-EndpointComplianceAudit
        $result.Risk | Should -Be 'unknown'
    }
    It 'identifies explicit non-compliance even without timestamp' {
        $result = [pscustomobject]@{ deviceName = 'LAB-02'; complianceState = 'noncompliant' } | Get-EndpointComplianceAudit
        $result.Risk | Should -Be 'high'
    }
    It 'does not mark valid recent compliant records as high risk' {
        $result = [pscustomobject]@{ deviceName = 'LAB-03'; complianceState = 'compliant'; lastSyncDateTime = ([datetimeoffset]::UtcNow.ToString('o')) } | Get-EndpointComplianceAudit
        $result.Risk | Should -Be 'low'
    }
}
