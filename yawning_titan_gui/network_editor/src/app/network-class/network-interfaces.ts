export interface NetworkJson {
  nodes: Record<string, Node>,
  edges: Record<string, Record<string, any>>,
  _doc_metadata: NetworkDocMetadata,

  /** Network reset options **/
  // special items to reset
  set_random_entry_nodes?: boolean,
  set_random_high_value_nodes?: boolean,
  set_random_vulnerabilities?: boolean,

  // preference for random node settings
  random_entry_node_placement?: RandomEntryNodePreference,
  random_high_value_node_preference?: RandomHighValueNodePreference,

  // number of special nodes
  num_of_random_entry_nodes?: number,
  num_of_random_high_value_nodes?: number,

  // range for node vulnerabilities
  node_vulnerability_lower_bound?: number,
  node_vulnerability_upper_bound?: number
}

export interface Node {
  uuid: string,
  name: string,
  high_value_node: boolean,
  entry_node: boolean,
  x_pos: number,
  y_pos: number,
  vulnerability: number
}

export interface Edge {
  uuid: string,
  connectedNodes: string[]
}

export interface NetworkDocMetadata {
  uuid: string,
  created_at: Date,
  updated_at: Date,
  name: string,
  description: string,
  author: string,
  locked: boolean
}

/**
 * Preference of how the random entry nodes are placed.
*/
export enum RandomEntryNodePreference {
  // Prefer central nodes
  CENTRAL = "central",

  // Prefer edge nodes
  EDGE = "edge",

  // No preference
  NONE = "none"
}

/**
 * Preference of how the random high value nodes are placed.
*/
export enum RandomHighValueNodePreference {
  // Prefer nodes furthest away from entry nodes.
  FURTHEST_AWAY_FROM_ENTRY = "furthest_away_from_entry",

  // No preference
  NONE = "none"
}
