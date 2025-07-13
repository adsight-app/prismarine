$cmd = @(
    'uv run prismarine',
    'generate-client',
    '--base .\example\myapp\',
    'myobject'
)

Invoke-Expression $($cmd -join ' ')
