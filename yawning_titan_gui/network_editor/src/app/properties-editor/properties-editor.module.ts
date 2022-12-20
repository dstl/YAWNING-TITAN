import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PropertiesEditorComponent } from './properties-editor.component';
import { PropertiesEditorSidenavComponent } from './properties-editor-sidenav/properties-editor-sidenav.component';
import { MaterialModule } from '../material.module';
import { PropertiesEditorService } from './properties-editor.service';

const components = [
  PropertiesEditorComponent,
  PropertiesEditorSidenavComponent
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
  ],
  providers: [
    PropertiesEditorService
  ]
})
export class PropertiesEditorModule { }
