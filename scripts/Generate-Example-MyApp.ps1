$cmd = @(
    'uv run prismarine',
    '--base .\example\myapp\',
    'generate-client myobject'
)

Invoke-Expression $($cmd -join ' ')
