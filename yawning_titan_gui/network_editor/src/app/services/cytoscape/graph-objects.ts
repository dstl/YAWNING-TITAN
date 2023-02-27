import * as cytoscape from "cytoscape";

export enum ElementType {
  NODE = 'node',
  EDGE = 'edge'
}

export interface NodeColourKey {
  label: string;
  cytoscapeStyleSheet: cytoscape.Stylesheet;
  noKeyDisplay?: boolean;
}
