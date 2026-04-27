$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$prefix = "http://127.0.0.1:4173/"

$contentTypes = @{
  ".html" = "text/html; charset=utf-8"
  ".css" = "text/css; charset=utf-8"
  ".js" = "text/javascript; charset=utf-8"
  ".json" = "application/json; charset=utf-8"
  ".csv" = "text/csv; charset=utf-8"
  ".png" = "image/png"
  ".ico" = "image/x-icon"
  ".webmanifest" = "application/manifest+json"
}

$listener = [System.Net.HttpListener]::new()
$listener.Prefixes.Add($prefix)
$listener.Start()

Write-Host "Tankzeit lokal gestartet:"
Write-Host "  $prefix"
Write-Host "  ${prefix}sparrechner.html"
Write-Host ""
Write-Host "Zum Beenden: Strg + C"

while ($listener.IsListening) {
  $context = $listener.GetContext()
  $requestPath = [Uri]::UnescapeDataString($context.Request.Url.AbsolutePath.TrimStart("/"))
  if ([string]::IsNullOrWhiteSpace($requestPath)) {
    $requestPath = "index.html"
  }

  $filePath = [System.IO.Path]::GetFullPath((Join-Path $root $requestPath))
  if (-not $filePath.StartsWith($root, [System.StringComparison]::OrdinalIgnoreCase)) {
    $context.Response.StatusCode = 403
    $context.Response.Close()
    continue
  }

  if (-not (Test-Path -LiteralPath $filePath -PathType Leaf)) {
    $context.Response.StatusCode = 404
    $context.Response.Close()
    continue
  }

  $extension = [System.IO.Path]::GetExtension($filePath).ToLowerInvariant()
  $context.Response.ContentType = if ($contentTypes.ContainsKey($extension)) {
    $contentTypes[$extension]
  } else {
    "application/octet-stream"
  }

  $bytes = [System.IO.File]::ReadAllBytes($filePath)
  $context.Response.ContentLength64 = $bytes.Length
  $context.Response.OutputStream.Write($bytes, 0, $bytes.Length)
  $context.Response.Close()
}
