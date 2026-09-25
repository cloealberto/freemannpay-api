$testExitCode = 1

try {
    docker-compose up -d --build api
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    docker-compose run --rm --build tests
    $testExitCode = $LASTEXITCODE
}
finally {
    docker-compose down
}

exit $testExitCode