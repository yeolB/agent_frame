param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet(
        "turn-start",
        "turn-stop",
        "session-start",
        "session-end",
        "status",
        "next-id",
        "index",
        "validate",
        "memory-complete",
        "review-complete"
    )]
    [string]$Action
)

$ErrorActionPreference = "Stop"
$continuityScript = Join-Path $PSScriptRoot "continuity"
$versionProbe = "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"
$candidates = @(
    @{ Command = "py"; PrefixArguments = @("-3") },
    @{ Command = "python"; PrefixArguments = @() },
    @{ Command = "python3"; PrefixArguments = @() }
)

foreach ($candidate in $candidates) {
    $commandName = $candidate.Command
    if ($null -eq (Get-Command $commandName -ErrorAction SilentlyContinue)) {
        continue
    }

    $prefixArguments = $candidate.PrefixArguments
    & $commandName @prefixArguments -c $versionProbe 2>$null
    if ($LASTEXITCODE -ne 0) {
        continue
    }

    & $commandName @prefixArguments $continuityScript $Action
    exit $LASTEXITCODE
}

Write-Error "Continuity hooks require Python 3.10 or newer. Install Python or make py/python/python3 available on PATH."
exit 1
