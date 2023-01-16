import { TestBed } from '@angular/core/testing';

import { ConfigurationService } from './configuration.service';
import { of } from 'rxjs';
import { HttpClient } from '@angular/common/http';

describe('ConfigurationService', () => {
  let service: ConfigurationService;

  const stubHttp = {
    get: () => of()
  };

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        { provide: HttpClient, useValue: stubHttp }
      ]
    });
    service = TestBed.get(ConfigurationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('METHOD: loadConfig', () => {
    it('should set the config', () => {
      const stubConfig = {
        config: 'yes'
      };
      spyOn<any>(service['httpClient'], 'get').and.returnValue(of(stubConfig));
      service.loadConfig('').toPromise();
      expect(service['_config']).toBe(stubConfig);
    });
  });
});
