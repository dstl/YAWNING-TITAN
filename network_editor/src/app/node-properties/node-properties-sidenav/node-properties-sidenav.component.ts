import { Component, ViewChild } from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';
import { Node } from 'src/app/network-class/network-interfaces';

@Component({
  selector: 'app-node-properties-sidenav',
  templateUrl: './node-properties-sidenav.component.html',
  styleUrls: ['./node-properties-sidenav.component.scss']
})
export class NodePropertiesSidenavComponent {

  public node: Node = null;

  @ViewChild('sidenav') sidenav: MatSidenav;

  public close(): void {
    this.sidenav.close();
  }

  public open(node: Node): void {
    this.node = node;
    this.sidenav.open();
  }
}
