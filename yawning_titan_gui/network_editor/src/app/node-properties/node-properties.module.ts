import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NodePropertiesComponent } from './node-properties.component';
import { NodePropertiesSidenavComponent } from './node-properties-sidenav/node-properties-sidenav.component';
import { MaterialModule } from '../material.module';
import { PropertiesEditorService } from './node-properties.service';
import { ReactiveFormsModule } from '@angular/forms';

const components = [
  NodePropertiesComponent,
  NodePropertiesSidenavComponent
]

@NgModule({
  declarations: [
    ...components
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
    PropertiesEditorService
  ]
})
export class NodePropertiesModule { }
