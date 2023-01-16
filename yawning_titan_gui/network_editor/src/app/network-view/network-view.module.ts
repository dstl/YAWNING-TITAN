import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MaterialModule } from '../material.module';
import { ControlsComponent } from './controls/controls.component';
import { NetworkViewComponent } from './network-view.component';
import { FileDragDropDirective } from './file-drag-drop.directive';

const components = [
  ControlsComponent,
  NetworkViewComponent
]

@NgModule({
  declarations: [
    ...components,
    FileDragDropDirective
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
