export interface NetworkJson {
  nodes: Record<string, Node>,
  edges: Record<string, Record<string, any>>,
  _doc_metadata: NetworkDocMetadata
}

export interface Node {
  uuid: string,
  name: string,
  high_value_node: boolean,
  entry_node: boolean,
  classes: string,
  x_pos: number,
  y_pos: number
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
