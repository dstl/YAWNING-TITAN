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
        let replaceStr = isDevMode() ? `${window.location.origin}/assets` :
          `${window.location.origin}/static/dist/assets`;

        res = res.replace(/{{.*}}/, replaceStr)

        this._config = JSON.parse(res)
      }));
  }
}
