import { Component, ViewChild } from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';

@Component({
  selector: 'app-node-properties-sidenav',
  templateUrl: './node-properties-sidenav.component.html',
  styleUrls: ['./node-properties-sidenav.component.scss']
})
export class NodePropertiesSidenavComponent {

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
