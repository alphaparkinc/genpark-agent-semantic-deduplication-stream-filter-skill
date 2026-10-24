import sys
import json
from client import SemanticDeduplicationStreamFilter

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "deduplicate_item",
                        "description": "Filters redundant text snippets based on token Jaccard similarity.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "item_id": {"type": "string"},
                                "content": {"type": "string"}
                            }
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        args = params.get("arguments", {})
        filter_engine = SemanticDeduplicationStreamFilter()
        res = filter_engine.process_item(args.get("item_id", "item_1"), args.get("content", ""))
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
            }
        }
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    filter_engine = SemanticDeduplicationStreamFilter()
    print(json.dumps(filter_engine.process_item("t1", "Hello world test"), indent=2))

if __name__ == "__main__":
    main()
