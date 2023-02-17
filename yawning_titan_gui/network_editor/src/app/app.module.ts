import { APP_INITIALIZER, isDevMode, NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppComponent } from './app.component';
import { CytoscapeService } from './services/cytoscape/cytoscape.service';
import { MaterialModule } from './material.module';
import { NetworkViewModule } from './network-view/network-view.module';
import { NodePropertiesModule } from './node-properties/node-properties.module';
import { HttpClientModule } from '@angular/common/http';
import { ConfigurationService } from './services/configuration/configuration.service';
import { CYTOSCAPE_STYLE, DJANGO_SAVE_URL } from './app.tokens';

export function djangoSaveUrlFactory(configurationService: ConfigurationService) {
  return configurationService.config?.saveLocation;
}

export function cytoscapeStyleFactory(configurationService: ConfigurationService) {
  return configurationService.config?.cytoscapeStyle;
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
    NodePropertiesModule,
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
    },
    {
      provide: CYTOSCAPE_STYLE,
      useFactory: cytoscapeStyleFactory,
      deps: [ConfigurationService]
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
