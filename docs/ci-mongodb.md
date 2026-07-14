# MongoDB CI integration

## Status

The Django CI workflow validates MongoDB connectivity and basic document operations against a real MongoDB service container.

## Service configuration

GitHub Actions starts MongoDB with:

- image: `mongo:8.0`;
- database: `core_test`;
- host port: `27017`;
- health check: `mongosh --quiet --eval 'db.adminCommand({ ping: 1 })'`.

The service runs without authentication because it is isolated inside the ephemeral CI runner.

## Validation performed

After Python dependencies are installed, the workflow uses the project's pinned `pymongo` dependency to:

1. create a `MongoClient` with a five-second server-selection timeout;
2. execute an administrative `ping`;
3. insert a marker document into `core_test.ci_integration`;
4. read the document back and validate its contents;
5. delete the document;
6. confirm that it no longer exists;
7. close the client.

This proves that MongoDB is not only running, but can be reached and used by the same Python dependency set as the application.

## Environment variables

The validation honors these CI settings:

```text
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_INITDB_DATABASE=core_test
```

## Scope

This integration covers connectivity and basic CRUD behavior. It does not yet validate:

- authentication;
- replica sets;
- transactions;
- production connection strings;
- application-specific MongoDB repositories or background workers.

Those can be added later if the application starts depending on those capabilities during automated tests.
