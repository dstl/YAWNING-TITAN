import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MaterialModule } from '../material.module';
import { NetworkViewComponent } from './network-view.component';
import { FileDragDropDirective } from './file-drag-drop.directive';
import { CanvasControlComponent } from './controls/canvas-control/canvas-control.component';
import { NodeColourKeyComponent } from './controls/node-colour-key/node-colour-key.component';
import { NodeColourKeyItemComponent } from './controls/node-colour-key/node-colour-key-item/node-colour-key-item.component';
import { MiniViewportComponent } from './controls/canvas-control/mini-viewport/mini-viewport.component';
import { MiniViewportService } from './controls/canvas-control/mini-viewport/mini-viewport.service';

const components = [
  NetworkViewComponent,
  MiniViewportComponent
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
  ],
  providers: [
    MiniViewportService
  ]
})
export class NetworkViewModule { }
