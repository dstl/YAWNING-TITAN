import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppComponent } from './app.component';
import { CytoscapeService } from './services/cytoscape/cytoscape.service';
import { MaterialModule } from './material.module';
import { NetworkViewModule } from './network-view/network-view.module';
import { PropertiesEditorModule } from './properties-editor/properties-editor.module';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    MaterialModule,
    PropertiesEditorModule,
    NetworkViewModule
  ],
  providers: [
    CytoscapeService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
