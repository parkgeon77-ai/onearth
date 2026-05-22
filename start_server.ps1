# Onearth 로컬 서버 + 터널 실행 스크립트
$dir = "C:\Users\User\onearth"
$port = 8080
$logFile = "$dir\tunnel.log"

Write-Host "Starting Onearth server..." -ForegroundColor Cyan

# Python HTTP server 시작
$pyJob = Start-Job -ScriptBlock {
    param($d, $p)
    python -m http.server $p --directory $d
} -ArgumentList $dir, $port

Start-Sleep -Seconds 2
Write-Host "HTTP server running on port $port" -ForegroundColor Green

# 이전 로그 초기화
if (Test-Path $logFile) { Remove-Item $logFile }

# SSH 터널 시작
$sshJob = Start-Job -ScriptBlock {
    param($lf)
    $output = ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -R 80:localhost:8080 nokey@localhost.run 2>&1
    $output | Out-File $lf -Encoding utf8
} -ArgumentList $logFile

Start-Sleep -Seconds 8

# URL 추출
$content = Get-Content $logFile -ErrorAction SilentlyContinue
$urlLine = $content | Select-String "https://.*lhr\.life"
if ($urlLine) {
    $url = ($urlLine -split "https://")[1].Split(" ")[0]
    $finalUrl = "https://$url"
    Write-Host ""
    Write-Host "=====================================" -ForegroundColor Yellow
    Write-Host " ONEARTH LIVE URL:" -ForegroundColor Yellow
    Write-Host " $finalUrl" -ForegroundColor Green
    Write-Host "=====================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "서버가 실행 중입니다. 이 창을 닫지 마세요." -ForegroundColor Cyan
    Write-Host "종료하려면 Ctrl+C 를 누르세요." -ForegroundColor Gray
} else {
    Write-Host "터널 연결 중..." -ForegroundColor Yellow
    Get-Content $logFile
}

# 지속 유지
try {
    while ($true) {
        Start-Sleep -Seconds 30
        $pyState = Get-Job -Id $pyJob.Id | Select-Object -ExpandProperty State
        $sshState = Get-Job -Id $sshJob.Id | Select-Object -ExpandProperty State
        if ($pyState -ne "Running") {
            Write-Host "HTTP server 재시작..." -ForegroundColor Yellow
            $pyJob = Start-Job -ScriptBlock { param($d,$p) python -m http.server $p --directory $d } -ArgumentList $dir, $port
        }
    }
} finally {
    Stop-Job $pyJob -ErrorAction SilentlyContinue
    Stop-Job $sshJob -ErrorAction SilentlyContinue
}
