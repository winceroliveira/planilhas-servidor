# Script para executar migrations na Vercel via endpoint
# Substitua SEU-PROJETO pela URL real do seu projeto na Vercel

param(
    [Parameter(Mandatory=$true)]
    [string]$UrlProjeto
)

# Garantir que a URL tenha https://
if (-not $UrlProjeto.StartsWith("http://") -and -not $UrlProjeto.StartsWith("https://")) {
    $UrlProjeto = "https://$UrlProjeto"
}

$endpoint = "$UrlProjeto/api/migrate/"

Write-Host "Executando migrations em: $endpoint" -ForegroundColor Yellow

try {
    $response = Invoke-WebRequest -Uri $endpoint -Method POST -UseBasicParsing -ErrorAction Stop
    
    Write-Host "`n✅ Sucesso!" -ForegroundColor Green
    Write-Host "Status Code: $($response.StatusCode)" -ForegroundColor Cyan
    
    if ($response.Content) {
        Write-Host "`nResposta JSON:" -ForegroundColor Cyan
        try {
            $json = $response.Content | ConvertFrom-Json
            $json | ConvertTo-Json -Depth 10 | Write-Host
        } catch {
            Write-Host "Resposta (texto):" -ForegroundColor Yellow
            Write-Host $response.Content
        }
    }
    
} catch {
    Write-Host "`n❌ Erro ao executar migrations:" -ForegroundColor Red
    Write-Host "Mensagem: $($_.Exception.Message)" -ForegroundColor Red
    
    # Tentar capturar a resposta do erro
    if ($_.Exception.Response) {
        try {
            $errorResponse = $_.Exception.Response
            $stream = $errorResponse.GetResponseStream()
            $reader = New-Object System.IO.StreamReader($stream)
            $responseBody = $reader.ReadToEnd()
            $reader.Close()
            $stream.Close()
            
            Write-Host "`n═══════════════════════════════════════" -ForegroundColor Yellow
            Write-Host "Resposta do Servidor (Status: $($errorResponse.StatusCode.value__)):" -ForegroundColor Yellow
            Write-Host "═══════════════════════════════════════" -ForegroundColor Yellow
            
            if ($responseBody) {
                Write-Host $responseBody
                
                # Tentar parsear como JSON
                try {
                    $json = $responseBody | ConvertFrom-Json
                    Write-Host "`n═══════════════════════════════════════" -ForegroundColor Cyan
                    Write-Host "Detalhes do Erro (JSON):" -ForegroundColor Cyan
                    Write-Host "═══════════════════════════════════════" -ForegroundColor Cyan
                    $json | ConvertTo-Json -Depth 10 | Write-Host
                    
                    if ($json.debug) {
                        Write-Host "`n🔍 Informações de Debug:" -ForegroundColor Magenta
                        $json.debug | ConvertTo-Json | Write-Host
                    }
                    
                    if ($json.traceback) {
                        Write-Host "`n📋 Traceback:" -ForegroundColor Red
                        $json.traceback | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
                    }
                    
                    if ($json.help) {
                        Write-Host "`n💡 Ajuda:" -ForegroundColor Green
                        Write-Host "  $($json.help)" -ForegroundColor White
                    }
                } catch {
                    Write-Host "`n⚠️ Resposta não é JSON válido" -ForegroundColor Yellow
                }
            } else {
                Write-Host "Resposta vazia do servidor" -ForegroundColor Yellow
            }
        } catch {
            Write-Host "`n⚠️ Não foi possível ler a resposta do servidor: $($_.Exception.Message)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "`n💡 Possíveis causas:" -ForegroundColor Cyan
        Write-Host "  - DATABASE_URL ou POSTGRES_URL não configurada na Vercel" -ForegroundColor White
        Write-Host "  - Erro de conexão com o banco de dados" -ForegroundColor White
        Write-Host "  - Erro de inicialização do Django" -ForegroundColor White
        Write-Host "  - Verifique os logs na Vercel: Dashboard → Deployments → Logs" -ForegroundColor White
    }
}

Write-Host "`n⚠️ Lembre-se de remover o endpoint após usar!" -ForegroundColor Yellow

