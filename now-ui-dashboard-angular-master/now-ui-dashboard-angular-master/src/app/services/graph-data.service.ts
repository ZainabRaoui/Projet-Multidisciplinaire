// src/app/services/graph-data.service.ts
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class GraphDataService {
  constructor() {}

  getGraphData(): Observable<any> {
    const graphData = {
      nodes: [
        { id: 'node1', label: 'Entity 1' },
        { id: 'node2', label: 'Sentiment 1' },
        { id: 'node3', label: 'Entity 2' },
      ],
      links: [
        { source: 'node1', target: 'node2', country: 'USA', age: '30-40' },
        { source: 'node2', target: 'node3', country: 'UK', age: '25-35' },
      ],
    };

    return of(graphData); // Retourne les données sous forme d'observable
  }
}
