# shillelagh-gristapi

Shillelagh adapter for querying Grist Documents.


#### `~/.config/shillelagh/shillelagh.yaml`
```
gristapi:
  api_key: <replace-with-your-key>
  server: <replace-with-your-server>
  org_id: <replace-with-your-org-id>
```

- find your api_key in your profile settings,
- server can be `https://templates.getgrist.com`,
- find your org_id with `curl -H "Authorization: Bearer <replace-with-your-apy-key" "https://templates.getgrist.com/api/orgs/" | jq '.[]|.id'`.

#### Python args
```python
connection = connect(
    ":memory:",
    adapter_kwargs={
        "gristapi": {
            "api_key": os.environ["GRIST_API_KEY"],
            "server": os.environ["GRIST_SERVER"],
            "org_id": os.environ["GRIST_ORG_ID"],
        }
    },
)
```

#### Superset args

SQLALCHEMY URI
```
shillelagh+safe://
```

Engine parameters
```
{"connect_args":{"adapters":["genericjsonapi","githubapi","datasetteapi","htmltableapi","s3selectapi","socrataapi","weatherapi","gristapi"],"adapter_kwargs":{"gristapi":{"api_key":"8873ad509f6f97497d5f20b9b10d57312409d364","server":"https://grist.kantan.fr","org_id":"3"}}}}
```

| SQLALCHEMY URI | Engine parameters |
| --- | --- |
| ![screenshot base](images/screenshot_base.png)| ![screenshot parametres](images/screenshot_parametres.png) | 
