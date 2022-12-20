export const test_network = {
  "set_random_entry_nodes": false,
  "random_entry_node_placement": null,
  "set_random_high_value_nodes": false,
  "random_high_value_node_placement": null,
  "node_vulnerability_lower_bound": 0,
  "node_vulnerability_upper_bound": 1,
  "nodes": {
    "64265a12-5201-4bc8-82db-927c24d03363": {
      "uuid": "64265a12-5201-4bc8-82db-927c24d03363",
      "name": "Router 1",
      "high_value_node": false,
      "entry_node": true,
      "classes": "entry_node",
      "x_pos": 0.0,
      "y_pos": 0.0
    },
    "c3fe11c6-c6e0-4450-8250-f2bcea6fbcf9": {
      "uuid": "c3fe11c6-c6e0-4450-8250-f2bcea6fbcf9",
      "name": "Switch 1",
      "high_value_node": false,
      "entry_node": false,
      "classes": "standard_node",
      "x_pos": 0.0,
      "y_pos": 0.0
    }
  },
  "edges": {
    "64265a12-5201-4bc8-82db-927c24d03363": {
      "c3fe11c6-c6e0-4450-8250-f2bcea6fbcf9": {},
    },
    "c3fe11c6-c6e0-4450-8250-f2bcea6fbcf9": {
      "64265a12-5201-4bc8-82db-927c24d03363": {}
    }
  },
  "_doc_metadata": {
    "uuid": "3cb8065c-b337-4c2c-8d43-c8dd8a171665",
    "created_at": "2022-12-15T12:14:53.223103",
    "updated_at": null,
    "name": null,
    "description": null,
    "author": null,
    "locked": false
  }
}
