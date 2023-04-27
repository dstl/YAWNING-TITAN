export interface Extent {
  zoom: number,
  pan: { x: number, y: number }
  bb: CyBoundingBox
}

export interface CyBoundingBox {
  x1: number,
  x2: number,
  y1: number,
  y2: number,
  w: number,
  h: number
}

export interface DisplayValue {
  zoom: {
    h: number,
    w: number
  },
  pan: { x: number, y: number }
}
