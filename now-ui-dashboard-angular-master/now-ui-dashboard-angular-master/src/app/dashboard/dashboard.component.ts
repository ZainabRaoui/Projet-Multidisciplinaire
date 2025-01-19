import { Component, OnInit } from '@angular/core';
import { ChartOptions, ChartType, ChartDataSets } from 'chart.js';
import { Label } from 'ng2-charts';


@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  public lineBigDashboardChartData: any[];
  public lineBigDashboardChartLabels: string[];
  public lineBigDashboardChartColors: any[];
  public lineBigDashboardChartOptions: any;
  public lineBigDashboardChartType: string;

  public lineChartData: any[];
  public lineChartLabels: string[];
  public lineChartColors: any[];
  public lineChartOptions: any;
  public lineChartType: string;

  constructor() { }

  ngOnInit(): void {
    // Données statiques pour les graphiques
    this.lineBigDashboardChartData = [
      { data: [10, 15, 30, 40, 50], label: 'Positive Sentiment' },
      { data: [5, 10, 20, 30, 45], label: 'Negative Sentiment' }
    ];

    // Pays sur l'axe des X
    this.lineBigDashboardChartLabels = ['USA', 'France', 'Germany', 'UK', 'Spain'];

    this.lineBigDashboardChartColors = [
      { backgroundColor: 'rgba(0,255,0,0.3)', borderColor: 'rgba(0,255,0,1)', borderWidth: 2 },
      { backgroundColor: 'rgba(255,0,0,0.3)', borderColor: 'rgba(255,0,0,1)', borderWidth: 2 }
    ];

    this.lineBigDashboardChartOptions = {
      responsive: true,
      scales: {
        yAxes: [{ ticks: { beginAtZero: true } }]
      }
    };

    this.lineBigDashboardChartType = 'line';

    // Données supplémentaires pour un autre graphique
    this.lineChartData = [
      { data: [10, 20, 30, 40, 60], label: 'Tweets Count by Country' }
    ];

    // Pays sur l'axe des X
    this.lineChartLabels = ['USA', 'France', 'Germany', 'UK', 'Spain'];

    this.lineChartColors = [
      { backgroundColor: 'rgba(0,123,255,0.3)', borderColor: 'rgba(0,123,255,1)', borderWidth: 2 }
    ];

    this.lineChartOptions = {
      responsive: true,
      scales: {
        yAxes: [{ ticks: { beginAtZero: true } }]
      }
    };

    this.lineChartType = 'line';
  }

  chartHovered(event: any): void {
    // Code pour gérer l'événement hover sur le graphique
  }

  chartClicked(event: any): void {
    // Code pour gérer l'événement click sur le graphique
  }
}
