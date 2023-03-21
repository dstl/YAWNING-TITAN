export interface NetworkJson {
  nodes: Record<string, Node>,
  edges: Record<string, Record<string, any>>,
  _doc_metadata: NetworkDocMetadata,

  /** Network reset options **/
  // Entry node reset behaviour
  set_random_entry_nodes: boolean,
  random_entry_node_preference: RandomEntryNodePreference,
  num_of_random_entry_nodes: number,

  // High Value reset behaviour
  set_random_high_value_nodes: boolean,
  random_high_value_node_preference: RandomHighValueNodePreference,
  num_of_random_high_value_nodes: number,

  // Node Vulnerabilities
  set_random_vulnerabilities: boolean,
  node_vulnerability_lower_bound: number,
  node_vulnerability_upper_bound: number
}

export interface NetworkSettings {
  entryNode: EntryNodeBehaviour,
  highValueNode: HighValueNodeBehaviour,
  vulnerability: VulnerabilitiesBehaviour
}

export interface EntryNodeBehaviour {
  set_random_entry_nodes?: boolean,
  random_entry_node_preference?: RandomEntryNodePreference,
  num_of_random_entry_nodes?: number,
}

export interface HighValueNodeBehaviour {
  set_random_high_value_nodes?: boolean,
  random_high_value_node_preference?: RandomHighValueNodePreference,
  num_of_random_high_value_nodes?: number,
}

export interface VulnerabilitiesBehaviour {
  set_random_vulnerabilities?: boolean,
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
  created_at: string,
  updated_at: string,
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
  CENTRAL = "CENTRAL",

  // Prefer edge nodes
  EDGE = "EDGE",

  // No preference
  NONE = "NONE"
}

/**
 * Preference of how the random high value nodes are placed.
*/
export enum RandomHighValueNodePreference {
  // Prefer nodes furthest away from entry nodes.
  FURTHEST_AWAY_FROM_ENTRY = "FURTHEST_AWAY_FROM_ENTRY",

  // No preference
  NONE = "NONE"
}
