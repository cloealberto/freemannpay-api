$ErrorActionPreference = "Stop"

docker compose up -d --wait api
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

docker compose run --build --rm --no-deps tests pytest tests/test_authorization.py -v
exit $LASTEXITCODE
