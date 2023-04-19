export interface CyBoundingBox {
  x1: number,
  x2: number,
  y1: number,
  y2: number,
  w: number,
  h: number
}

export interface DisplayValue {
  zoom: number,
  pan: { x: number, y: number }
}

export interface ViewportOptions {
  padding: number
}
