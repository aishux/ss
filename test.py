from azure.cli.core import get_default_cli

az_cli = get_default_cli()

az_cli.invoke(['login', '--service-principal', '-u', '<appId>', '-p', 'password','--tenant','teanat id'])
