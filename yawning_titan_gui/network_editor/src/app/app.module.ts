import { APP_INITIALIZER, isDevMode, NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppComponent } from './app.component';
import { CytoscapeService } from './services/cytoscape/cytoscape.service';
import { MaterialModule } from './material.module';
import { NetworkViewModule } from './network-view/network-view.module';
import { PropertiesEditorModule } from './properties-editor/properties-editor.module';
import { HttpClientModule } from '@angular/common/http';
import { ConfigurationService } from './services/configuration/configuration.service';
import { DJANGO_SAVE_URL } from './app.tokens';

export function djangoSaveUrlFactory(configurationService: ConfigurationService) {
  return configurationService.config?.saveLocation;
}

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    MaterialModule,
    PropertiesEditorModule,
    NetworkViewModule
  ],
  providers: [
    CytoscapeService,
    ConfigurationService,
    {
      provide: APP_INITIALIZER, deps: [ConfigurationService], multi: true,
      useFactory: (configurationService: ConfigurationService) => () => configurationService.loadConfig(
        isDevMode() ? 'assets/config.json' : 'static/dist/assets/config.json'
      ).toPromise(),
    },
    {
      provide: DJANGO_SAVE_URL,
      useFactory: djangoSaveUrlFactory,
      deps: [ConfigurationService]
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
