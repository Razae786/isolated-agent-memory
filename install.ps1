param (
    [string]$StorageDrive = "D:"
)

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host " Isolated Agent Memory - 1-Click Installer" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

$StorageRoot = "$StorageDrive\AntigravityMemory"
New-Item -ItemType Directory -Path "$StorageRoot\projects" -Force | Out-Null
Write-Host "[+] Initialized memory directory at: $StorageRoot" -ForegroundColor Green

# Install python package in editable mode
pip install -e .
if ($LASTEXITCODE -eq 0) {
    Write-Host "[+] Successfully installed 'vault' CLI utility." -ForegroundColor Green
} else {
    Write-Host "[!] Warning: pip install failed. You can still use python -m memory_vault.cli" -ForegroundColor Yellow
}

Write-Host "`n[+] Configured! Your agents will now automatically isolate memory per project." -ForegroundColor Green
Write-Host "Run 'vault list' to see active memory partitions." -ForegroundColor White
