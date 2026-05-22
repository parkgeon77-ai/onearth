# Onearth Launcher
$dir = "C:\Users\User\onearth"
$port = 8080
$localUrl = "http://localhost:$port"

# 이미 실행 중인지 확인
$portInUse = netstat -ano | Select-String ":$port " | Select-Object -First 1
if ($portInUse) {
    # 서버 이미 실행 중 — 브라우저만 열기
    Start-Process $localUrl
    exit
}

# Python 서버 시작
Start-Process python -ArgumentList "-m http.server $port --directory `"$dir`"" -WindowStyle Hidden

# SSH 터널 시작 (선택적 — 외부 공개 URL 원할 시)
$tunnelLog = "$dir\tunnel.log"
if (Test-Path $tunnelLog) { Remove-Item $tunnelLog }
Start-Process powershell -ArgumentList "-WindowStyle Hidden -Command `"ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=20 -R 80:localhost:$port nokey@localhost.run 2>&1 | Out-File '$tunnelLog' -Encoding utf8`"" -WindowStyle Hidden

# 서버 준비될 때까지 대기 후 브라우저 오픈
Start-Sleep -Seconds 2
Start-Process $localUrl
