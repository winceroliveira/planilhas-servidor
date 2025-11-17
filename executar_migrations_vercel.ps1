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
    $response = Invoke-WebRequest -Uri $endpoint -Method POST -UseBasicParsing
    
    Write-Host "`n✅ Sucesso!" -ForegroundColor Green
    Write-Host "Resposta:" -ForegroundColor Cyan
    $response.Content | ConvertFrom-Json | ConvertTo-Json
    
} catch {
    Write-Host "`n❌ Erro ao executar migrations:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    
    if ($_.Exception.Response) {
        try {
            $stream = $_.Exception.Response.GetResponseStream()
            $reader = New-Object System.IO.StreamReader($stream)
            $responseBody = $reader.ReadToEnd()
            Write-Host "`nResposta do servidor:" -ForegroundColor Yellow
            Write-Host $responseBody
            
            # Tentar parsear como JSON
            try {
                $json = $responseBody | ConvertFrom-Json
                Write-Host "`nDetalhes do erro:" -ForegroundColor Yellow
                $json | ConvertTo-Json -Depth 5
            } catch {
                Write-Host "Resposta não é JSON válido"
            }
        } catch {
            Write-Host "Não foi possível ler a resposta do servidor"
        }
    }
    
    Write-Host "`n💡 Possíveis causas:" -ForegroundColor Cyan
    Write-Host "  - DATABASE_URL não configurada na Vercel" -ForegroundColor White
    Write-Host "  - Erro de conexão com o banco de dados" -ForegroundColor White
    Write-Host "  - Verifique os logs na Vercel: Dashboard → Deployments → Logs" -ForegroundColor White
}

Write-Host "`n⚠️ Lembre-se de remover o endpoint após usar!" -ForegroundColor Yellow

