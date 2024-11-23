# duckdb-atproto

Querying ATProto from DuckDB by creating an HTTP Secret scoped to your PDS or `api.bsky.app`.

This workflow is for very short-lived, manual queries.

This is not a place of honor.

## Requirements

* duckdb
* Python

## Usage

```bash
Usage: set_bearer_token.py <bearer_token> [<scope>]
```

## Example

Discover your *bearer token* and *host* from the Network tab when you're logged into [bsky.app](https://bsky.app).

```bash
$ ./create_secret.py eyJ0eXAiO<snip> shiitake.us-east.host.bsky.network
Creating duckdb secret atproto_shiitake_us_east_host_bsky_network
┌─────────┐
│ Success │
│ boolean │
├─────────┤
│ true    │
└─────────┘
```

Open `duckdb` and query the API:

```
D select * from read_json('https://shiitake.us-east.host.bsky.network/xrpc/app.bsky.graph.getFollowers?actor=did%3Aplc%3Avc7f4oafdgxsihk4cry2xpze&limit=30');
┌──────────────────────┬───────────────────────────────────────────────────────────────────────────────┬───────────────┐
│      followers       │                                    subject                                    │    cursor     │
│ struct(did varchar…  │ struct(did varchar, handle varchar, displayname varchar, avatar varchar, as…  │    varchar    │
├──────────────────────┼───────────────────────────────────────────────────────────────────────────────┼───────────────┤
│ [{'did': did:plc:t…  │ {'did': did:plc:vc7f4oafdgxsihk4cry2xpze, 'handle': jcsalterego.bsky.social…  │ 3lbmwfgwgqm2c │
└──────────────────────┴───────────────────────────────────────────────────────────────────────────────┴───────────────┘
```
