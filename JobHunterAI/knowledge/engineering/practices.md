# Engineering Best Practices

## Concurrency and Performance
- **Non-blocking Operations**: Avoid event-loop starvation by converting blocking synchronous tasks to asynchronous coroutines using `httpx.AsyncClient` where applicable.
- **Diagnostics**: Log detailed tracebacks when exceptions occur. Avoid swallowing exceptions or failing silently.
- **Path Resolution**: Enforce strict canonical path checks on all file operations to mitigate directory traversal exploits.
