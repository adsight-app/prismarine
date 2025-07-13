$cmd = @(
    'uv run prismarine',
    'generate-client',
    '--base .\example\myapp-custom-access\',
    '--dynamo-access-module dynamo_access',
    'myobject'
)


Invoke-Expression $($cmd -join ' ')