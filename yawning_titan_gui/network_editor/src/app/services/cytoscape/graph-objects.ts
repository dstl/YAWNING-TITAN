import * as cytoscape from "cytoscape";

export enum ElementType {
  NODE = 'node',
  EDGE = 'edge'
}

export interface EdgeObj {
  edgeId: string;
  nodeA: string;
  nodeB: string
}

export interface NodeColourKey {
  label: string;
  cytoscapeStyleSheet: cytoscape.Stylesheet;
  noKeyDisplay?: boolean;
}

export interface SelectedGraphRef {
  id: string
  type: ElementType
}
