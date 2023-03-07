import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MaterialModule } from '../material.module';
import { NetworkViewComponent } from './network-view.component';
import { FileDragDropDirective } from './file-drag-drop.directive';
import { CanvasControlComponent } from './controls/canvas-control/canvas-control.component';
import { NodeColourKeyComponent } from './controls/node-colour-key/node-colour-key.component';
import { NodeColourKeyItemComponent } from './controls/node-colour-key/node-colour-key-item/node-colour-key-item.component';

const components = [
  NetworkViewComponent
]

@NgModule({
  declarations: [
    ...components,
    FileDragDropDirective,
    CanvasControlComponent,
    NodeColourKeyComponent,
    NodeColourKeyItemComponent
  ],
  exports: [
    ...components
  ],
  imports: [
    CommonModule,
    MaterialModule
  ]
})
export class NetworkViewModule { }
