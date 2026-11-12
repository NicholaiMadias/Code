import io
import json
import unittest
from endpoint_toolkit.api import graph_managed_devices, workspace_one_devices

class Response(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *_): self.close()

class ApiTests(unittest.TestCase):
    def test_graph_pages(self):
        urls = []
        def opener(request, timeout):
            urls.append(request.full_url)
            if len(urls) == 1:
                body = {"value": [{"id": "a"}], "@odata.nextLink": "https://graph.microsoft.com/v1.0/deviceManagement/managedDevices?$skiptoken=x"}
            else:
                body = {"value": [{"id": "b"}]}
            self.assertEqual(request.get_method(), "GET")
            return Response(json.dumps(body).encode())
        self.assertEqual(len(graph_managed_devices("placeholder", opener=opener)), 2)

    def test_graph_next_link_cannot_escape_host(self):
        def opener(request, timeout):
            return Response(json.dumps({"value": [], "@odata.nextLink": "https://evil.example/v1.0/deviceManagement/managedDevices"}).encode())
        with self.assertRaises(ValueError):
            graph_managed_devices("placeholder", opener=opener)

    def test_graph_fails_closed_on_truncation(self):
        def opener(request, timeout):
            return Response(json.dumps({"value": [], "@odata.nextLink": "https://graph.microsoft.com/v1.0/deviceManagement/managedDevices?$skiptoken=more"}).encode())
        with self.assertRaises(ValueError):
            graph_managed_devices("placeholder", max_pages=1, opener=opener)

    def test_ws1_origin_and_partial_page(self):
        def opener(request, timeout):
            self.assertEqual(request.get_method(), "GET")
            return Response(json.dumps({"Devices": [{"Id": 1}], "Total": 5}).encode())
        with self.assertRaises(ValueError):
            workspace_one_devices("https://my-tenant.example", "placeholder", opener=opener)
        with self.assertRaises(ValueError):
            workspace_one_devices("http://my-tenant.example", "placeholder", opener=opener)

if __name__ == "__main__":
    unittest.main()
