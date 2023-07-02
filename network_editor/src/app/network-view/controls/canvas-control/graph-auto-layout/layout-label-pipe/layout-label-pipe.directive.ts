import { Pipe } from '@angular/core';

@Pipe({
  name: 'appLayoutLabelPipe'
})
export class LayoutLabelPipeDirective {
  /**
   * Converts snake case to title case e.g.
   * snake_case => Snake Case
   * @param str
   * @returns
   */
  public transform(str: string): string {
    return str.replace (/^[-_]*(.)/, (_, c) => c.toUpperCase())
    .replace (/[-_]+(.)/g, (_, c) => ' ' + c.toUpperCase());
  }
}
