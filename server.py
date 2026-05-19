import requests
from mcp.server.fastmcp import FastMCP

# Create a FastMCP server instance (name matters for CLI discovery)
mcp = FastMCP("canada-opendata-mcp")

# Base URL for Canada's open data CKAN API
CKAN_BASE = "https://open.canada.ca/data/api/action"

@mcp.tool()
def search_datasets(query: str, limit: int = 5) -> dict:
    """Search for datasets on the Government of Canada Open Data portal."""
    params = {"q": query, "rows": limit}
    resp = requests.get(f"{CKAN_BASE}/package_search", params=params)
    resp.raise_for_status()
    data = resp.json()
    results = []
    for ds in data.get("result", {}).get("results", []):
        results.append({
            "id": ds["id"],
            "title": ds.get("title", ""),
            "notes": ds.get("notes", "")[:200],
            "num_resources": len(ds.get("resources", []))
        })
    return {"results": results}

@mcp.tool()
def get_dataset_metadata(dataset_id: str) -> dict:
    """Get detailed metadata for a specific dataset by its ID."""
    resp = requests.get(f"{CKAN_BASE}/package_show", params={"id": dataset_id})
    resp.raise_for_status()
    pkg = resp.json()["result"]
    resources = []
    for res in pkg.get("resources", []):
        resources.append({
            "id": res["id"],
            "name": res.get("name", ""),
            "format": res.get("format", ""),
            "url": res.get("url", "")
        })
    return {
        "title": pkg.get("title", ""),
        "description": pkg.get("notes", ""),
        "resources": resources
    }

@mcp.tool()
def download_dataset(resource_id: str) -> dict:
    """Get a downloadable URL for a dataset resource."""
    resp = requests.get(f"{CKAN_BASE}/resource_show", params={"id": resource_id})
    resp.raise_for_status()
    resource = resp.json()["result"]
    return {
        "download_url": resource.get("url"),
        "format": resource.get("format", ""),
        "name": resource.get("name", "")
    }
