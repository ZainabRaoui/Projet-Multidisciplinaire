import { Component, OnInit } from '@angular/core';
import { ChartOptions, ChartType, ChartDataSets } from 'chart.js';
import { Label } from 'ng2-charts';


@Component({
  selector: 'app-maps',
  templateUrl: './maps.component.html',
  styleUrls: ['./maps.component.css']
})
export class MapsComponent implements OnInit {
  // Données statiques des utilisateurs
  users = [
    { firstName: 'John', lastName: 'Doe', age: 25, country: 'USA', time: 'Morning' },
    { firstName: 'Jane', lastName: 'Smith', age: 30, country: 'UK', time: 'Afternoon' },
    { firstName: 'Ali', lastName: 'Khan', age: 22, country: 'Pakistan', time: 'Evening' },
    { firstName: 'Maria', lastName: 'Garcia', age: 28, country: 'Spain', time: 'Night' },
    { firstName: 'Ahmed', lastName: 'Moussa', age: 35, country: 'Egypt', time: 'Morning' },
    { firstName: 'Emily', lastName: 'Johnson', age: 27, country: 'Canada', time: 'Afternoon' },
  ];

  constructor() { }

  ngOnInit(): void {
  }

}
