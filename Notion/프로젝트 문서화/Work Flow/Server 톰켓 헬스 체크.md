---
base: "[[Work Flow.base]]"
할당: []
상태: 검토 중
프로젝트: []
---
```java
 param (
    [ValidateSet("Auto", "Passive")]
    [string]$Mode = "Auto"
)

# ==========================================
# [타임아웃 설정을 위한 커스텀 WebClient 정의]
# ==========================================
$source = @"
using System;
using System.Net;
public class TimeoutWebClient : WebClient {
    protected override WebRequest GetWebRequest(Uri address) {
        WebRequest request = base.GetWebRequest(address);
        if (request != null) {
            request.Timeout = 3000; // 3초
        }
        return request;
    }
}
"@
Add-Type -TypeDefinition $source -ErrorAction SilentlyContinue

# ==========================================
# [공통 환경 설정 및 경로]
# ==========================================
$ScriptPath = $MyInvocation.MyCommand.Path
$BaseDir = Split-Path -Parent $ScriptPath
$targetFile = Join-Path $BaseDir "service_list.txt"
$statusDir = Join-Path $BaseDir "status"
$logDir = Join-Path $BaseDir "logs"

foreach ($dir in @($statusDir, $logDir)) {
    if (-not (Test-Path $dir)) { New-Item -Path $dir -ItemType Directory | Out-Null }
}

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 -bor [Net.SecurityProtocolType]::Tls11 -bor [Net.SecurityProtocolType]::Tls
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }

# 이메일 설정
$testEmail = "[removed marker deleted]@f1soft.co.kr"
$smtpAddr = "smtp.hiworks.com"
$smtpPort = 587
$username = "[removed marker deleted]@f1soft.co.kr"
$password = "epbrqSojIdZDO6y1YuLP"
$fromName = "Jeakyoung"

function Write-Log {
    param([string]$Message, [ConsoleColor]$Color = "White", [bool]$ToFile = $true)
    $TimeStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogDate = Get-Date -Format "yyyy-MM-dd"
    $LogEntry = "[$TimeStamp] $Message"
    
    Write-Host $LogEntry -ForegroundColor $Color
    
    if ($ToFile) {
        $LogFile = Join-Path $logDir "HealthCheck_$LogDate.log"
        $LogEntry | Out-File $LogFile -Append -Encoding UTF8
        Get-ChildItem $logDir -Filter "*.log" | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-3) } | Remove-Item -Force
    }
}

# ==========================================
# [MODE: Auto - 백그라운드 자동 감시]
# ==========================================
if ($Mode -eq "Auto") {
    $TaskName = "F1Soft_HealthChecker"
    if (-not (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue)) {
        $Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"$ScriptPath`" -Mode Auto"
        $Trigger = New-ScheduledTaskTrigger -AtLogOn
        $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
        Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -RunLevel Highest
        Write-Host "[Auto] Task Registered Successfully." -ForegroundColor Green
    }

    Write-Log "[START] Auto Monitoring (Timeout: 3s / Logs: Error Only)" "Cyan" $false

    while($true) {
        if (Test-Path $targetFile) {
            $targets = Get-Content $targetFile | Where-Object { $_ -match "\S" -and $_ -notmatch "^\s*#" }
            foreach ($url in $targets) {
                $url = $url.Trim(); $safeName = $url -replace "[^a-zA-Z0-9]", "_"
                $statusFile = Join-Path $statusDir "$safeName.txt"

                try {
                    $web = New-Object TimeoutWebClient
                    $web.Headers.Add("User-Agent", "Mozilla/5.0")
                    $rawContent = $web.DownloadString($url)
                    
                    if ($rawContent.Trim().ToUpper() -match "UP") {
                        if (Test-Path $statusFile) { 
                            Write-Log "RECOVERED: $url" "Green" $true
                            Remove-Item $statusFile -Force 
                        }
                    } else { throw "Content Mismatch (Not UP)" }
                }
                catch {
                    $detailedError = $_.Exception.Message
                    Write-Log "ERROR: $url - $detailedError" "Red" $true

                    if (-not (Test-Path $statusFile)) {
                        (Get-Date).ToString("yyyy-MM-dd HH:mm:ss") | Out-File $statusFile
                        Write-Log "  -> Failure tracked." "Yellow" $false
                    } else {
                        $fileData = Get-Content $statusFile -Raw
                        $firstFailTime = [DateTime]($fileData.Split("|")[0].Trim())
                        
                        if (((Get-Date) - $firstFailTime).TotalMinutes -ge 1 -and $fileData -notmatch "SENT") {
                            try {
                                Write-Log "  -> Sending Alert Email..." "Magenta" $true
                                $smtp = New-Object Net.Mail.SmtpClient($smtpAddr, $smtpPort)
                                $smtp.EnableSsl = $true
                                $smtp.Credentials = New-Object System.Net.NetworkCredential($username, $password)
                                
                                $fromAddr = New-Object System.Net.Mail.MailAddress($username, $fromName, [System.Text.Encoding]::UTF8)
                                $toAddr = New-Object System.Net.Mail.MailAddress($testEmail)
                                
                                $mail = New-Object Net.Mail.MailMessage($fromAddr, $toAddr)
                                $mail.Subject = "[ERROR] Service Down: $url"
                                $mail.Body = "Target: $url`nError: $detailedError`nDown Since: $firstFailTime"
                                $mail.SubjectEncoding = [System.Text.Encoding]::UTF8
                                $mail.BodyEncoding = [System.Text.Encoding]::UTF8
                                
                                $LogDate = Get-Date -Format "yyyy-MM-dd"
                                $currentLogFile = Join-Path $logDir "HealthCheck_$LogDate.log"
                                if (Test-Path $currentLogFile) {
                                    $attachment = New-Object Net.Mail.Attachment($currentLogFile)
                                    $mail.Attachments.Add($attachment)
                                }

                                $smtp.Send($mail)
                                if ($attachment) { $attachment.Dispose() }
                                $mail.Dispose()

                                "$($firstFailTime.ToString('yyyy-MM-dd HH:mm:ss')) | SENT" | Out-File $statusFile -Force
                                Write-Log "  [SUCCESS] Email Sent as '$fromName'." "Green" $true
                            } catch {
                                Write-Log "  [MAIL FAIL] $($_.Exception.Message)" "Red" $true
                            }
                        }
                    }
                }
                finally { if ($web) { $web.Dispose() } }
            }
        }
        Start-Sleep -Seconds 60
    }
}

