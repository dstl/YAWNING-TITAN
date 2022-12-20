import { Component, Input, ViewChild } from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';

@Component({
  selector: 'app-properties-editor-sidenav',
  templateUrl: './properties-editor-sidenav.component.html',
  styleUrls: ['./properties-editor-sidenav.component.scss']
})
export class PropertiesEditorSidenavComponent {

  public nodeId = null;

  @ViewChild('sidenav') sidenav: MatSidenav;

  public close(): void {
    this.sidenav.close();
  }

  public open(id: string): void {
    this.nodeId = id;
    this.sidenav.open();
  }
}
