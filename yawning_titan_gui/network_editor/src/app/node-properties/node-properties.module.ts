import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NodePropertiesComponent } from './node-properties.component';
import { NodePropertiesSidenavComponent } from './node-properties-sidenav/node-properties-sidenav.component';
import { MaterialModule } from '../material.module';
import { NodePropertiesService } from './node-properties.service';
import { ReactiveFormsModule } from '@angular/forms';
import { FocusTrackingDirective } from './directive/focus-tracking.directive'

const components = [
  NodePropertiesComponent,
  NodePropertiesSidenavComponent,
  FocusTrackingDirective
]

@NgModule({
  declarations: [
    ...components,

  ],
  exports: [
    ...components
  ],
  imports: [
    CommonModule,
    MaterialModule,
    ReactiveFormsModule,
  ],
  providers: [
    NodePropertiesService
  ]
})
export class NodePropertiesModule { }