# ==========================================
# [MODE: Passive - 수동 상태 체크]
# ==========================================
else {
    Write-Host "`n--- [Passive Mode] Status Check (Timeout: 3s) ---" -ForegroundColor Cyan
    if (-not (Test-Path $targetFile)) { Write-Host "[ERROR]: service_list.txt not found." -ForegroundColor Red; return }

    $targets = Get-Content $targetFile | Where-Object { $_ -match "\S" -and $_ -notmatch "^\s*#" }
    foreach ($url in $targets) {
        $url = $url.Trim()
        try {
            $web = New-Object TimeoutWebClient
            $web.Headers.Add("User-Agent", "Mozilla/5.0")
            $start = Get-Date
            $rawContent = $web.DownloadString($url)
            $end = Get-Date
            $time = [Math]::Round(($end - $start).TotalMilliseconds, 0)
            
            if ($rawContent.Trim().ToUpper() -match "UP") {
                Write-Host " [OK]   " -NoNewline -ForegroundColor Green
                Write-Host "$url ($($time)ms)"
            } else { throw "Response not 'UP'" }
        }
        catch {
            Write-Host " [FAIL] " -NoNewline -ForegroundColor Red
            Write-Host "$url - $($_.Exception.Message)"
        }
        finally { if ($web) { $web.Dispose() } }
    }
    Write-Host "-------------------------------------------------`n"
	} 
```

→ SMTP 메일 송부 접속주소

$smtpAddr = "smtp.hiworks.com"
$smtpPort = 587
$username = "[removed marker deleted]@f1soft.co.kr"
$password = "epbrqSojIdZDO6y1YuLP"



→ health Checker 시행 방법

→ C:\scripts 파일경로

.\check_tomcat.ps1 (PS 시행 방법 Debug모드)

작동방식 → 1분단위로 health Checker 를 지속적으로 돌린다 / 주기가 돌아올때까지 응답이 없는 경우

→ SMTP 방식으로 지정되어있는 사용자에게 메일을 발송


![[image 212.png]]

→ BG_Proccess 메모리 상시 사용 정보

.\check_tomcat.ps1 -Mode Auto

.\check_tomcat.ps1 -Mode Passive

아래가 로컬


│ 메인 (/)     │ [https://reel-trip-test-5zkrcqawz-[removed marker deleted]-2257s-projects.vercel.app](https://reel-trip-test-5zkrcqawz-[removed marker deleted]-2257s-projects.vercel.app/test-ui)
│ 테스트 UI    │ [https://reel-trip-test-5zkrcqawz-[removed marker deleted]-2257s-projects.vercel.app/test-ui](https://reel-trip-test-5zkrcqawz-[removed marker deleted]-2257s-projects.vercel.app/test-ui)
│ API Docs UI  │ [https://your-domain.vercel.app/BE/api-docs](https://your-domain.vercel.app/BE/api-docs)                   
│ OpenAPI JSON │ [https://your-domain.vercel.app/BE/docs](https://your-domain.vercel.app/BE/docs)                       
[<u>https://reel-trip-api.vercel.app/</u>](https://reel-trip-api.vercel.app/)

<API_Server + Test + Doc>  [https://reel-trip-api.vercel.app/test-ui](https://reel-trip-api.vercel.app/test-ui)

<PRD_Server> [https://reel-trip-test.vercel.app/auth/login](https://reel-trip-test.vercel.app/auth/login)


포트폴리오 목적이면 "실제 대규모"보다 "대규모를 고려한 설계"를 보여주는 게 핵심이에요.

IVFFlat보다 HNSW가 더 유리한 이유

- "왜 이 인덱스를 선택했는가?"
- "트레이드오프를 이해하고 있는가?"

HNSW는 현재 업계 표준이에요 (Pinecone, Weaviate 등 대부분 HNSW 기반). IVFFlat은 데이터가 정적일 때 유효한데, 여행 추천 서비스는 데이터가 계속 추가되는 구조라
HNSW가 더 자연스러운 선택이에요.

포트폴리오에서 어필할 수 있는 구조

현재                       추가하면 좋은 것
─────────────────────────────────────────
pgvector 풀스캔            HNSW 인덱스
단순 임베딩 저장           임베딩 배치 파이프라인
단일 유사도 검색           하이브리드 검색 (벡터 + 키워드)

하이브리드 검색이 특히 임팩트 있어요.

- - 벡터 유사도 + 키워드 매칭 결합
SELECT *,
(1 - (embedding <=> $1::vector)) * 0.7 +
ts_rank(to_tsvector(content), plainto_tsquery($2)) * 0.3 AS score
FROM documents
ORDER BY score DESC
