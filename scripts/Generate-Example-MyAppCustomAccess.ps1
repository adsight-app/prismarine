$cmd = @(
    'uv run prismarine',
    '--base .\example\myapp-custom-access\',
    '--dynamo-access-module dynamo_access',
    'generate-client myobject'
)


Invoke-Expression $($cmd -join ' ')