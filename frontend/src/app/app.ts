import { Component, signal } from '@angular/core';
import { CsvUpload } from './csv-upload/csv-upload';
import { ContractsTable } from './contracts-table/contracts-table';

@Component({
  selector: 'app-root',
  imports: [CsvUpload, ContractsTable],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  protected readonly title = signal('frontend');
}
