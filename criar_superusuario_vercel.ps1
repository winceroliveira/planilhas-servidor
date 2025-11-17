# Script para criar superusuário na Vercel via endpoint
# ⚠️ REMOVER O ENDPOINT APÓS USAR!

param(
    [Parameter(Mandatory=$true)]
    [string]$UrlProjeto,
    
    [Parameter(Mandatory=$true)]
    [string]$Username,
    
    [Parameter(Mandatory=$true)]
    [string]$Email,
    
    [Parameter(Mandatory=$true)]
    [string]$Password
)

# Garantir que a URL tenha https://
if (-not $UrlProjeto.StartsWith("http://") -and -not $UrlProjeto.StartsWith("https://")) {
    $UrlProjeto = "https://$UrlProjeto"
}

$endpoint = "$UrlProjeto/api/create-superuser/"

Write-Host "Criando superusuário em: $endpoint" -ForegroundColor Yellow
Write-Host "Username: $Username" -ForegroundColor Cyan
Write-Host "Email: $Email" -ForegroundColor Cyan

# Criar body JSON
$body = @{
    username = $Username
    email = $Email
    password = $Password
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri $endpoint -Method POST -Body $body -ContentType "application/json" -UseBasicParsing -ErrorAction Stop
    
    Write-Host "`n✅ Sucesso!" -ForegroundColor Green
    Write-Host "Status Code: $($response.StatusCode)" -ForegroundColor Cyan
    
    if ($response.Content) {
        Write-Host "`nResposta JSON:" -ForegroundColor Cyan
        try {
            $json = $response.Content | ConvertFrom-Json
            $json | ConvertTo-Json -Depth 10 | Write-Host
            
            Write-Host "`n🎉 Superusuário criado com sucesso!" -ForegroundColor Green
            Write-Host "Você pode fazer login no admin com:" -ForegroundColor Yellow
            Write-Host "  Username: $($json.username)" -ForegroundColor White
            Write-Host "  Email: $($json.email)" -ForegroundColor White
        } catch {
            Write-Host "Resposta (texto):" -ForegroundColor Yellow
            Write-Host $response.Content
        }
    }
    
} catch {
    Write-Host "`n❌ Erro ao criar superusuário:" -ForegroundColor Red
    Write-Host "Mensagem: $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.Exception.Response) {
        try {
            $errorResponse = $_.Exception.Response
            $stream = $errorResponse.GetResponseStream()
            $reader = New-Object System.IO.StreamReader($stream)
            $responseBody = $reader.ReadToEnd()
            $reader.Close()
            $stream.Close()
            
            Write-Host "`nResposta do Servidor:" -ForegroundColor Yellow
            if ($responseBody) {
                Write-Host $responseBody
                
                try {
                    $json = $responseBody | ConvertFrom-Json
                    Write-Host "`nDetalhes do Erro:" -ForegroundColor Red
                    $json | ConvertTo-Json -Depth 10 | Write-Host
                } catch {
                    Write-Host "Resposta não é JSON válido"
                }
            }
        } catch {
            Write-Host "Não foi possível ler a resposta do servidor"
        }
    }
}

Write-Host "`n⚠️ Lembre-se de remover o endpoint após usar!" -ForegroundColor Yellow

