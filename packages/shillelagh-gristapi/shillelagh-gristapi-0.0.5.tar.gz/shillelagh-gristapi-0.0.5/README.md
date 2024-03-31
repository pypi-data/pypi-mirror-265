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

```json
{
  "connect_args":
    {
      "adapters":
        ["genericjsonapi","githubapi","datasetteapi","htmltableapi","s3selectapi","socrataapi","weatherapi","gristapi"],
      "adapter_kwargs":
        {
          "gristapi":{
            "api_key": "<REPLACE_WITH_YOUR_API_KEY>",
            "server": "<REPLACE_WITH_YOUR_SERVER_URL>",
            "org_id": "<REPLACE_WITH_YOUR_ORD_ID>"
          }
        }
    }
}
```

| SQLALCHEMY URI | Engine parameters |
| --- | --- |
| ![screenshot base](images/screenshot_base.png)| ![screenshot parametres](images/screenshot_parametres.png) | 
