import { Injectable, isDevMode } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ConfigurationService {

  private _config: any;

  get config() { return this._config; }

  constructor(private httpClient: HttpClient) { }

  /**
   * Load a JSON configuration file from the given location
   * @param location
   * @returns
   */
  public loadConfig(location: string): any {
    return this.httpClient.get(`${window.location.origin}/${location}`, {
      responseType: 'text'
    })
      .pipe(tap((res: string) => {
        // replace assets with the correct path
        let assetsPathStr = isDevMode() ? `${window.location.origin}/assets` :
          `${window.location.origin}/_static/dist/assets`;

        res = res.replaceAll(/{{ASSETS_PATH}}/ig, assetsPathStr)

        // replace host with the correct value
        let hostStr = window.location.origin;
        res = res.replaceAll(/{{HOST}}/ig, hostStr)

        this._config = JSON.parse(res)
      }));
  }
}
