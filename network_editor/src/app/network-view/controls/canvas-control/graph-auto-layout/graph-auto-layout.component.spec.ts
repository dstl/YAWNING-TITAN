import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClient } from '@angular/common/http';
import { NO_ERRORS_SCHEMA } from '@angular/core';

import { GraphAutoLayoutComponent } from './graph-auto-layout.component';
import { UPDATE_NETWORK_LAYOUT_URL } from '../../../../app.tokens';
import { NetworkService } from '../../../../network-class/network.service';
import { MatMenuModule } from '@angular/material/menu';
import { Network } from 'src/app/network-class/network';
import { of } from 'rxjs';
import { MatSnackBar } from '@angular/material/snack-bar';

describe('GraphAutoLayoutComponent', () => {
  let component: GraphAutoLayoutComponent;
  let fixture: ComponentFixture<GraphAutoLayoutComponent>;

  const httpClientStub = {
    post: () => { }
  }

  const networkStub = {
    getNetworkJson: () => { },
    loadNetwork: () => { }
  }

  const snackbarStub = {
    openFromComponent: () => {}
  }

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [GraphAutoLayoutComponent],
      imports: [MatMenuModule],
      providers: [
        { provide: UPDATE_NETWORK_LAYOUT_URL, useValue: '' },
        { provide: HttpClient, useValue: httpClientStub },
        { provide: NetworkService, useValue: networkStub },
        { provide: MatSnackBar, useValue: snackbarStub },
      ],
      schemas: [
        NO_ERRORS_SCHEMA
      ]
    })
      .compileComponents();

    fixture = TestBed.createComponent(GraphAutoLayoutComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('METHOD: autoLayoutsAvailable', () => {
    afterEach(() => {
      (<any>window).NETWORK_LAYOUTS = undefined;
    });

    it('should parse the layouts available', () => {
      (<any>window).NETWORK_LAYOUTS = '["test"]';

      expect(component.autoLayoutsAvailable()).toBeTruthy();
      expect(component.layouts).toEqual(["test"]);
    });

    it('should set layouts to be an empty array if there are no layouts', () => {
      (<any>window).NETWORK_LAYOUTS = undefined;

      expect(component.autoLayoutsAvailable()).toBeFalsy();
      expect(component.layouts).toEqual([]);
    })
  });

  describe('METHOD: applyLayout', () => {
    it('should load the network returned after sorting', () => {
      let network = new Network();
      network.addNode(0.05, 0.05, 0);
      const httpSpy = spyOn(component['httpClient'], 'post').and.returnValue(of(network.toJson()));
      const loadNetworkSpy = spyOn(component['networkService'], 'loadNetwork');
      const scaleUpNodePositionsSpy = spyOn<any>(component, 'scaleUpNodePositions').and.returnValue(
        network.toJson()
      )

      component.applyLayout('');

      expect(httpSpy).toHaveBeenCalled();
      expect(scaleUpNodePositionsSpy).toHaveBeenCalled();
      expect(loadNetworkSpy).toHaveBeenCalled();
    });
  });

  describe('METHOD: scaleUpNodePositions', () => {
    let canvas = document.createElement('canvas');
    beforeEach(() => {
      canvas = document.createElement('canvas');
      canvas.style['width'] = "200px";
      canvas.style['height'] = "100px";
      canvas.className = 'canvas-test';
      canvas.id = 'cytoscapeCanvas';
      document.body.appendChild(canvas);
    });

    afterEach(() => {
      document.body.removeChild(canvas);
    })

    it('should scale up the returned node positions to fit the screen', () => {
      const network = {
        nodes: {
          '1': {
            uuid: '1',
            name: 'node',
            x_pos: 0.05,
            y_pos: 0.05
          }
        }
      }

      const expected = {
        nodes: {
          '1': {
            uuid: '1',
            name: 'node',
            x_pos: 5,
            y_pos: 5
          }
        }
      }

      expect(component['scaleUpNodePositions'](network as any)).toEqual(expected as any)
    });
  });
});
